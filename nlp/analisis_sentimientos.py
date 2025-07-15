def analizar_sentimiento(texto):
    if not texto.strip():
        return "neutral"

    texto = texto.lower()
    palabras_positivas = ["feliz", "motivado", "contento", "bien", "alegre", "tranquilo", "positivo", "optimista", "emocionado"]
    palabras_negativas = ["triste", "solo", "desmotivado", "mal", "cansado", "estresado", "deprimido", "ansioso", "preocupado", "vacío", "enojado"]

    positivos = sum(1 for palabra in palabras_positivas if palabra in texto)
    negativos = sum(1 for palabra in palabras_negativas if palabra in texto)

    if positivos > negativos:
        return "positivo"
    elif negativos > positivos:
        return "negativo"
    return "neutral"
