from services.database_service import (
    get_participant_sessions,
    get_active_participant_sessions,
)

PARTICIPANT_ID = "P-ae22ebd8"


# -----------------------------------------------------
# Todas las sesiones
# -----------------------------------------------------

sessions = get_participant_sessions(
    PARTICIPANT_ID,
    only_closed=False,
)

print("\n=== TODAS LAS SESIONES ===")

for session in sessions:

    print("\n-----------------------------")
    print(
        "ID:",
        session["session_id"],
    )
    print(
        "Inicio:",
        session["start_time"],
    )
    print(
        "Fin:",
        session["end_time"],
    )
    print(
        "Interacciones:",
        session["interaction_count"],
    )
    print(
        "Estado:",
        session["status"],
    )


# -----------------------------------------------------
# Sesiones activas
# -----------------------------------------------------

active_sessions = (
    get_active_participant_sessions(
        PARTICIPANT_ID
    )
)

print("\n=== SESIONES ACTIVAS ===")
print(
    "Total activas:",
    len(active_sessions),
)

for session in active_sessions:

    print(
        session["session_id"],
        "->",
        session["status"],
    )