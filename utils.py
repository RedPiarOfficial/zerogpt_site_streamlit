import streamlit as st
import streamlit.components.v1 as components

def get_sidebar_default():
    st.sidebar.title("Menu")
    with st.sidebar:
        st.page_link("app.py", label="Home", icon="🏠", use_container_width=True)
        st.page_link("pages/chat.py", label="Chat", icon="💬", use_container_width=True)
        st.page_link("pages/image.py", label="Image", icon="🖼️", use_container_width=True)

def get_sidebar_characters():
    st.sidebar.title("Menu Characters")
    with st.sidebar:
        st.page_link("pages/characterCreate.py", label="Character Create", use_container_width=True)

@st.dialog('System & FirstMessage')
def system_dialog(localStorage):
    system_message = st.text_area('System Message', placeholder='You best virtual asssistant')
    first_message = st.text_area('First_Message', placeholder='Hello, im your assistant!')

    st.caption('The history will be deleted after confirmation.')
    if st.button('Submit', type="secondary"):
        st.session_state.messages = [{'role': 'system', 'content': system_message}, {"role": "assistant", "content": first_message, "pure_think": ''}]
        st.session_state.history_chat = [{'role': 'system', 'content': system_message}, {"role": "assistant", "content": first_message}]
        localStorage.setItem('chat_history', st.session_state.messages, key='reset_chat')
        localStorage.setItem('opt_history', st.session_state.history_chat, key='reset_history')
        st.rerun()

@st.dialog('Delete History')
def Delete_History_dialog(localStorage):
    st.write('Confirm the deletion of the history.')

    if st.button('Confirm'):
        localStorage.deleteAll()
        st.session_state.messages = []
        st.session_state.history_chat = []
        st.rerun()