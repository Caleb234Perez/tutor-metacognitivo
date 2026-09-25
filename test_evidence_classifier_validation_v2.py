from services.evidence_classifier_service import (
    classify_pedagogical_evidence,
)


VALIDATION_CASES = [
    # =========================================================
    # 1. PLANEACIÓN
    # =========================================================
    (
        "Creo que primero debería entender qué me pide el ejercicio y luego intentar resolverlo.",
        "plan_ready",
    ),
    (
        "Voy a comenzar separando los datos importantes de los que no necesito.",
        "plan_ready",
    ),
    (
        "Mi idea es leer otra vez el problema y después hacer las operaciones.",
        "plan_ready",
    ),
    (
        "Antes de responder quiero revisar paso por paso lo que hice.",
        "plan_ready",
    ),

    # =========================================================
    # 2. DIFICULTAD
    # =========================================================
    (
        "Ya me hice bolas con esta parte y no sé por dónde seguir.",
        "difficulty_detected",
    ),
    (
        "Según yo iba bien, pero ahorita ya no entiendo qué sigue.",
        "difficulty_detected",
    ),
    (
        "Me perdí cuando empezó esa parte del procedimiento.",
        "difficulty_detected",
    ),
    (
        "No estoy seguro de haber entendido lo que tengo que hacer.",
        "difficulty_detected",
    ),

    # =========================================================
    # 3. RESOLUCIÓN DE DIFICULTAD
    # =========================================================
    (
        "Ah ya, ahora sí entendí por qué estaba mal.",
        "difficulty_resolved",
    ),
    (
        "Creo que ya le agarré la idea.",
        "difficulty_resolved",
    ),
    (
        "Ya vi qué estaba haciendo mal y ahora sí puedo continuar.",
        "difficulty_resolved",
    ),
    (
        "Con esa explicación ya me queda mucho más claro.",
        "difficulty_resolved",
    ),

    # =========================================================
    # 4. FINALIZACIÓN COMPLETA
    # =========================================================
    (
        "Listo, ya terminé todo lo que me pedía la actividad.",
        "activity_completed",
    ),
    (
        "Ya acabé con todos los ejercicios y no me falta ninguno.",
        "activity_completed",
    ),
    (
        "Terminé la actividad completa.",
        "activity_completed",
    ),

    # =========================================================
    # 5. FINALIZACIÓN PARCIAL
    # =========================================================
    (
        "Ya terminé esta pregunta, pero todavía me quedan otras dos.",
        "none",
    ),
    (
        "Acabé esta parte y ahora voy con la siguiente.",
        "none",
    ),
    (
        "Ya resolví el primer ejercicio, todavía no termino los demás.",
        "none",
    ),

    # =========================================================
    # 6. MENSAJES NEUTROS
    # =========================================================
    (
        "La pregunta está redactada diferente a la anterior.",
        "none",
    ),
    (
        "Estoy pensando cuál de las opciones elegir.",
        "none",
    ),
    (
        "Creo que este tema está interesante.",
        "none",
    ),
    (
        "Cuando termine voy a jugar un rato.",
        "none",
    ),

    # =========================================================
    # 7. NEGACIONES
    # =========================================================
    (
        "No tengo problema con esta parte.",
        "none",
    ),
    (
        "No estoy perdido, solo estoy revisando mis pasos.",
        "none",
    ),
    (
        "No necesito ayuda por ahora.",
        "none",
    ),
    (
        "No diría que estoy confundido.",
        "none",
    ),

    # =========================================================
    # 8. CONTRASTES
    # =========================================================
    (
        "Pensé que no iba a poder, pero ahora ya sé cómo hacerlo.",
        "difficulty_resolved",
    ),
    (
        "Creía que ya estaba claro, pero ahora me surgió otra duda.",
        "difficulty_detected",
    ),
    (
        "Al principio no entendía nada, aunque ya lo veo más claro.",
        "difficulty_resolved",
    ),
    (
        "Ya había avanzado bastante, pero me atoré en este paso.",
        "difficulty_detected",
    ),

    # =========================================================
    # 9. COLOQUIALISMOS / LENGUAJE NATURAL
    # =========================================================
    (
        "Aquí ya me revolví.",
        "difficulty_detected",
    ),
    (
        "Ya le entendí a esta parte.",
        "difficulty_resolved",
    ),
    (
        "Creo que ya salió.",
        "difficulty_resolved",
    ),
    (
        "Ando medio perdido con esto.",
        "difficulty_detected",
    ),

    # =========================================================
    # 10. ERRORES ORTOGRÁFICOS MODERADOS
    # =========================================================
    (
        "no entiendo bien k tengo ke hacer",
        "difficulty_detected",
    ),
    (
        "ya entendi, ahora si se como seguir",
        "difficulty_resolved",
    ),
    (
        "primero voi a revisar los datos del problema",
        "plan_ready",
    ),

    # =========================================================
    # 11. AMBIGÜEDADES
    # =========================================================
    (
        "Creo que más o menos entiendo, pero todavía no estoy seguro.",
        "difficulty_detected",
    ),
    (
        "Ya terminé de revisar, aunque todavía no termino la actividad.",
        "none",
    ),
    (
        "Parece que ya quedó, pero quiero revisar antes de decir que terminé.",
        "none",
    ),
]


