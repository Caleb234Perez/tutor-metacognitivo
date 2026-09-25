from services.evidence_classifier_service import (
    classify_pedagogical_evidence,
)


TEST_MESSAGES = [
    "Primero revisaré qué información me proporciona el problema.",
    "Esta parte me está haciendo bolas.",
    "Ahora entiendo mejor lo que tengo que hacer.",
    "He terminado toda la actividad.",
    "Voy a salir a caminar cuando termine.",
    "Terminé la primera pregunta, todavía me faltan las demás.",
    "Creo que entiendo, aunque todavía tengo algunas dudas.",
]


print(
    "\n=== PRUEBA INICIAL DEL CLASIFICADOR CONTEXTUAL ===\n"
)

for message in TEST_MESSAGES:

    result = classify_pedagogical_evidence(
        message
    )

    print(f"Mensaje: {message}")
    print(f"Evento:  {result}")
    print("-" * 60)