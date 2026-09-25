#from pedagogy.evidence_detector import detect_pedagogical_event
from services.evidence_classifier_service import (
    classify_pedagogical_evidence,
)

VALIDATION_CASES = [
    # =========================================================
    # 1. PLANEACIÓN
    # =========================================================
    (
        "Primero revisaré qué información me proporciona el problema.",
        "plan_ready",
    ),
    (
        "Creo que empezaré identificando lo que me están pidiendo.",
        "plan_ready",
    ),
    (
        "Antes de responder voy a analizar los datos.",
        "plan_ready",
    ),
    (
        "Mi plan es leer cada pregunta con cuidado.",
        "plan_ready",
    ),

    # =========================================================
    # 2. DIFICULTAD
    # =========================================================
    (
        "Esta parte me está haciendo bolas.",
        "difficulty_detected",
    ),
    (
        "No logro resolver esta pregunta.",
        "difficulty_detected",
    ),
    (
        "Me confundí con el procedimiento.",
        "difficulty_detected",
    ),
    (
        "No sé qué hacer después de este paso.",
        "difficulty_detected",
    ),

    # =========================================================
    # 3. DIFICULTAD RESUELTA
    # =========================================================
    (
        "Ahora entiendo mejor lo que tengo que hacer.",
        "difficulty_resolved",
    ),
    (
        "Ya veo dónde estaba mi error.",
        "difficulty_resolved",
    ),
    (
        "Creo que ahora sí lo comprendí.",
        "difficulty_resolved",
    ),
    (
        "Eso aclara mi duda.",
        "difficulty_resolved",
    ),

    # =========================================================
    # 4. FINALIZACIÓN COMPLETA
    # =========================================================
    (
        "He terminado toda la actividad.",
        "activity_completed",
    ),
    (
        "Listo, completé todos los ejercicios.",
        "activity_completed",
    ),
    (
        "Ya respondí todo.",
        "activity_completed",
    ),

    # =========================================================
    # 5. MENSAJES NEUTROS
    # =========================================================
    (
        "Estoy pensando en la respuesta.",
        "none",
    ),
    (
        "La segunda pregunta parece diferente.",
        "none",
    ),
    (
        "Voy a salir a caminar cuando termine.",
        "none",
    ),
    (
        "Me gusta este tema.",
        "none",
    ),

    # =========================================================
    # 6. CONTRASTES
    # =========================================================
    (
        "Al principio estaba confundido, pero ahora lo entiendo.",
        "difficulty_resolved",
    ),
    (
        "Creí que lo había entendido, pero sigo atorado.",
        "difficulty_detected",
    ),
    (
        "Ya había avanzado, pero ahora no sé cómo continuar.",
        "difficulty_detected",
    ),
    (
        "No podía resolverlo, pero finalmente ya pude.",
        "difficulty_resolved",
    ),

    # =========================================================
    # 7. NEGACIONES
    # =========================================================
    (
        "No estoy confundido con este ejercicio.",
        "none",
    ),
    (
        "Esta parte no me cuesta.",
        "none",
    ),
    (
        "No tengo problemas para entenderlo.",
        "none",
    ),

    # =========================================================
    # 8. FINALIZACIÓN PARCIAL
    # =========================================================
    (
        "Terminé la primera pregunta, todavía me faltan las demás.",
        "none",
    ),
    (
        "Ya respondí la primera parte y ahora sigo con la segunda.",
        "none",
    ),

    # =========================================================
    # 9. CASOS AMBIGUOS
    # =========================================================
    (
        "Creo que entiendo, aunque todavía tengo algunas dudas.",
        "difficulty_detected",
    ),
    (
        "No estaba seguro al principio, pero ahora sí me queda claro.",
        "difficulty_resolved",
    ),
]


passed = 0
failed = 0
failed_cases = []

print(
    "\n=== VALIDACIÓN INDEPENDIENTE "
    "DEL DETECTOR DE EVIDENCIAS ===\n"
)

for index, (message, expected) in enumerate(
    VALIDATION_CASES,
    start=1,
):

    result = classify_pedagogical_evidence(message)
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
        "en esta batería de validación."
    )