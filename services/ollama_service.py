from ollama import chat


MODEL_NAME = "llama3.2:3b"


def generate_response(messages, system_prompt):
    """
    Genera una respuesta utilizando el modelo local
    ejecutado mediante Ollama.

    Devuelve un diccionario con:
    - success: indica si la generación fue correcta.
    - content: texto que se mostrará al usuario.
    """

    if not system_prompt:
        raise ValueError(
            "El system_prompt no puede estar vacío."
        )

    if not isinstance(messages, list):
        raise TypeError(
            "messages debe ser una lista."
        )

    messages_for_model = [
        {
            "role": "system",
            "content": system_prompt,
        }
    ]

    messages_for_model.extend(messages)

    try:
        response = chat(
            model=MODEL_NAME,
            messages=messages_for_model,
        )

        if (
            response is None
            or response.message is None
            or not response.message.content
        ):
            print(
                "[ERROR OLLAMA] "
                "El modelo no devolvió una respuesta válida."
            )

            return {
                "success": False,
                "content": (
                    "En este momento no puedo generar una "
                    "orientación. Intenta nuevamente en unos "
                    "momentos."
                ),
                "error_type": "empty_response",
                "error_message":(
                    "El generador no devolvio contenido"
                ),
            }

        return {
            "success": True,
            "content": response.message.content,
        }

    except Exception as error:
        print(
            "[ERROR OLLAMA] "
            f"No fue posible generar la respuesta: {error}"
        )

        return {
            "success": False,
            "content": (
                "En este momento no puedo generar una "
                "orientación. Intenta nuevamente en unos "
                "momentos."
            ),
            "error_type":"generation_error",
            "error_message": str(error),
        }