from ollama import chat


MODEL_NAME = "llama3.2:3b"

VALID_EVENTS = (
    "plan_ready",
    "difficulty_detected",
    "difficulty_resolved",
    "activity_completed",
    "none",
)
CONTEXTUAL_EVENTS = (
    "plan_ready",
    "difficulty_detected",
    "difficulty_resolved",
    "none",
)

CLASSIFIER_PROMPT = """
Actúas exclusivamente como un clasificador de evidencia
lingüística para un tutor metacognitivo.

NO eres un tutor conversacional.
NO debes responder ni aconsejar al estudiante.
NO debes explicar tu decisión.

La finalización completa de la actividad es evaluada
por otro componente del sistema.

Por lo tanto, NO debes clasificar ningún mensaje como
activity_completed.

Tu tarea consiste exclusivamente en distinguir entre
estas cuatro categorías:

plan_ready
difficulty_detected
difficulty_resolved
none

DEFINICIONES

plan_ready:
El estudiante expresa una intención o plan concreto
relacionado con la actividad de aprendizaje.

difficulty_detected:
El estudiante comunica confusión, duda, bloqueo,
falta de comprensión o incapacidad para continuar
con la actividad.

difficulty_resolved:
El estudiante comunica que una dificultad anterior
ha sido superada o que ahora comprende aquello
que antes no comprendía.

none:
No existe evidencia suficiente para clasificar el mensaje
en alguna de las categorías anteriores.

REGLAS

1. Si existe contraste, considera principalmente el estado
   actual expresado por el estudiante.

2. Una intención relacionada con resolver, revisar,
   comprender o analizar una actividad puede representar
   plan_ready.

3. Expresiones coloquiales de confusión, bloqueo o falta
   de comprensión pueden representar difficulty_detected.

4. Expresiones que indican que algo ahora quedó claro,
   que se encontró un error o que ya se comprendió pueden
   representar difficulty_resolved.

5. Si no existe evidencia suficiente, utiliza none.

FORMATO DE RESPUESTA

Devuelve SOLAMENTE una de estas cuatro palabras exactas:

plan_ready
difficulty_detected
difficulty_resolved
none
"""

def validate_activity_completion(message):
    """
    Valida de forma conservadora si un mensaje contiene
    evidencia suficiente para considerar que la actividad
    completa ha finalizado.

    Esta función no decide fases ni estrategias pedagógicas.
    Únicamente valida la evidencia lingüística de cierre.
    """

    text = message.lower().strip()

    # Señales explícitas de que todavía existe trabajo pendiente.
    incomplete_patterns = (
        "todavía no termino",
        "todavia no termino",
        "aún no termino",
        "aun no termino",
        "todavía me falta",
        "todavia me falta",
        "todavía me faltan",
        "todavia me faltan",
        "me falta",
        "me faltan",
        "ahora sigo",
        "sigo con",
        "voy con la siguiente",
        "voy con el siguiente",
        "continúo con",
        "continuo con",
        "antes de decir que terminé",
        "antes de decir que termine",
        "antes de decir que finalicé",
        "antes de decir que finalice",
    )

    if any(
        pattern in text
        for pattern in incomplete_patterns
    ):
        return False

    # Evidencias explícitas de finalización total.
    complete_patterns = (
        "toda la actividad",
        "actividad completa",
        "todo lo que me pedía",
        "todo lo que me pedia",
        "todos los ejercicios",
        "todas las preguntas",
        "respondí todo",
        "respondi todo",
        "terminé todo",
        "termine todo",
        "acabé todo",
        "acabe todo",
        "finalicé todo",
        "finalice todo",
        "completé todo",
        "complete todo",
        "no me falta ninguno",
        "no me falta nada",
    )

    if any(
        pattern in text
        for pattern in complete_patterns
    ):
        return True

    # También se aceptan expresiones breves de cierre
    # cuando constituyen prácticamente todo el mensaje.
    standalone_completion_patterns = (
        "ya terminé",
        "ya termine",
        "ya acabé",
        "ya acabe",
        "ya finalicé",
        "ya finalice",
        "terminé",
        "termine",
        "acabé",
        "acabe",
        "finalicé",
        "finalice",
    )

    normalized = text.rstrip(".! ")

    if normalized in standalone_completion_patterns:
        return True

    return False

def classify_pedagogical_evidence(message):
    """
    Clasifica evidencia lingüística del mensaje del estudiante
    utilizando un modelo local mediante Ollama.

    La función no realiza transiciones pedagógicas, no modifica
    scaffolding y no selecciona estrategias.
    """

    if not isinstance(message, str):
        raise TypeError(
            "message debe ser una cadena de texto."
        )

    message = message.strip()

    if not message:
        return "none"
    if validate_activity_completion(message):
        return "activity_completed"

    classification_request = f"""
    Clasifica el siguiente mensaje.
    <mensaje>
    {message}
    </mensaje>

    Devuelve solamente una categoría válida.
    """

    messages = [
        {
            "role": "system",
            "content": CLASSIFIER_PROMPT,
        },
        {
            "role": "user",
            "content": classification_request,
        },
    ]

    response = chat(
        model=MODEL_NAME,
        messages=messages,
        options={
            "temperature":0,
        },
    )
    

    if (
        response is None
        or response.message is None
        or not response.message.content
    ):
        raise RuntimeError(
            "El modelo no devolvió una clasificación válida."
        )
    print(
        "\n[DEBUG CLASSIFIER RAW]:",
        repr(response.message.content),
    )
    print(
        "\n[DEBUG PROMPT ALLOWED]:",
        CONTEXTUAL_EVENTS,
    )
    result = (
        response.message.content
        .strip()
        .lower()
    )

    # Limpieza mínima por si el modelo agrega formato.
    result = result.replace("`", "")
    result = result.replace('"', "")
    result = result.replace("'", "")
    result = result.strip()

    if result in VALID_EVENTS:
        if result == "activity_completed":
            return "none"
        return result

    detected_events = [
        event
        for event in VALID_EVENTS
        if event in result
    ]

    if len(detected_events) == 1:
        detected_event = detected_events[0]
        if detected_event == "activity_completed":
            return "none"
        return detected_event

    if result in CONTEXTUAL_EVENTS:
        return result
    detected_events = [
        event
        for event in CONTEXTUAL_EVENTS
        if event in result
    ]
    if len(detected_events) == 1:
        return detected_events[0]
    return "none"

    

