import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq

# 1. Cargar variables de entorno
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# 2. Configuración de página
st.set_page_config(page_title="Mundial Chatbot", page_icon="⚽")

st.markdown("""
    <style>
    .main { background-color: #e8f5e9; }
    .stButton>button { background-color: #2e7d32; color: white; border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚽ Mundial Chatbot")
st.subheader("Información oficial de los Mundiales")

# 3. Función optimizada para leer el contexto
def leer_contexto():
    try:
        # Asegúrate de que el archivo esté en la misma carpeta
        with open("conocimiento.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Error: No se encontró la base de conocimientos."

contexto_fijo = leer_contexto()

# 4. Inicializar historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes previos
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Lógica del Chatbot
if prompt := st.chat_input("¿Qué quieres saber sobre los mundiales?"):
    # Agregar pregunta del usuario al historial
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Preparamos los mensajes para la API
        # Incluimos las instrucciones del sistema PRIMERO
        mensajes_api = [
            {
                "role": "system", 
                "content": f"""Eres un experto en historia del fútbol. 
                REGLA CRÍTICA: Responde exclusivamente usando la información del CONTEXTO. 
                Si la respuesta no está en el CONTEXTO, responde: 'Lo siento, mi base de datos no contiene esa información específica'.
                No inventes datos ni uses conocimiento previo fuera del texto proporcionado.
                
                CONTEXTO:
                {contexto_fijo}"""
            }
        ]
        
        # Agregamos el historial reciente para que tenga memoria de la charla
        for m in st.session_state.messages[-5:]: # Enviamos los últimos 5 mensajes para ahorrar tokens
            mensajes_api.append({"role": m["role"], "content": m["content"]})

        # Llamada a Groq con parámetros de precisión
        response = client.chat.completions.create(
            messages=mensajes_api,
            model="llama-3.3-70b-versatile",
            temperature=0.1,  # Muy baja para evitar alucinaciones
            max_tokens=800,
            top_p=1,
        )
        
        full_response = response.choices[0].message.content
        st.markdown(full_response)
    
    # Guardar respuesta del asistente
    st.session_state.messages.append({"role": "assistant", "content": full_response})
