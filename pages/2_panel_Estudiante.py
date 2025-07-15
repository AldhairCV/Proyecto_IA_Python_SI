import streamlit as st
from model.preprocesamiento import codificar_respuestas
from model.logica_difusa import generar_recomendacion
from nlp.analisis_sentimientos import analizar_sentimiento
from firebase.firebase_config import db
import joblib
import csv
from datetime import datetime
import google.generativeai as genai

# 🔐 Configurar clave de Gemini
genai.configure(api_key="AIzaSyAeUgPPwE0lvoPVsk9OSTo6wv77jF0KS4E")  # Reemplaza con tu API KEY válida

st.set_page_config(page_title="Panel Estudiante", layout="centered")
st.title("🧠 Evaluación Emocional para los Estudiantes")

# Cargar modelo IA
modelo = joblib.load("model/modelo_clasificacion.pkl")

# Inicializar estado
if "form_data" not in st.session_state:
    st.session_state.form_data = {
        "nombre": "",
        "texto": "",
        "respuestas": ["Nunca"] * 5,
        "evaluado": False,
        "riesgo": "",
        "sentimiento": "",
        "recomendacion": "",
        "chat_context": "",
        "chatbot": None
    }

# 🧹 Botón de limpieza
if st.button("🧹 Limpiar todo"):
    st.session_state.form_data = {
        "nombre": "",
        "texto": "",
        "respuestas": ["Nunca"] * 5,
        "evaluado": False,
        "riesgo": "",
        "sentimiento": "",
        "recomendacion": "",
        "chat_context": "",
        "chatbot": None
    }
    st.rerun()

# --------------------
# FORMULARIO PRINCIPAL
# --------------------

# Nombre
nombre = st.text_input("👤 Tu nombre completo:", value=st.session_state.form_data["nombre"])
st.session_state.form_data["nombre"] = nombre

# Texto libre
texto = st.text_area("📝 ¿Cómo te sientes hoy?", value=st.session_state.form_data["texto"])
st.session_state.form_data["texto"] = texto

# Preguntas tipo Likert
opciones = ["Nunca", "A veces", "Frecuentemente", "Siempre"]
preguntas = [
    "¿Con qué frecuencia te sientes desmotivado?",
    "¿Has perdido interés en actividades?",
    "¿Te cuesta concentrarte?",
    "¿Sientes tristeza sin razón?",
    "¿Tienes problemas para dormir?"
]

respuestas = []
for i, pregunta in enumerate(preguntas):
    respuesta = st.selectbox(
        pregunta,
        opciones,
        index=opciones.index(st.session_state.form_data["respuestas"][i]),
        key=f"pregunta_{i}"
    )
    respuestas.append(respuesta)
    st.session_state.form_data["respuestas"][i] = respuesta

# --------------------
# EVALUACIÓN
# --------------------

if st.button("🟢 Evaluar ahora"):
    if not nombre or not texto or any(r == "" for r in respuestas):
        st.warning("⚠️ Por favor completa todos los campos.")
    else:
        respuestas_codificadas = [codificar_respuestas(r) for r in respuestas]
        sentimiento = analizar_sentimiento(texto)
        riesgo = modelo.predict([respuestas_codificadas])[0]
        recomendacion = generar_recomendacion(riesgo, sentimiento)

        st.session_state.form_data["riesgo"] = riesgo
        st.session_state.form_data["sentimiento"] = sentimiento
        st.session_state.form_data["recomendacion"] = recomendacion
        st.session_state.form_data["evaluado"] = True

        st.success("✅ Evaluación completada")
        st.write(f"**Nivel de riesgo:** {riesgo}")
        st.write(f"**Sentimiento detectado:** {sentimiento}")
        st.info(f"**Recomendación:** {recomendacion}")

        # Guardar en CSV
        with open("data/respuestas_guardadas.csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                nombre, texto, *respuestas, riesgo, sentimiento, recomendacion
            ])

        # Guardar en Firebase
        doc = {
            "Fecha_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Nombre_del_estudiante": nombre,
            "Mensaje_libre": texto,
            "respuesta_1": respuestas[0],
            "respuesta_2": respuestas[1],
            "respuesta_3": respuestas[2],
            "respuesta_4": respuestas[3],
            "respuesta_5": respuestas[4],
            "Nivel_de_riesgo": riesgo,
            "Tipo_sentimiento": sentimiento,
            "Recomendacion": recomendacion
        }
        db.collection("respuestas").add(doc)

        # Preparar chatbot
        st.session_state.form_data["chat_context"] = (
            f"Eres un orientador emocional empático. "
            f"El estudiante ha sido evaluado con:\n"
            f"- Nivel de riesgo: {riesgo}\n"
            f"- Sentimiento detectado: {sentimiento}\n"
            f"- Recomendación inicial: {recomendacion}\n"
            f"Con esa información, responde con consejos amables y útiles según lo que el estudiante pregunte."
        )
        st.session_state.form_data["chatbot"] = None  # Forzar reinicio del chat

# --------------------
# CHAT CON GEMINI
# --------------------

if st.session_state.form_data["evaluado"]:
    st.markdown("---")
    st.subheader("💬 ¿Deseas un mejor consejo?")

    if st.session_state.form_data["chatbot"] is None:
        modelo = genai.GenerativeModel("gemini-2.0-flash")
        chatbot = modelo.start_chat(history=[])
        chatbot.send_message(st.session_state.form_data["chat_context"])
        st.session_state.form_data["chatbot"] = chatbot

    with st.form("chat_form"):
        pregunta_usuario = st.text_input("Haz tu pregunta:", placeholder="Ej: ¿Qué puedo hacer para sentirme más animado?")
        enviar = st.form_submit_button("Preguntar")

    if enviar and pregunta_usuario:
        try:
            respuesta = st.session_state.form_data["chatbot"].send_message(pregunta_usuario)
            st.markdown("**🤖 Respuesta del orientador:**")
            st.success(respuesta.text)
        except Exception as e:
            if "ResourceExhausted" in str(e) or "quota" in str(e).lower():
                st.warning("🚫 Has alcanzado el límite gratuito diario o por minuto de Gemini.")
                st.info("Intenta nuevamente más tarde o revisa tu cuenta en: [Gemini API Quotas](https://ai.google.dev/gemini-api/docs/rate-limits)")
            else:
                st.error("❌ Error al contactar con Gemini.")
                st.exception(e)
