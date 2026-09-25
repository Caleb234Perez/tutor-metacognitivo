import json

from ollama import chat


MODEL_NAME = "llama3.2:3b"

VALID_EVENTS = (
    "plan_ready",
    "difficulty_detected",
    "difficulty_resolved",
    "activity_completed",
    "none",
)


EVIDENCE_PROMPT = """
Actúas exclusivamente como analizador de evidencia
lingüística para un tutor metacognitivo.

NO eres el tutor.
NO debes responder al estudiante.
NO debes decidir una fase metacognitiva.
NO debes decidir una estrategia pedagógica.
NO debes modificar scaffolding.
NO debes decidir si la actividad está completa.

La finalización completa se evalúa mediante otro
componente determinístico.

Tu única tarea es identificar tres tipos de evidencia:

1. plan_evidence
   true únicamente cuando el estudiante expresa una
   intención o plan concreto relacionado con la actividad
   de aprendizaje.

2. difficulty_evidence
   true cuando el estudiante expresa una dificultad
   ACTUAL: confusión, duda, bloqueo, falta de comprensión
   o incapacidad para continuar.

3. resolved_evidence
   true cuando el estudiante comunica que una dificultad
   previa fue superada o que ahora comprende aquello que
   antes no comprendía.

REGLAS IMPORTANTES

- Una acción ya completada no representa necesariamente
  resolved_evidence.

- Resolver una pregunta o ejercicio no significa por sí
  mismo que una dificultad metacognitiva fue resuelta.

- difficulty_evidence solamente representa una dificultad
  actual, no una dificultad pasada que ya fue superada.

- Expresiones coloquiales pueden representar evidencia.
  No dependas de palabras exactas.

- Una posibilidad, hipótesis o frase condicional no debe
  convertirse automáticamente en dificultad.

- plan_evidence requiere una acción intencional concreta
  relacionada con la tarea de aprendizaje.

- Revisar simplemente si una actividad ya terminó no
  representa necesariamente plan_evidence.

Devuelve exclusivamente un objeto JSON con esta estructura:

{
  "plan_evidence": false,
  "difficulty_evidence": false,
  "resolved_evidence": false
}

Los únicos valores permitidos son true o false.
No agregues explicaciones.
"""


def select_relevant_clause(text):
    """
    Cuando existe un contraste, prioriza la proposición
    que representa el estado más reciente comunicado
    por el estudiante.
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

            for part in reversed(parts):

                part = part.strip()

                if part:
                    relevant_text = part
                    break

    return relevant_text


def validate_activity_completion(message):
    """
    Valida de forma conservadora si existe evidencia
    explícita de finalización completa.
    """

    text = message.lower().strip()

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


def analyze_contextual_evidence(message):
    """
    Utiliza el modelo local únicamente para identificar
    evidencias lingüísticas, sin producir directamente
    un evento pedagógico.
    """

    relevant_text = select_relevant_clause(
        message.lower().strip()
    )

    request = f"""
Analiza exclusivamente el siguiente mensaje:

<mensaje>
{relevant_text}
</mensaje>

Devuelve únicamente el objeto JSON solicitado.
"""

    messages = [
        {
            "role": "system",
            "content": EVIDENCE_PROMPT,
        },
        {
            "role": "user",
            "content": request,
        },
    ]

    response = chat(
        model=MODEL_NAME,
        messages=messages,
        format="json",
        options={
            "temperature": 0,
        },
    )

    if (
        response is None
        or response.message is None
        or not response.message.content
    ):
        return {
            "plan_evidence": False,
            "difficulty_evidence": False,
            "resolved_evidence": False,
        }

    raw_result = response.message.content.strip()

    print(
        "\n[DEBUG EVIDENCE RAW]:",
        repr(raw_result),
    )

    try:
        parsed = json.loads(raw_result)

    except json.JSONDecodeError:

        return {
            "plan_evidence": False,
            "difficulty_evidence": False,
            "resolved_evidence": False,
        }

    evidence = {
        "plan_evidence": (
            parsed.get("plan_evidence") is True
        ),
        "difficulty_evidence": (
            parsed.get("difficulty_evidence") is True
        ),
        "resolved_evidence": (
            parsed.get("resolved_evidence") is True
        ),
    }

    print(
        "[DEBUG EVIDENCE PARSED]:",
        evidence,
    )

    return evidence


def resolve_contextual_event(evidence):
    """
    Convierte las evidencias detectadas en un único evento
    mediante reglas determinísticas.

    El LLM identifica significado lingüístico.
    Python decide qué evento representa esa evidencia.
    """

    if evidence["difficulty_evidence"]:
        return "difficulty_detected"

    if evidence["resolved_evidence"]:
        return "difficulty_resolved"

    if evidence["plan_evidence"]:
        return "plan_ready"

    return "none"


def classify_pedagogical_evidence(message):
    """
    Clasifica el mensaje mediante una arquitectura híbrida:

    1. Finalización completa mediante regla determinística.
    2. Evidencias semánticas mediante LLM.
    3. Conversión de evidencias a evento mediante reglas.

    No modifica el estado del Motor Pedagógico.
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

    evidence = analyze_contextual_evidence(
        message
    )

    return resolve_contextual_event(
        evidence
    )