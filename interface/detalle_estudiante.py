import tkinter as tk

def mostrar_detalle_estudiante(row_data):
    ventana = tk.Toplevel()
    ventana.title("👁️ Detalle del Estudiante")
    ventana.geometry("650x620")
    ventana.configure(bg="#f0f4f8")

    tk.Label(
        ventana,
        text="👤 Detalle de Evaluación",
        font=("Helvetica", 18, "bold"),
        bg="#f0f4f8"
    ).pack(pady=10)

    campos = [
        "Fecha", "Nombre", "¿Cómo se siente hoy?",
        "¿Con qué frecuencia se siente desmotivado?",
        "¿Ha perdido interés en actividades?",
        "¿Le cuesta concentrarse?",
        "¿Siente tristeza sin razón?",
        "¿Tiene problemas para dormir?",
        "Nivel de Riesgo", "Sentimiento Detectado"
    ]

    for i, campo in enumerate(campos):
        frame = tk.Frame(ventana, bg="#f0f4f8")
        frame.pack(fill="x", padx=30, pady=4)

        tk.Label(
            frame,
            text=campo + ":",
            font=("Arial", 12, "bold"),
            bg="#f0f4f8",
            width=32,
            anchor="w"
        ).pack(side="left")

        entrada = tk.Entry(frame, font=("Arial", 11), width=35)
        entrada.insert(0, row_data[i])  # ⬅️ Aquí se asigna el valor
        entrada.configure(state="readonly")  # Se pone en solo lectura después
        entrada.pack(side="left")

    # ✅ Color de advertencia si el riesgo es "muy_alto"
    if row_data[8].strip().lower() == "muy_alto":
        alerta = tk.Label(
            ventana,
            text="⚠️ Riesgo muy alto: Intervención urgente recomendada",
            font=("Arial", 12, "bold"),
            fg="white",
            bg="#e74c3c",
            pady=10
        )
        alerta.pack(pady=20, fill="x", padx=30)

    # 🔙 Botón para cerrar ventana
    tk.Button(
        ventana,
        text="❌ Cerrar",
        font=("Arial", 14, "bold"),
        bg="#7f8c8d",
        fg="white",
        width=20,
        command=ventana.destroy
    ).pack(pady=30, padx=20)
