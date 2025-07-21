import streamlit as st
import zerogpt
from utils import get_sidebar_default
import streamlit.components.v1 as components
from streamlit_local_storage import LocalStorage

AiClient = zerogpt.Client()
get_sidebar_default()
chat_id = st.query_params.get("character")
localStorage = LocalStorage()


# Инициализируем историю сообщений
if "messages" not in st.session_state:
    with st.spinner("Загрузка истории чата..."):
        st.session_state.messages = localStorage.getItem('chat_history') or []

st.sidebar.title(f"Chat Options")
with st.sidebar:
    think_mode = st.toggle("Think mode")
    uncensured = st.toggle('uncensured mode')
    with st.popover("add system"):
        system_message = st.text_area('System Message')
        if st.button("Set System Message", type="secondary"):
            messages = [msg for msg in st.session_state.messages if msg.get("role") != "system"]
            st.session_state.messages.insert(0, {'role': 'system', 'content': system_message})

    if st.button("Delete chat history"):
        components.html("""
    <script>
        localStorage.removeItem("chat_history");
        location.reload();
    </script>
    """, height=0)
        st.session_state.messages = []
        st.rerun()


def wrapped_gen(prompt):
    response = ""
    response_gen = AiClient.send_message(st.session_state.messages, think=think_mode, stream=True, uncensored=uncensured)
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
            st.write(message["content"])

# Получаем ввод от пользователя
prompt = st.chat_input("Введите ваш запрос")

if prompt:
    with st.chat_message("user"):
        st.write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        st.write_stream(wrapped_gen(prompt))

    localStorage.setItem('chat_history', st.session_state.messages)