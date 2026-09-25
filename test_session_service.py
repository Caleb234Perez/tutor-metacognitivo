from services.database_service import (
    create_participant,
    get_session,
)

from services.session_service import (
    initialize_session,
    initialize_database_session,
    close_session,
    save_database_session_summary,
)


print("PRUEBA 1 - Crear participante")

participant_id = create_participant()

print(
    f"Participante: {participant_id}"
)


print()
print("PRUEBA 2 - Crear estado de sesión")

session_id = "session-service-test"

session_state = initialize_session(
    session_id
)

print(session_state)


print()
print("PRUEBA 3 - Registrar sesión en SQLite")

initialize_database_session(
    participant_id=participant_id,
    session_id=session_id,
)

database_session = get_session(
    session_id
)

print(database_session)


print()
print("PRUEBA 4 - Cerrar sesión")

session_state = close_session(
    session_state
)

closed = save_database_session_summary(
    session_state=session_state,
    interaction_count=3,
    difficulty_count=1,
    final_phase="reflection",
)

print(
    f"Cierre en SQLite: {closed}"
)


print()
print("PRUEBA 5 - Recuperar sesión cerrada")

database_session = get_session(
    session_id
)

print(database_session)