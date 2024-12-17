from openai import OpenAI
import streamlit as st 
from dotenv import load_dotenv
import os

load_dotenv()
key = os.getenv("OPENAI_API_KEY")
print("API KEY:", key)

client = OpenAI(api_key=key)

value = st.chat_input("user")

if (value): 
    with st.chat_message("assistant"): 
        st.write(value)

    with (st.chat_message("assistant")):
        txt = st.header("Waiting for api...")

        completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user","content": value}
        ]
        )

        txt.text(completion.choices[0].message.content)