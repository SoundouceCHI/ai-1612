from openai import OpenAI
import streamlit as st 
from dotenv import load_dotenv
import os

load_dotenv()
key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=key)

value = st.text_input("Prompt...")

if (value):
    txt = st.header("Waiting for api...")

    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user","content": value}
    ]
    )

txt.text(completion.choices[0].message.content)