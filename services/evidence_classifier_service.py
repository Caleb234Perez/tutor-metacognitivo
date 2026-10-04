from services.ollama_service import generate_response

VALID_EVENTS = (
    "plan_ready",
    "difficulty_detected",
    "difficulty_resolved",
    "activity_completed",
    "none",
)


CLASSIFIER_PROMPT = """
Actúas exclusivamente como un clasificador de evidencia
lingüística para un tutor metacognitivo.

NO eres un tutor conversacional.
NO debes responder ni aconsejar al estudiante.
NO debes explicar las reglas.
NO debes explicar tu decisión.

Debes clasificar cada mensaje en exactamente UNA
de estas cinco categorías:

plan_ready
difficulty_detected
difficulty_resolved
activity_completed
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

activity_completed:
El estudiante comunica claramente que terminó
la actividad completa.

none:
No existe evidencia suficiente de alguno de los
eventos anteriores.

REGLAS

1. Si existe contraste, como "pero", "aunque" o
   "sin embargo", considera principalmente el estado
   actual expresado al final del mensaje.

2. Haber terminado solamente una parte, pregunta,
   ejercicio o paso NO significa activity_completed.

3. Una actividad ajena al aprendizaje, como comer,
   caminar o hacer ejercicio físico, NO representa
   plan_ready.

4. Una frase que niega una dificultad, como
   "no estoy confundido", debe clasificarse como none.

5. No inventes categorías.
REGLA ESTRICTA PARA activity_completed

Utiliza activity_completed únicamente cuando el mensaje
indique claramente que la actividad completa terminó.

NO utilices activity_completed cuando el estudiante:

- apenas va a comenzar;
- describe un plan o lo que hará;
- terminó solamente una parte;
- terminó una pregunta;
- terminó un ejercicio dentro de varios;
- identificó un error;
- resolvió una duda;
- comprendió algo que antes no comprendía;
- indica que continuará con otra parte.

Si existe duda entre activity_completed y otra categoría,
NO utilices activity_completed.

FORMATO DE RESPUESTA

Tu respuesta debe contener SOLAMENTE una de estas
palabras exactas:

plan_ready
difficulty_detected
difficulty_resolved
activity_completed
none

EJEMPLOS

Mensaje:
"Primero voy a revisar los datos del problema."
Respuesta:
plan_ready

Mensaje:
"No logro comprender esta parte."
Respuesta:
difficulty_detected

Mensaje:
"Antes estaba confundido, pero ahora ya lo entiendo."
Respuesta:
difficulty_resolved

Mensaje:
"Ya terminé toda la actividad."
Respuesta:
activity_completed

Mensaje:
"Terminé la primera pregunta y todavía me faltan otras."
Respuesta:
none

Mensaje:
"Voy a salir a caminar."
Respuesta:
none
Mensaje:
"Creo que empezaré identificando lo que me están pidiendo."
Respuesta:
plan_ready

Mensaje:
"Ya veo dónde estaba mi error."
Respuesta:
difficulty_resolved

Mensaje:
"Ya respondí la primera parte y ahora sigo con la segunda."
Respuesta:
none
"""


def classify_pedagogical_evidence(message):
    """
    Clasifica evidencia lingüística del mensaje del
    estudiante utilizando un modelo local mediante
    Ollama.

    La función no realiza transiciones pedagógicas,
    no modifica scaffolding y no selecciona
    estrategias.

    Devuelve un resultado estructurado que permite
    distinguir una clasificación válida de un fallo
    técnico.
    """

    if not isinstance(message, str):
        raise TypeError(
            "message debe ser una cadena de texto."
        )

    message = message.strip()

    if not message:
        return {
            "success": True,
            "event": "none",
        }

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

    try:

        response = generate_response(
            messages=[
                {
                    "role": "user",
                    "content": classification_request,
                }
            ],
            system_prompt=CLASSIFIER_PROMPT,
        )
        if (
            not response
            or not response.get("success")
            or not response.get("content")
        ):

            print(
                "[ERROR CLASSIFIER] "
                "El modelo no devolvió contenido."
            )

            return {
                "success": False,
                "event": None,
                "error_type": "empty_response",
                "error_message":(
                    "El clasificador no devolvio el contenido"
                ),
            }

        print(
            "\n[DEBUG CLASSIFIER RAW]:",
            repr(response["content"]),
        )

        result = (
            response["content"]
            .strip()
            .lower()
        )

        # Limpieza mínima por si el modelo agrega formato.
        result = result.replace("`", "")
        result = result.replace('"', "")
        result = result.replace("'", "")
        result = result.strip()

        if result in VALID_EVENTS:

            return {
                "success": True,
                "event": result,
            }

        detected_events = [
            event
            for event in VALID_EVENTS
            if event in result
        ]

        if len(detected_events) == 1:

            return {
                "success": True,
                "event": detected_events[0],
            }

        print(
            "[WARNING CLASSIFIER] "
            f"Respuesta no reconocida: {result!r}"
        )

        return {
            "success": False,
            "event": None,
            "error_type":"invalid_response",
            "error_message":(
                f"Respuesta no reconocida: {result!r}"
            ),
        }

    except Exception as error:

        print(
            "[ERROR CLASSIFIER] "
            "No fue posible clasificar el mensaje: "
            f"{error}"
        )

        return {
            "success": False,
            "event": None,
            "error_type":"classifier_error",
            "error_message": str(error),
        }




    