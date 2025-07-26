import streamlit as st
import zerogpt
import streamlit.components.v1 as components
from streamlit_local_storage import LocalStorage
import base64
from docx import Document
from io import BytesIO

from utils import get_sidebar_default, system_dialog, Delete_History_dialog

AiClient = zerogpt.Client()

get_sidebar_default()
chat_id = st.query_params.get("character")
localStorage = LocalStorage()

# Инициализируем историю сообщений
if "messages" not in st.session_state or 'opt_history' not in st.session_state:
    with st.spinner("Loading..."):
        st.session_state.messages = localStorage.getItem('chat_history') or []
        st.session_state.history_chat = localStorage.getItem('opt_history') or []

st.sidebar.title(f"Chat Options")
with st.sidebar:
    toggled = localStorage.getItem('options_toggle') or {'think_mode': False, 'uncensured': False}
    think_mode = st.toggle("Think mode", value=toggled['think_mode'])
    uncensured = st.toggle('uncensured mode', value=toggled['uncensured'])

    localStorage.setItem('options_toggle', {'think_mode': think_mode, 'uncensured': uncensured}, key='options_toggle')
    if st.button("Set System Message", type="secondary"):
        system_dialog(localStorage)

    if st.button("Delete chat history"):
        Delete_History_dialog(localStorage)


def wrapped_gen(prompt):
    response = ""
    response_gen = AiClient.send_message(st.session_state.history_chat, think=think_mode, stream=True, uncensored=uncensured)
    placeholder_think = st.empty()
    thinking = think_mode
    pure_think = ""
    for chunk in response_gen:
        if thinking:
            pure_think += chunk
            if "</think>" in chunk:
                thinking = False
                continue
            with placeholder_think.expander("🧠 Показать размышления"):
                st.markdown(pure_think, unsafe_allow_html=True)
        else:
            response += chunk
            yield chunk
    st.session_state.messages.append({"role": "assistant", "content": response, "pure_think": pure_think})
    st.session_state.history_chat.append({'role': 'assistant', 'content': response})

# Отображаем всю историю сообщений
for message in st.session_state.messages:
    if message["role"] == "system":
        continue
    with st.chat_message(message["role"]):
        if message["role"] == "assistant":
            if message.get("pure_think"):
                with st.expander("🧠 Показать размышления"):
                    st.markdown(message["pure_think"], unsafe_allow_html=True)
                st.write(message["content"])
            else:
                st.write(message["content"])
        else:
            st.write(message.get("basic_prompt", message["content"]))
            if "files" in message and message["files"]:
                st.markdown("📎 **Files:**")
                for f in message["files"]:
                    try:
                        file_bytes = base64.b64decode(f["content"])
                        st.download_button(
                            label=f"{f['name']}",
                            data=file_bytes,
                            file_name=f["name"],
                            mime=f["type"]
                        )
                    except Exception as e:
                        st.markdown(f"• `{f['name']}` (ошибка при декодировании)")

# Получаем ввод от пользователя
prompt = st.chat_input("Введите ваш запрос", accept_file="multiple", file_type=["txt", "docx"])

if prompt:
    final_prompt = ""
    saved_files = []

    if hasattr(prompt, "files") and prompt.files:
        for uploaded_file in prompt.files:
            file_bytes = uploaded_file.read()
            file_b64 = base64.b64encode(file_bytes).decode("utf-8")
            saved_files.append({
                "name": uploaded_file.name,
                "type": uploaded_file.type,
                "content": file_b64
            })

            text = ""
            filename = uploaded_file.name.lower()

            try:
                if filename.endswith(".docx"):
                    doc = Document(BytesIO(file_bytes))
                    text = "\n".join(p.text for p in doc.paragraphs)
                else:
                    # Пытаемся просто декодировать как текст
                    text = file_bytes.decode("utf-8")
            except Exception as e:
                text = file_bytes

            final_prompt += (
                f"\n📎 Uploaded file:\n"
                f"**{uploaded_file.name}**\n\n"
                f"{text}\n"
            )

    user_text = prompt.text if hasattr(prompt, "text") else prompt

    with st.chat_message("user"):
        st.write(user_text)
        if saved_files:
            for f in saved_files:
                try:
                    file_bytes = base64.b64decode(f["content"])
                    st.download_button(
                        label=f"Скачать {f['name']}",
                        data=file_bytes,
                        file_name=f["name"],
                        mime=f["type"]
                    )
                except Exception as e:
                    st.markdown(f"• `{f['name']}` (Error)")

    st.session_state.messages.append({
        "role": "user",
        "content": user_text + "\n\n" + final_prompt,
        "basic_prompt": user_text,
        "files": saved_files
    })
    st.session_state.history_chat.append({'role': 'user', 'content': user_text + "\n\n" + final_prompt})

    with st.chat_message("assistant"):
        st.write_stream(wrapped_gen(prompt))

    localStorage.setItem("chat_history", st.session_state.messages)
    localStorage.setItem('opt_history', st.session_state.history_chat, key='set_opthis')