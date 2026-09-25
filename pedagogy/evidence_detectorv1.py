VALID_EVENTS = (
    "plan_ready",
    "difficulty_detected",
    "difficulty_resolved",
    "activity_completed",
    "none",
)


def detect_pedagogical_event(message):
    """
    Detecta de manera inicial evidencias explícitas
    presentes en el mensaje del estudiante.

    Esta primera versión utiliza reglas simples y
    controladas. Posteriormente podrá sustituirse
    o complementarse con otros mecanismos.
    """

    text = message.lower().strip()

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

    if any(pattern in text for pattern in completed_patterns):
        return "activity_completed"

    if any(pattern in text for pattern in resolved_patterns):
        return "difficulty_resolved"

    if any(pattern in text for pattern in difficulty_patterns):
        return "difficulty_detected"

    if any(pattern in text for pattern in plan_patterns):
        return "plan_ready"

    return "none"