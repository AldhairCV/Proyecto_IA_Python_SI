import tkinter as tk
from tkinter import ttk, messagebox

def crear_ventana_inicio(app_callback):
    ventana = tk.Tk()
    ventana.title("🧠 Sistema de Apoyo Emocional")
    ventana.geometry("750x720")
    ventana.configure(bg="#f0f4f8")
    ventana.resizable(False, False)

    tk.Label(ventana, text="🧠 Evaluación Emocional del Estudiante",
             font=("Helvetica", 20, "bold"), bg="#f0f4f8").pack(pady=20)

    marco = tk.Frame(ventana, bg="#ffffff", padx=30, pady=20, bd=2, relief="groove")
    marco.pack(pady=10)

    # Entrada de nombre
    tk.Label(marco, text="👤 Nombre del estudiante:", font=("Arial", 12, "bold"),
             bg="#ffffff").pack(anchor="w", pady=(5, 0))
    entrada_nombre = tk.Entry(marco, width=60, font=("Arial", 11))
    entrada_nombre.pack(pady=5)

    # Entrada de texto libre
    tk.Label(marco, text="📝 ¿Cómo se siente hoy?", font=("Arial", 12, "bold"),
             bg="#ffffff").pack(anchor="w", pady=(10, 0))
    entrada_sentimiento = tk.Entry(marco, width=60, font=("Arial", 11))
    entrada_sentimiento.pack(pady=5)

    # Preguntas tipo Likert
    opciones = ["Nunca", "A veces", "Frecuentemente", "Siempre"]
    preguntas = [
        "¿Con qué frecuencia se siente desmotivado?",
        "¿Ha perdido interés en actividades?",
        "¿Le cuesta concentrarse?",
        "¿Siente tristeza sin razón?",
        "¿Tiene problemas para dormir?"
    ]

    respuestas = []  # Guardamos los Combobox directamente

    for pregunta in preguntas:
        tk.Label(marco, text=f"❓ {pregunta}", font=("Arial", 12),
                 bg="#ffffff").pack(anchor="w", pady=(10, 0))

        combo = ttk.Combobox(
            marco,
            values=opciones,
            state="readonly",
            width=57,
            font=("Arial", 11)
        )
        combo.pack(pady=2)
        combo.set(opciones[0])
        respuestas.append(combo)

    # Función para limpiar los campos
    def limpiar_campos():
        entrada_nombre.delete(0, tk.END)
        entrada_sentimiento.delete(0, tk.END)
        for combo in respuestas:
            combo.set(opciones[0])
        messagebox.showinfo("Formulario limpio", "Todos los campos han sido reiniciados 🧹")

    # Función para procesar evaluación
    def procesar():
        nombre = entrada_nombre.get().strip()
        texto = entrada_sentimiento.get().strip()
        respuestas_texto = [c.get().strip() for c in respuestas]

        if not nombre or not texto:
            messagebox.showwarning("Campos incompletos", "Complete todos los campos antes de evaluar.")
            return

        if any(r not in opciones for r in respuestas_texto):
            messagebox.showwarning("Respuestas faltantes", "Seleccione una opción válida para cada pregunta.")
            return

        print("[DEBUG] Respuestas capturadas:", respuestas_texto)

        datos = {
            "nombre": nombre,
            "texto": texto,
            "respuestas": respuestas_texto
        }

        app_callback(datos)

    # 🧹 + 🟢 Botones alineados en fila
    botones_frame = tk.Frame(ventana, bg="#f0f4f8")
    botones_frame.pack(pady=17)

    # Botón de limpieza
    tk.Button(
        botones_frame,
        text="🧹",
        command=limpiar_campos,
        bg="#95a5a6",
        fg="white",
        font=("Arial", 13, "bold"),
        width=4,
        height=2
    ).pack(side="left", padx=10)

    # Botón de evaluación
    tk.Button(
        botones_frame,
        text="🟢 Evaluar",
        command=procesar,
        bg="#4CAF50",
        fg="white",
        font=("Arial", 13, "bold"),
        width=25,
        height=2
    ).pack(side="left", padx=10)

    # 🔙 Botón de regreso (con import diferido)
    def volver_al_login():
        ventana.destroy()
        from interface.login import seleccionar_rol
        seleccionar_rol()

    tk.Button(
        ventana,
        text="🔙 Regresar al inicio",
        command=volver_al_login,
        bg="#e74c3c",
        fg="white",
        font=("Arial", 12, "bold"),
        width=22,
        height=5
    ).pack(side="bottom",padx=5, pady=12 )

    ventana.mainloop()
