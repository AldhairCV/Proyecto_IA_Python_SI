import streamlit as st

st.set_page_config(page_title="Sistema de Apoyo Emocional", layout="centered")

# Inicializar sesión
if "docente_autenticado" not in st.session_state:
    st.session_state.docente_autenticado = False

st.title("🔐 Acceso al Sistema de Apoyo Emocional")

with st.form("login"):
    correo = st.text_input("📧 Correo institucional")
    clave = st.text_input("🔑 Contraseña", type="password")
    entrar = st.form_submit_button("Ingresar")

if entrar:
    if correo == "admin.maestro@gmail.com" and clave == "tutor123":
        st.session_state.docente_autenticado = True
        st.success("✅ Acceso concedido al panel docente.")
        st.info("Ahora puedes entrar al panel desde la barra lateral.")
    else:
        st.warning("⚠️ Acceso como estudiante o datos incorrectos.")
