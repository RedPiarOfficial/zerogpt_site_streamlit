import streamlit as st
from utils import get_sidebar_default, get_sidebar_characters

st.set_page_config(layout="wide")

get_sidebar_default()
get_sidebar_characters()

def render_character_cards_grid(characters):
    html_cards = ""
    for char in characters:
        html_cards += f"""
        <div class="card">
            <img src="{char['avatar']}" alt="{char['name']}">
            <h3>{char['name']}</h3>
            <p>{char['description']}</p>
            <a href="/chat?character={char['id']}" target="_self">💬 Начать диалог</a>
        </div>
        """

    # Объединяем стили и HTML в один блок
    st.markdown(
        f"""
        <style>
        .card-grid {{
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            justify-content: center;
            padding: 20px 0;
        }}

        .card {{
            background-color: #fff;
            color: #000;
            padding: 20px;
            border-radius: 16px;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
            text-align: center;
            width: 280px;
            min-width: 200px;
            font-family: "Segoe UI", sans-serif;
            transition: transform 0.2s ease;
        }}

        .card:hover {{
            transform: scale(1.03);
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.25);
        }}

        .card img {{
            width: 100px;
            height: 100px;
            border-radius: 50%;
            object-fit: cover;
            margin-bottom: 15px;
            border: 3px solid #ccc;
        }}

        .card h3 {{
            margin: 0;
            font-size: 20px;
            font-weight: 600;
        }}

        .card p {{
            margin: 6px 0 20px;
            font-size: 14px;
            color: #888;
        }}

        .card a {{
            display: inline-block;
            padding: 10px 20px;
            background-color: #1677ff;
            color: white;
            border-radius: 8px;
            text-decoration: none;
            font-weight: bold;
            transition: background 0.2s ease;
        }}

        .card a:hover {{
            background-color: #125fd1;
        }}

        @media (prefers-color-scheme: dark) {{
            .card {{
                background-color: #1e1e1e;
                color: #f0f0f0;
            }}
            .card p {{
                color: #aaa;
            }}
        }}
        </style>

        <div class="card-grid">
            {html_cards}
        </div>
        """,
        unsafe_allow_html=True
    )

st.header('ZeroGPT test for public')

st.write('Here we are testing the capabilities of the zerogpt library in Python. All services are provided for free, but not always with perfect quality — that’s why we’re testing them.')
st.write('In this version of the site, you can only chat with an LLM model.')
st.write('For now, image generation and image prompts are excluded from the site.')
st.write('In the near future, the site will be developed and more new functions will be added for better use and testing.')

st.header('Change log')
st.write('21.07.2025')
st.write('1. added using local storage for chat history')
st.write('2. added auto save chat history')
st.write('3. added delete chat history button')