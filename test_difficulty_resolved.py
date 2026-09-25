from services.evidence_classifier_service import (
    classify_pedagogical_evidence,
)


test_messages = [
    "Ahora sí entendí cómo hacerlo.",
    "Creo que ya entendí.",
    "Ya veo dónde estaba mi error.",
    "Antes no entendía esta parte, pero ahora sí.",
    "Al principio estaba confundido, pero ya lo veo más claro.",
    "Sigo sin entender cómo hacerlo.",
    "Aquí es donde me confundí.",
]


print("=== PRUEBA difficulty_resolved ===\n")

for message in test_messages:

    result = classify_pedagogical_evidence(
        message
    )

    print("Mensaje:", message)
    print("Resultado:", result)
    print("-" * 50)