from pedagogy.prompt_manager import (
    build_system_prompt,
)


# ---------------------------------------------------------
# Prueba 1: combinación válida
# ---------------------------------------------------------

print("PRUEBA 1 - Prompt válido")

try:

    prompt = build_system_prompt(
        phase="control",
        scaffolding_level=2,
        strategy="conceptual_hint",
    )

    print("OK - Prompt construido correctamente.")
    print(
        f"Longitud: {len(prompt)} caracteres"
    )

except Exception as error:

    print(
        f"ERROR inesperado: {error}"
    )


# ---------------------------------------------------------
# Prueba 2: fase inexistente
# ---------------------------------------------------------

print()
print("PRUEBA 2 - Fase inválida")

try:

    build_system_prompt(
        phase="fase_inexistente",
        scaffolding_level=1,
        strategy="goal_setting",
    )

    print(
        "ERROR - La fase inválida fue aceptada."
    )

except ValueError as error:

    print(
        f"OK - Error controlado: {error}"
    )


# ---------------------------------------------------------
# Prueba 3: estrategia inexistente
# ---------------------------------------------------------

print()
print("PRUEBA 3 - Estrategia inválida")

try:

    build_system_prompt(
        phase="monitoring",
        scaffolding_level=1,
        strategy="estrategia_inexistente",
    )

    print(
        "ERROR - La estrategia inválida fue aceptada."
    )

except ValueError as error:

    print(
        f"OK - Error controlado: {error}"
    )


# ---------------------------------------------------------
# Prueba 4: compatibilidad sin estrategia
# ---------------------------------------------------------

print()
print("PRUEBA 4 - Prompt sin estrategia")

try:

    prompt = build_system_prompt(
        phase="planning",
        scaffolding_level=1,
    )

    print(
        "OK - Prompt construido sin estrategia."
    )

except Exception as error:

    print(
        f"ERROR inesperado: {error}"
    )