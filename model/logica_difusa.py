def generar_recomendacion(nivel_riesgo, sentimiento):
    if nivel_riesgo == "muy_alto":
        return "🔴 ¡Es muy importante que busques ayuda! Por favor_recurre a tu docente o tutor de confianza para que te brinde la ayuda y el apoyo necesarios de inmediato."

    elif nivel_riesgo == "alto":
        return "🔶 Si te sientes mal_te recomendamos hablar con alguien de confianza en el colegio para recibir un seguimiento personalizado. Te sentirás mejor." if sentimiento == "negativo" else "🟠 Te haremos un seguimiento cada quince días para ver cómo te sientes y te ayudaremos a fortalecer tus amistades y redes de apoyo. ¡No estás solo!"

    elif nivel_riesgo == "medio":
        if sentimiento == "negativo":
            return "🟡 Te sugerimos realizar ejercicios de autocuidado para sentirte mejor y hablaremos con tu tutor para ver cómo podemos ayudarte."
        elif sentimiento == "positivo":
            return "🟢 ¡Sigue así! Estaremos observando tu evolución y nos pondremos en contacto contigo en 15 días para ver cómo sigues."
        else:
            return "🟡 Vamos a programar una tutoría grupal para ver cómo se sienten todos y así poder apoyarnos mutuamente."

    elif nivel_riesgo == "bajo":
        return "🟠 ¡Fortalece tus amistades y lazos con las personas que te quieren! Eso te ayudará mucho." if sentimiento == "negativo" else "🟢 ¡Sigue cultivando esos hábitos positivos! Te están ayudando a estar muy bien."

    elif nivel_riesgo == "muy_bajo":
        return "🟢 ¡Excelente! Tu estado emocional es óptimo. ¡Aprovecha para fomentar tu liderazgo y ayudar a otros!" if sentimiento == "positivo" else "🟡 Tendremos una conversación breve para confirmar que todo sigue estable y que te sientes bien."

    return "⚠️ La información no es clara. Por favor_repite el cuestionario para que podamos entender mejor cómo te sientes."