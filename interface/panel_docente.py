import tkinter as tk
from tkinter import ttk, messagebox
import csv
from interface.detalle_estudiante import mostrar_detalle_estudiante  # ✅ IMPORTACIÓN

def mostrar_panel_docente():
    ventana = tk.Tk()
    ventana.title("📋 Panel del Tutor")
    ventana.geometry("1150x600")
    ventana.configure(bg="#f4f6f8")

    tk.Label(
        ventana,
        text="📋 Respuestas de estudiantes",
        font=("Helvetica", 20, "bold"),
        bg="#f4f6f8",
        fg="#2c3e50"
    ).pack(pady=10)

    estilo = ttk.Style()
    estilo.theme_use("default")

    estilo.configure("Treeview",
                     font=("Helvetica", 14),
                     rowheight=40,
                     background="#ffffff",
                     fieldbackground="#ffffff")

    estilo.configure("Treeview.Heading",
                     font=("Helvetica", 15, "bold"),
                     background="#d5d8dc",
                     foreground="#2c3e50")

    columnas = ("alerta", "fecha", "nombre", "texto", "r1", "r2", "r3", "r4", "r5", "riesgo", "sentimiento")
    tree = ttk.Treeview(ventana, selectmode="browse", show="headings")
    tree["columns"] = columnas

    for col in columnas:
        ancho = 60 if col == "alerta" else 160 if col == "nombre" else 120
        if col == "texto":
            ancho = 250
        tree.heading(col, text=col.capitalize() if col != "alerta" else "⚠️")
        tree.column(col, anchor="center", width=ancho)

    tree.tag_configure("alerta", background="#f8d7da", foreground="#721c24")

    datos_respaldo = []

    try:
        with open("data/respuestas_guardadas.csv", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 10:
                    datos_respaldo.append(row)
                    fila = row.copy()
                    fila[1] = f"👤 {fila[1]}"
                    alerta = "⚠️" if row[8].strip().lower() == "muy_alto" else ""
                    if alerta:
                        tree.insert("", "end", values=(alerta, *fila), tags=("alerta",))
                    else:
                        tree.insert("", "end", values=("", *fila))
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontró el archivo de respuestas.")

    tree.pack(expand=True, fill="both", padx=10, pady=10)

    # 🔍 Evento doble clic para mostrar detalles del estudiante
    def al_seleccionar(event):
        item = tree.focus()
        if item:
            index = tree.index(item)
            mostrar_detalle_estudiante(datos_respaldo[index])

    tree.bind("<Double-1>", al_seleccionar)

    # 🔙 Botón para regresar al login (IMPORTACIÓN INTERNA)
    def volver_al_login():
        ventana.destroy()
        from interface.login import seleccionar_rol
        seleccionar_rol()

    tk.Button(
        ventana,
        text="🔙 Regresar al inicio",
        font=("Arial", 14),
        bg="#e74c3c",
        fg="white",
        command=volver_al_login
    ).pack(pady=15)

    ventana.mainloop()
