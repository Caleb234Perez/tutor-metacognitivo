from services.learning_trace_service import (
    save_learning_trace,
)


trace = save_learning_trace(
    session_id="test-session-learning-trace",
    interaction_number=1,
    student_message="No entiendo cómo continuar.",
    tutor_response=(
        "¿Qué parte del procedimiento "
        "te está causando más dificultad?"
    ),
    phase_before="monitoring",
    phase_after="control",
    pedagogical_event="difficulty_detected",
    metacognitive_strategy="guiding_question",
    scaffolding_level=1,
    difficulty_count=1,
)


print("Traza guardada correctamente.")
print()

for key, value in trace.items():
    print(
        f"{key}: {value}"
    )