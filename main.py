from openai import OpenAI
import streamlit as st 
from dotenv import load_dotenv
import os
import whisper
import os
from pathlib import Path 

load_dotenv()
key = os.getenv("OPENAI_API_KEY")
print("API KEY:", key)

client = OpenAI(api_key=key)

def capture_audio():
    audio_data = st.audio_input("Dites quelque chose")
    if audio_data is not None:
        audio_file = "input_audio.mp3"
        with open(audio_file, "wb") as f:
            f.write(audio_data.getbuffer())
        return audio_file


def transcribe_audio(audio_file):
    with open(audio_file, "rb") as file:
        translation = client.audio.translations.create(
        model="whisper-1",
        file=file
        )
    return translation.text

def get_gpt_response(prompt):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Tu es un assistant vocal intelligent."},
            {"role": "user", "content": prompt},
        ]
        )
    return response.choices[0].message.content.strip()

def text_to_speech(text):
    speech_file_path = Path(__file__).parent / "response_audio.mp3"
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text
    )
    print(response)
    print(type(response))
    response.stream_to_file(speech_file_path)
    return speech_file_path

def voice_assistant():
    try:
        st.title("Assistant Vocal")
 
        audio_data = capture_audio()
        if audio_data: 
            user_input = transcribe_audio(audio_data)
            st.write(f"Vous avez dit : {user_input}")
 
            gpt_response = get_gpt_response(user_input)
            st.write(f"Assistant : {gpt_response}")
 
            audio_response_file = text_to_speech(gpt_response)
 
            st.audio(str(audio_response_file), format="audio/mp3")

    except Exception as e:
        st.error(f"Une erreur est survenue : {e}")

if __name__ == "__main__":
    voice_assistant()
