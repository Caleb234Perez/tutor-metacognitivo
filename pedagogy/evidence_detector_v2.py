VALID_EVENTS = (
    "plan_ready",
    "difficulty_detected",
    "difficulty_resolved",
    "activity_completed",
    "none",
)


def select_relevant_clause(text):
    """
    Selecciona la parte más reciente del mensaje cuando
    existe un conector de contraste.

    En expresiones como:
    "No entendía, pero ya lo resolví",
    la proposición posterior al contraste representa
    el estado actual comunicado por el estudiante.
    """

    contrast_connectors = (
        " pero ",
        " sin embargo ",
        " aunque ",
    )

    relevant_text = text

    for connector in contrast_connectors:

        if connector in relevant_text:

            parts = relevant_text.split(connector)

            # Se utiliza la última proposición no vacía.
            for part in reversed(parts):

                part = part.strip()

                if part:
                    relevant_text = part
                    break

    return relevant_text


def detect_pedagogical_event(message):
    """
    Detecta evidencias explícitas presentes en el
    mensaje del estudiante.

    Esta versión incorpora una primera resolución
    de mensajes con contraste.
    """

    text = message.lower().strip()

    # Cuando existe contraste, se prioriza la
    # proposición que expresa el estado más reciente.
    relevant_text = select_relevant_clause(text)

    difficulty_patterns = (
        "no entiendo",
        "no sé cómo",
        "no se como",
        "estoy atorado",
        "estoy atascado",
        "no puedo",
        "me cuesta",
        "tengo dificultad",
        "sigo sin entender",
        "sigo sin comprender",
        "sigo atorado",
        "sigo atascado",
        "todavía no entiendo",
        "todavia no entiendo",
        "aún no entiendo",
        "aun no entiendo",
        "no me queda claro",
        "sigo confundido",
        "sigo confundida",
        "todavía estoy confundido",
        "todavía estoy confundida",
        "no logro entender",
        "sigo sin poder",
        "todavía no puedo",
        "todavia no puedo",
        "aún no puedo",
        "aun no puedo",
        "necesito más ayuda",
        "necesito mas ayuda",
        "necesito ayuda para",
        "no tiene sentido para mí",
        "no tiene sentido para mi",
        "estoy perdido",
        "estoy perdida",
    )

    resolved_patterns = (
        "ya entendí",
        "ya entendi",
        "ya pude",
        "ya funciona",
        "ya lo resolví",
        "ya lo resolvi",
        "creo que ya entendí",
        "creo que ya entendi",
        "me quedó claro",
        "me quedo claro",
        "ahora sí entendí",
        "ahora si entendí",
        "ahora sí entendi",
        "ahora si entendi",
    )

    completed_patterns = (
        "ya terminé",
        "ya termine",
        "terminé la actividad",
        "termine la actividad",
        "ya acabé",
        "ya acabe",
        "ya finalicé",
        "ya finalice",
    )

    plan_patterns = (
        "voy a",
        "primero voy",
        "mi plan es",
        "pienso hacer",
        "primero haré",
        "primero hare",
        "después voy",
        "despues voy",
    )

    if (
        not contains_partial_completion(relevant_text)
        and any(
            pattern in relevant_text
            for pattern in completed_patterns
        )
        
    ):
        return "activity_completed"

    if any(
        pattern in relevant_text
        for pattern in resolved_patterns
    ):
        return "difficulty_resolved"

    if (
        not contains_negated_difficulty(relevant_text)
        and any(
            pattern in relevant_text
            for pattern in difficulty_patterns
        )
        
    ):
        return "difficulty_detected"

    if (
        any (
            pattern in relevant_text
            for pattern in plan_patterns
        )
        and contains_learning_context(relevant_text) 
        and not contains_non_learning_context(relevant_text)      
    ):
        return "plan_ready"

    return "none"

def contains_negated_difficulty(text):
    """
    Detecta expresiones explícitas en las que el
    estudiante niega presentar una dificultad.

    Estas expresiones no deben interpretarse como
    difficulty_detected.
    """

    negated_difficulty_patterns = (
        "no tengo dificultad",
        "no tengo dificultades",
        "no necesito ayuda",
        "no necesito más ayuda",
        "no necesito mas ayuda",
        "no me cuesta",
        "no estoy confundido",
        "no estoy confundida",
        "no estoy atorado",
        "no estoy atascado",
        "no tengo problema",
        "no tengo problemas",
        "no puedo decir que sea difícil",
        "no puedo decir que sea dificil",
    )

    return any(
        pattern in text
        for pattern in negated_difficulty_patterns
    )
def contains_learning_context(text):
    """
    Detecta términos que vinculan una expresión de
    planeación con la actividad de aprendizaje.
    """

    learning_context_patterns = (
        "problema",
        "ejercicio",
        "actividad",
        "pregunta",
        "respuesta",
        "instrucciones",
        "datos",
        "procedimiento",
        "esquema",
        "texto",
        "tema",
        "paso",
        "pasos",
        "resolver",
        "responder",
        "revisar",
        "leer",
        "identificar",
        "analizar",
        "comprender",
        "explicar",
        "calcular",
    )

    return any(
        pattern in text
        for pattern in learning_context_patterns
    )
def contains_partial_completion(text):
    """
    Detecta expresiones que indican la finalización
    de una parte de la actividad, pero no necesariamente
    de la actividad completa.
    """

    partial_completion_patterns = (
        "terminé de leer",
        "termine de leer",
        "acabé de leer",
        "acabe de leer",
        "finalicé de leer",
        "finalice de leer",
        "primer ejercicio",
        "primera pregunta",
        "primer problema",
        "primera parte",
        "primer paso",
        "ahora sigo",
        "todavía falta",
        "todavia falta",
        "me falta",
    )

    return any(
        pattern in text
        for pattern in partial_completion_patterns
    )

def contains_non_learning_context(text):
    """
    Detecta expresiones que pueden coincidir con términos
    educativos, pero cuyo contexto indica una actividad
    ajena a la tarea de aprendizaje.
    """

    non_learning_patterns = (
        "hacer ejercicio en",
        "hacer ejercicio físico",
        "hacer ejercicio fisico",
        "ir al gimnasio",
        "entrenar en",
    )

    return any(
        pattern in text
        for pattern in non_learning_patterns
    )