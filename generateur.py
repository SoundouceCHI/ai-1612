from openai import OpenAI
import streamlit as st 
from dotenv import load_dotenv
import os
import whisper
import os
from pathlib import Path 

def generate_article_content(topic):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Tu es un rédacteur qui génère des articles clairs et informatifs."},
            {"role": "user", "content": f"Écris un article sur le sujet suivant : {topic} en 3 paragraphes."}
        ]
    )
    return response.choices[0].message.content

 
def generate_image(prompt):
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    return response.data[0].url

st.title("Générateur d'articles avec images")

 
topic = st.text_input("Choisir un sujet de l'article :", "")

if topic:
    st.subheader(topic)
    
    with st.spinner("Génération de l'article en cours..."):
        article_content = generate_article_content(topic)
        paragraphs = article_content.split("\n\n")  

    for i, paragraph in enumerate(paragraphs[:3]):   
        st.write(paragraph)
 
        with st.spinner(f"Création de l'image {i+1}..."):
            image_prompt = f"Illustration pour le sujet '{topic}', basée sur : {paragraph[:50]}"
            image_url = generate_image(image_prompt)
            st.image(image_url, caption=f"Image {i+1} générée pour '{topic}'")

    st.success("Article généré avec succès !")

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


#generer image 
def openai_create_image(prompt):
    response = client.images.generate(
        model="dall-e-3",  
        prompt=prompt,
        n=1,  # nb img
        size="1024x1024"  # Taille img
    )
    return response.data[0].url

def openai_create_image_variation(image_path, prompt):
    with open(image_path, "rb") as image_file:
        response = client.images.edit( 
            image=image_file,
            prompt=prompt,
            n=1,   
            size="1024x1024"   
        )
    return response.data[0].url

st.title("Génération d'images avec DALL·E")

uploaded_image = st.file_uploader("Téléchargez une image pour créer une variation :", type=["png", "jpg", "jpeg"])
variation_prompt = st.text_input("Entrez un prompt pour la variation (appuyez sur Entrée) :")
 
if uploaded_image and variation_prompt:
    with open("temp_image.png", "wb") as f:
        f.write(uploaded_image.getbuffer())
    variation_url = openai_create_image_variation("temp_image.png", variation_prompt)
    st.image(variation_url, caption="Variation de l'image avec DALL·E")
    os.remove("temp_image.png")   