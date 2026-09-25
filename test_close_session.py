from services.database_service import (
    create_participant,
    create_session,
    get_session,
    close_database_session,
)


print("PRUEBA 1 - Crear sesión")

participant_id = create_participant()

session_id = create_session(
    participant_id=participant_id
)

print(
    f"Participante: {participant_id}"
)

print(
    f"Sesión: {session_id}"
)


print()
print("Estado antes del cierre:")

session_before = get_session(
    session_id
)

print(session_before)


print()
print("PRUEBA 2 - Cerrar sesión")

closed = close_database_session(
    session_id=session_id,
    duration_seconds=180,
    interaction_count=5,
    difficulty_count=2,
    final_phase="reflection",
)

print(
    f"Cierre realizado: {closed}"
)


print()
print("Estado después del cierre:")

session_after = get_session(
    session_id
)

print(session_after)


print()
print("PRUEBA 3 - Sesión inexistente")

missing = close_database_session(
    session_id="sesion-inexistente",
    duration_seconds=10,
    interaction_count=1,
    difficulty_count=0,
    final_phase="planning",
)

print(
    f"Cierre realizado: {missing}"
)
