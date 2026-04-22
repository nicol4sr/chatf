import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq

# Cargar variables de entorno
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Configuración de página con temática futbolera
st.set_page_config(page_title="Mundial Chatbot", page_icon="⚽")

st.markdown("""
    <style>
    .main { background-color: #e8f5e9; }
    .stButton>button { background-color: #2e7d32; color: white; border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚽ Mundial Chatbot: Informacion de los Mundiales")
st.subheader("Consulta datos de los ganadores de los Mundiales")

# Función para leer el archivo txt local
def leer_contexto():
    try:
        with open("conocimiento.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "El archivo de conocimiento no se encuentra en la carpeta."

contexto = leer_contexto()

# Historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input del usuario
if prompt := st.chat_input("¿Qué quieres saber sobre el partido?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Construcción del Prompt con el contenido del TXT
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": f"Eres un experto en fútbol. Responde usando esta información: {contexto}"},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile",
        )
        full_response = response.choices[0].message.content
        st.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
        
