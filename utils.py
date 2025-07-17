import streamlit as st


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


        

