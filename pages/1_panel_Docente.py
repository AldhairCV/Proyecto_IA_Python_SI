import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Panel del Tutor", layout="wide")
st.title("📋 Panel del Tutor")

# 🔒 Protección: verificar sesión
if not st.session_state.get("docente_autenticado", False):
    st.warning("🔐 Acceso denegado. Debes iniciar sesión como docente desde la página principal.")
    st.stop()

try:
    df = pd.read_csv("data/respuestas_guardadas.csv")

    # Validar columnas
    if df.shape[1] == 11:
        df.columns = [
            "Fecha", "Nombre", "Texto", "Respuesta 1", "Respuesta 2",
            "Respuesta 3", "Respuesta 4", "Respuesta 5",
            "Riesgo", "Sentimiento", "Recomendación"
        ]
    else:
        st.error(f"❌ Número inesperado de columnas: se esperaban 11, pero hay {df.shape[1]}.")
        st.stop()

    # Mostrar tabla completa
    st.subheader("📄 Todas las evaluaciones registradas")
    st.dataframe(df, use_container_width=True)

    # Mostrar gráfico de distribución
    
    st.subheader("📊 Distribución por nivel de riesgo (ordenado)")

    orden_niveles = ["muy_alto", "alto", "medio", "bajo", "muy_bajo"]

    conteo = df["Riesgo"].value_counts().reindex(orden_niveles, fill_value=0).reset_index()
    conteo.columns = ["Nivel de riesgo", "Cantidad"]

    chart = alt.Chart(conteo).mark_bar().encode(
        x=alt.X("Nivel de riesgo", sort=orden_niveles, title="Nivel de riesgo"),
        y=alt.Y("Cantidad", title="Número de estudiantes"),
        tooltip=["Nivel de riesgo", "Cantidad"],
        color=alt.Color("Nivel de riesgo", sort=orden_niveles)
    ).properties(
        width=700,
        height=400
    )

    st.altair_chart(chart, use_container_width=True)

    # Filtro por riesgo
    st.subheader("🎯 Filtrar por nivel de riesgo")
    riesgos = df["Riesgo"].unique()
    seleccionados = st.multiselect("Selecciona niveles de riesgo:", riesgos, default=riesgos)

    filtrado = df[df["Riesgo"].isin(seleccionados)]

    # Mostrar datos filtrados
    st.subheader("📋 Estudiantes filtrados")
    st.dataframe(filtrado, use_container_width=True)

except FileNotFoundError:
    st.error("❌ No se encontró el archivo 'respuestas_guardadas.csv'.")

except Exception as e:
    st.error(f"❌ Error al procesar los datos: {e}")
