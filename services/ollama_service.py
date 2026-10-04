import os
import requests
from dotenv import load_dotenv


load_dotenv()


MODEL_NAME = "@cf/meta/llama-3.2-3b-instruct"

CLOUDFLARE_API_TOKEN = os.getenv(
    "CLOUDFLARE_API_TOKEN"
)

CLOUDFLARE_ACCOUNT_ID = os.getenv(
    "CLOUDFLARE_ACCOUNT_ID"
)


def generate_response(messages, system_prompt):
    """
    Genera una respuesta utilizando
    Llama 3.2 3B Instruct mediante Cloudflare Workers AI.

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

    if not CLOUDFLARE_API_TOKEN:
        raise RuntimeError(
            "No se encontró CLOUDFLARE_API_TOKEN."
        )

    if not CLOUDFLARE_ACCOUNT_ID:
        raise RuntimeError(
            "No se encontró CLOUDFLARE_ACCOUNT_ID."
        )

    messages_for_model = [
        {
            "role": "system",
            "content": system_prompt,
        }
    ]

    messages_for_model.extend(messages)

    url = (
        "https://api.cloudflare.com/client/v4/accounts/"
        f"{CLOUDFLARE_ACCOUNT_ID}/ai/run/{MODEL_NAME}"
    )

    headers = {
        "Authorization": (
            f"Bearer {CLOUDFLARE_API_TOKEN}"
        ),
        "Content-Type": "application/json",
    }

    payload = {
        "messages": messages_for_model
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=60,
        )

        response.raise_for_status()

        response_data = response.json()

        content = (
            response_data
            .get("result", {})
            .get("response")
        )

        if not content:
            print(
                "[ERROR CLOUDFLARE] "
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
                "error_message": (
                    "El generador no devolvió contenido"
                ),
            }

        return {
            "success": True,
            "content": content,
        }

    except Exception as error:
        print(
            "[ERROR CLOUDFLARE] "
            f"No fue posible generar la respuesta: {error}"
        )

        return {
            "success": False,
            "content": (
                "En este momento no puedo generar una "
                "orientación. Intenta nuevamente en unos "
                "momentos."
            ),
            "error_type": "generation_error",
            "error_message": str(error),
        }