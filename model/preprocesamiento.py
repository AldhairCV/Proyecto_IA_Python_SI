def codificar_respuestas(respuesta):
    escala = {
        "Nunca": 0,
        "A veces": 1,
        "Frecuentemente": 2,
        "Siempre": 3
    }
    return escala.get(respuesta, 0)
