from pedagogy.evidence_detector import detect_pedagogical_event


TEST_CASES = [
    # Planeación clara
    (
        "Primero voy a leer el problema y después voy a resolverlo.",
        "plan_ready",
    ),
    (
        "Mi plan es revisar las instrucciones antes de comenzar.",
        "plan_ready",
    ),

    # Dificultad explícita
    (
        "No entiendo esta parte.",
        "difficulty_detected",
    ),
    (
        "Me cuesta comprender el ejercicio.",
        "difficulty_detected",
    ),
    (
        "Sigo sin poder resolverlo.",
        "difficulty_detected",
    ),

    # Dificultad resuelta
    (
        "Ya entendí cómo hacerlo.",
        "difficulty_resolved",
    ),
    (
        "Creo que ya entendí el procedimiento.",
        "difficulty_resolved",
    ),

    # Actividad terminada
    (
        "Ya terminé la actividad.",
        "activity_completed",
    ),
    (
        "Ya finalicé.",
        "activity_completed",
    ),

    # Mensajes neutros
    (
        "La actividad me parece interesante.",
        "none",
    ),
    (
        "Estoy leyendo el ejercicio.",
        "none",
    ),
    (
        "Creo que la respuesta podría ser cinco.",
        "none",
    ),

    # Casos ambiguos / potenciales falsos positivos
    (
        "Voy a comer después de terminar esto.",
        "none",
    ),
    (
        "No puedo creer que ya entendí.",
        "difficulty_resolved",
    ),
    (
        "Ya terminé de leer, pero no entiendo el problema.",
        "difficulty_detected",
    ),
    (
        "Creo que ya entendí, pero todavía no me queda claro.",
        "difficulty_detected",
    ),
        # Contraste: dificultad -> resolución
    (
        "No entendía esta parte, pero ya lo resolví.",
        "difficulty_resolved",
    ),
    (
        "Al principio no podía hacerlo, pero ya pude.",
        "difficulty_resolved",
    ),

    # Contraste: resolución -> dificultad
    (
        "Pensé que ya entendía, pero sigo sin comprender.",
        "difficulty_detected",
    ),
    (
        "Ya pude avanzar, pero todavía no entiendo esta parte.",
        "difficulty_detected",
    ),

    # Finalización parcial
    (
        "Ya terminé de leer las instrucciones.",
        "none",
    ),
    (
        "Ya acabé el primer ejercicio, ahora sigo con el segundo.",
        "none",
    ),

    # Finalización real
    (
        "Ya terminé toda la actividad.",
        "activity_completed",
    ),
    (
        "Ya finalicé el ejercicio completo.",
        "activity_completed",
    ),

    # Planes no pedagógicos
    (
        "Voy a tomar agua.",
        "none",
    ),
    (
        "Después voy a comer.",
        "none",
    ),
    (
        "Pienso hacer ejercicio en la tarde.",
        "none",
    ),

    # Planes pedagógicos
    (
        "Voy a revisar el problema paso por paso.",
        "plan_ready",
    ),
    (
        "Primero voy a identificar los datos del ejercicio.",
        "plan_ready",
    ),
    (
        "Pienso hacer un esquema antes de responder.",
        "plan_ready",
    ),

    # Negaciones y expresiones que pueden confundir
    (
        "No tengo dificultad con esta parte.",
        "none",
    ),
    (
        "No necesito más ayuda.",
        "none",
    ),
    (
        "No puedo decir que sea difícil.",
        "none",
    ),

    # Lenguaje natural equivalente no contemplado
    (
        "Esto no tiene sentido para mí.",
        "difficulty_detected",
    ),
    (
        "Estoy perdido con este ejercicio.",
        "difficulty_detected",
    ),
    (
        "Ahora sí me quedó claro.",
        "difficulty_resolved",
    ),
]


passed = 0
failed = 0

print("\n=== PRUEBAS DEL DETECTOR DE EVIDENCIAS ===\n")

for index, (message, expected) in enumerate(TEST_CASES, start=1):

    result = detect_pedagogical_event(message)

    correct = result == expected

    if correct:
        passed += 1
        status = "OK"
    else:
        failed += 1
        status = "FALLO"

    print(f"Prueba {index}")
    print(f"Mensaje:  {message}")
    print(f"Esperado: {expected}")
    print(f"Obtenido: {result}")
    print(f"Resultado: {status}")
    print("-" * 60)


print("\n=== RESUMEN ===")
print(f"Correctas: {passed}")
print(f"Fallidas:  {failed}")
print(f"Total:     {len(TEST_CASES)}")