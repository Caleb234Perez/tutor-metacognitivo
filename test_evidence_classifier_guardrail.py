from services.evidence_classifier_service import (
    classify_pedagogical_evidence,
)


TEST_CASES = [
    (
        "Ya terminé toda la actividad.",
        "activity_completed",
    ),
    (
        "Ya respondí todo.",
        "activity_completed",
    ),
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
    (
        "Creo que ya le agarré la idea.",
        "difficulty_resolved",
    ),
    (
        "Ya me hice bolas con esta parte y no sé por dónde seguir.",
        "difficulty_detected",
    ),
    (
        "Creo que primero debería entender qué me pide el ejercicio y luego intentar resolverlo.",
        "plan_ready",
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

print(
    "\n=== PRUEBA DEL GUARDRAIL "
    "DE FINALIZACIÓN V3.3 ===\n"
)


for index, (message, expected) in enumerate(
    TEST_CASES,
    start=1,
):

    result = classify_pedagogical_evidence(
        message
    )

    correct = result == expected

    if correct:
        passed += 1

    print(f"Prueba {index}")
    print(f"Mensaje:  {message}")
    print(f"Esperado: {expected}")
    print(f"Obtenido: {result}")
    print(
        "Resultado:",
        "OK" if correct else "FALLO",
    )
    print("-" * 60)


print("\n=== RESUMEN ===")
print(f"Correctas: {passed}")
print(
    f"Fallidas:  {len(TEST_CASES) - passed}"
)
print(f"Total:     {len(TEST_CASES)}")