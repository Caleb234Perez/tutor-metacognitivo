from services.ollama_service import (
    generate_response,
)


# ---------------------------------------------------------
# Prueba 1: generación normal
# ---------------------------------------------------------

print("PRUEBA 1 - Generación válida")

try:

    response = generate_response(
        messages=[
            {
                "role": "user",
                "content": (
                    "Estoy intentando comprender "
                    "cómo funciona un ciclo."
                ),
            }
        ],
        system_prompt=(
            "Eres un tutor universitario. "
            "Formula una pregunta breve para ayudar "
            "al estudiante a explicar su razonamiento."
        ),
    )

    print("OK - Respuesta generada.")
    print()
    print(response)

except Exception as error:

    print(
        f"ERROR inesperado: {error}"
    )


# ---------------------------------------------------------
# Prueba 2: prompt vacío
# ---------------------------------------------------------

print()
print("PRUEBA 2 - Prompt vacío")

try:

    generate_response(
        messages=[],
        system_prompt="",
    )

    print(
        "ERROR - Se aceptó un prompt vacío."
    )

except ValueError as error:

    print(
        f"OK - Error controlado: {error}"
    )


# ---------------------------------------------------------
# Prueba 3: messages inválido
# ---------------------------------------------------------

print()
print("PRUEBA 3 - Messages inválido")

try:

    generate_response(
        messages="mensaje incorrecto",
        system_prompt="Prompt válido.",
    )

    print(
        "ERROR - Se aceptó un tipo inválido."
    )

except TypeError as error:

    print(
        f"OK - Error controlado: {error}"
    )


# ---------------------------------------------------------
# Prueba 4: historial vacío válido
# ---------------------------------------------------------

print()
print("PRUEBA 4 - Historial vacío")

try:

    response = generate_response(
        messages=[],
        system_prompt=(
            "Responde únicamente con la palabra OK."
        ),
    )

    print(
        "OK - El servicio acepta historial vacío."
    )
    print(
        f"Respuesta: {response}"
    )

except Exception as error:

    print(
        f"ERROR inesperado: {error}"
    )