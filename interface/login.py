import tkinter as tk
from tkinter import messagebox, simpledialog
from interface.ventanas import crear_ventana_inicio
from interface.panel_docente import mostrar_panel_docente
from interface.app import ejecutar_sistema

def seleccionar_rol():
    ventana = tk.Tk()
    ventana.title("🎓 Selección de Rol")
    ventana.geometry("800x500")
    ventana.configure(bg="#eaf2f8")
    ventana.resizable(False, False)

    tk.Label(
        ventana,
        text="🧠 Sistema de Apoyo Emocional",
        font=("Helvetica", 24, "bold"),
        bg="#eaf2f8",
        fg="#2c3e50"
    ).pack(pady=40)

    tk.Label(
        ventana,
        text="¿Cómo deseas ingresar?",
        font=("Helvetica", 18),
        bg="#eaf2f8"
    ).pack(pady=10)

    def ingresar_estudiante():
        ventana.destroy()
        crear_ventana_inicio(ejecutar_sistema)

    def ingresar_docente():
        clave = simpledialog.askstring("🔒 Acceso Docente", "Ingresa la clave:", show="*")
        if clave == "tutor123":
            ventana.destroy()
            mostrar_panel_docente()
        else:
            messagebox.showerror("Error", "Clave incorrecta.")

    # Botones de acceso
    boton_estudiante = tk.Button(
        ventana, text="👨‍🎓 Ingresar como Estudiante",
        font=("Arial", 16), bg="#5dade2", fg="white",
        width=30, height=2, command=ingresar_estudiante
    )
    boton_estudiante.pack(pady=15)

    boton_docente = tk.Button(
        ventana, text="👩‍🏫 Ingresar como Docente",
        font=("Arial", 16), bg="#48c9b0", fg="white",
        width=30, height=2, command=ingresar_docente
    )
    boton_docente.pack(pady=15)

    # Botón de salir
    boton_salir = tk.Button(
        ventana, text="❌ Salir",
        font=("Arial", 14), bg="#e74c3c", fg="white",
        width=15, command=ventana.destroy
    )
    boton_salir.pack(pady=20)

    ventana.mainloop()
