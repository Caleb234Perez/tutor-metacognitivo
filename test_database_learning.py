import sqlite3

from services.database_service import (
    create_participant,
    create_session,
    save_database_trace,
    get_session_traces,
)


# ---------------------------------------------------------
# PRUEBA 1 - Preparar participante y sesión
# ---------------------------------------------------------

print("PRUEBA 1 - Crear participante y sesión")

participant_id = create_participant()

session_id = create_session(
    participant_id=participant_id
)

print(f"Participante: {participant_id}")
print(f"Sesión: {session_id}")


# ---------------------------------------------------------
# PRUEBA 2 - Guardar primera traza
# ---------------------------------------------------------

print()
print("PRUEBA 2 - Guardar learning trace")

trace_id = save_database_trace(
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
    f"Traza creada con ID: {trace_id}"
)


# ---------------------------------------------------------
# PRUEBA 3 - Guardar segunda traza
# ---------------------------------------------------------

print()
print("PRUEBA 3 - Guardar segunda learning trace")

second_trace_id = save_database_trace(
    session_id=session_id,
    interaction_number=2,
    student_message=(
        "Sigo sin entender cómo hacerlo."
    ),
    tutor_response=(
        "Piensa en la condición que determina "
        "si el ciclo debe continuar."
    ),
    phase_before="control",
    phase_after="control",
    pedagogical_event="difficulty_detected",
    metacognitive_strategy="conceptual_hint",
    scaffolding_level=2,
    difficulty_count=2,
)

print(
    f"Traza creada con ID: {second_trace_id}"
)


# ---------------------------------------------------------
# PRUEBA 4 - Recuperar trazas
# ---------------------------------------------------------

print()
print("PRUEBA 4 - Recuperar trazas")

traces = get_session_traces(
    session_id
)

for trace in traces:

    print()
    print(trace)


# ---------------------------------------------------------
# PRUEBA 5 - Sesión inexistente
# ---------------------------------------------------------

print()
print("PRUEBA 5 - Recuperar sesión inexistente")

missing = get_session_traces(
    "sesion-inexistente"
)

print(
    f"Resultado: {missing}"
)


# ---------------------------------------------------------
# PRUEBA 6 - Comprobar clave foránea
# ---------------------------------------------------------

print()
print("PRUEBA 6 - Traza con sesión inexistente")

try:

    save_database_trace(
        session_id="sesion-inexistente",
        interaction_number=1,
        student_message="Mensaje",
        tutor_response="Respuesta",
        phase_before="planning",
        phase_after="monitoring",
        pedagogical_event="plan_ready",
        metacognitive_strategy="comprehension_check",
        scaffolding_level=1,
        difficulty_count=0,
    )

    print(
        "ERROR - Se permitió guardar la traza."
    )

except sqlite3.IntegrityError as error:

    print(
        "OK - SQLite rechazó la traza."
    )

    print(
        f"Motivo: {error}"
    )
    # ---------------------------------------------------------
# PRUEBA 7 - Interacción duplicada
# ---------------------------------------------------------

print()
print("PRUEBA 7 - Interacción duplicada")

try:

    save_database_trace(
        session_id=session_id,
        interaction_number=1,
        student_message="Mensaje duplicado",
        tutor_response="Respuesta duplicada",
        phase_before="control",
        phase_after="control",
        pedagogical_event="difficulty_detected",
        metacognitive_strategy="guiding_question",
        scaffolding_level=1,
        difficulty_count=1,
    )

    print(
        "ERROR - Se permitió duplicar "
        "interaction_number."
    )

except sqlite3.IntegrityError as error:

    print(
        "OK - SQLite rechazó la interacción duplicada."
    )

    print(
        f"Motivo: {error}"
    )