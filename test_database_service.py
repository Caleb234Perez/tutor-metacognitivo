import sqlite3

from services.database_service import (
    create_participant,
    create_session,
    get_session,
)


# ---------------------------------------------------------
# PRUEBA 1 - Crear participante y sesión
# ---------------------------------------------------------

print("PRUEBA 1 - Crear participante y sesión")

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


# ---------------------------------------------------------
# PRUEBA 2 - Recuperar sesión
# ---------------------------------------------------------

print()
print("PRUEBA 2 - Recuperar sesión")

session = get_session(
    session_id
)

print(session)


# ---------------------------------------------------------
# PRUEBA 3 - Sesión inexistente
# ---------------------------------------------------------

print()
print("PRUEBA 3 - Sesión inexistente")

missing_session = get_session(
    "sesion-inexistente"
)

print(
    f"Resultado: {missing_session}"
)


# ---------------------------------------------------------
# PRUEBA 4 - Clave foránea
# ---------------------------------------------------------

print()
print("PRUEBA 4 - Participante inexistente")

try:

    create_session(
        participant_id="P-INEXISTENTE"
    )

    print(
        "ERROR - Se permitió crear la sesión."
    )

except sqlite3.IntegrityError as error:

    print(
        "OK - SQLite rechazó la sesión."
    )

    print(
        f"Motivo: {error}"
    )