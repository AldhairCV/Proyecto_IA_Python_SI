from model.logica_difusa import generar_recomendacion
from model.preprocesamiento import codificar_respuestas
from nlp.analisis_sentimientos import analizar_sentimiento
import joblib
from tkinter import messagebox
from datetime import datetime

import csv
import sys
import os

modelo = joblib.load('model/modelo_clasificacion.pkl')

def ejecutar_sistema(datos):
    respuestas_codificadas = [codificar_respuestas(r) for r in datos["respuestas"]]
    sentimiento = analizar_sentimiento(datos["texto"])
    riesgo = modelo.predict([respuestas_codificadas])[0]
    recomendacion = generar_recomendacion(riesgo, sentimiento)

    mensaje = (
        f"Estudiante: {datos['nombre']}\n\n"
        f"Riesgo emocional detectado: {riesgo}\n"
        f"Sentimiento expresado: {sentimiento}\n\n"
        f"Recomendación:\n{recomendacion}"
    )

    # ✅ Ahora también se pasa texto (respuesta emocional libre)
    guardar_respuesta(
        nombre=datos["nombre"],
        texto=datos["texto"],
        respuestas_texto=datos["respuestas"],
        riesgo=riesgo,
        sentimiento=sentimiento
    )

    messagebox.showinfo("Resultado del análisis", mensaje)


def guardar_respuesta(nombre, texto, respuestas_texto, riesgo, sentimiento):
    from firebase.firebase_config import db
    
    #Guardar en CSV
    with open("data/respuestas_guardadas.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            nombre,
            texto,
            *respuestas_texto,
            riesgo,
            sentimiento
        ])

    # 🔹 Guardar en Firestore
    doc = {
        "Fecha_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Nombre_del_estudiante": nombre,
        "Mensaje_libre": texto,
        "respuesta_1": respuestas_texto[0],
        "respuesta_2": respuestas_texto[1],
        "respuesta_3": respuestas_texto[2],
        "respuesta_4": respuestas_texto[3],
        "respuesta_5": respuestas_texto[4],
        "Nivel_de_riesgo": riesgo,
        "Tipo_sentimiento": sentimiento
    }

    db.collection("respuestas").add(doc)
    print("✅ Guardado también en Firebase.")