passed = 0
failed = 0
failed_cases = []
all_results = []

print(
    "\n=== VALIDACIÓN INÉDITA V2 "
    "DEL CLASIFICADOR CONTEXTUAL ===\n"
)

for index, (message, expected) in enumerate(
    VALIDATION_CASES,
    start=1,
):

    result = classify_pedagogical_evidence(message)
    all_results.append(
        {
            "expected":expected,
            "obtained": result,
        }
    )
    correct = result == expected

    if correct:
        passed += 1
        status = "OK"
    else:
        failed += 1
        status = "FALLO"

        failed_cases.append(
            {
                "number": index,
                "message": message,
                "expected": expected,
                "obtained": result,
            }
        )

    print(f"Prueba {index}")
    print(f"Mensaje:  {message}")
    print(f"Esperado: {expected}")
    print(f"Obtenido: {result}")
    print(f"Resultado: {status}")
    print("-" * 60)


total = len(VALIDATION_CASES)

percentage = (
    (passed / total) * 100
    if total > 0
    else 0
)

print("\n=== RESUMEN DE VALIDACIÓN ===")
print(f"Correctas: {passed}")
print(f"Fallidas:  {failed}")
print(f"Total:     {total}")
print(f"Resultado: {percentage:.2f} %")


if failed_cases:

    print("\n=== CASOS FALLIDOS ===")

    for case in failed_cases:

        print(f"\nPrueba {case['number']}")
        print(f"Mensaje:  {case['message']}")
        print(f"Esperado: {case['expected']}")
        print(f"Obtenido: {case['obtained']}")

else:

    print(
        "\nNo se registraron fallos "
        "en esta batería inédita."
    )
# =========================================================
# ANÁLISIS POR CATEGORÍA
# =========================================================

CATEGORIES = [
    "plan_ready",
    "difficulty_detected",
    "difficulty_resolved",
    "activity_completed",
    "none",
]


print("\n=== DESEMPEÑO POR CATEGORÍA ===")

for category in CATEGORIES:

    category_cases = [
        item
        for item in all_results
        if item["expected"] == category
    ]

    category_correct = sum(
        1
        for item in category_cases
        if item["obtained"] == category
    )

    category_total = len(category_cases)

    category_accuracy = (
        (category_correct / category_total) * 100
        if category_total > 0
        else 0
    )

    print(
        f"{category:22} "
        f"{category_correct}/{category_total} "
        f"({category_accuracy:.2f} %)"
    )


# =========================================================
# MATRIZ DE CONFUSIÓN
# =========================================================

print("\n=== MATRIZ DE CONFUSIÓN ===")
print("Filas = esperado")
print("Columnas = obtenido\n")

header = "Esperado".ljust(22)

for category in CATEGORIES:
    header += category[:10].rjust(12)

print(header)
print("-" * len(header))


for expected_category in CATEGORIES:

    row = expected_category.ljust(22)

    for obtained_category in CATEGORIES:

        count = sum(
            1
            for item in all_results
            if (
                item["expected"] == expected_category
                and item["obtained"] == obtained_category
            )
        )

        row += str(count).rjust(12)

    print(row)


# =========================================================
# FALSOS POSITIVOS POR EVENTO
# =========================================================

print("\n=== FALSOS POSITIVOS POR EVENTO ===")

for category in CATEGORIES:

    false_positives = sum(
        1
        for item in all_results
        if (
            item["obtained"] == category
            and item["expected"] != category
        )
    )

    print(
        f"{category:22} "
        f"{false_positives}"
    )