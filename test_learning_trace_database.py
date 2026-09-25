from services.database_service import (
    create_participant,
    create_session,
    get_session_traces,
)

from services.learning_trace_service import (
    save_learning_trace_to_database,
)


print("PRUEBA 1 - Crear participante y sesión")

participant_id = create_participant()

session_id = create_session(
    participant_id=participant_id
)

print(f"Participante: {participant_id}")
print(f"Sesión: {session_id}")


print()
print("PRUEBA 2 - Guardar traza mediante Learning Trace Service")

trace_id = save_learning_trace_to_database(
    session_id=session_id,
    interaction_number=1,
    student_message=(
        "No entiendo cómo hacer el ciclo."
    ),
    tutor_response=(
        "¿Qué parte del ciclo te está "
        "causando dificultad?"
    ),
    phase_before="monitoring",
    phase_after="control",
    pedagogical_event="difficulty_detected",
    metacognitive_strategy="guiding_question",
    scaffolding_level=1,
    difficulty_count=1,
)

print(
    f"Traza guardada con ID: {trace_id}"
)


print()
print("PRUEBA 3 - Recuperar trazas desde SQLite")

traces = get_session_traces(
    session_id
)

for trace in traces:
    print(trace)