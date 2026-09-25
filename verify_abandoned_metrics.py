from services.database_service import (
    get_session,
)

session_id = (
    "ff4002aa-cdf1-4d7c-bb59-488e84dc3a14"
)

session = get_session(session_id)

print("\nVERIFICACIÓN DE MÉTRICAS")
print("=" * 50)

if session is None:

    print("No se encontró la sesión.")

else:

    print(
        "session_id:",
        session["session_id"],
    )

    print(
        "status:",
        session["status"],
    )

    print(
        "start_time:",
        session["start_time"],
    )

    print(
        "end_time:",
        session["end_time"],
    )

    print(
        "duration_seconds:",
        session["duration_seconds"],
    )

    print(
        "interaction_count:",
        session["interaction_count"],
    )

    print(
        "difficulty_count:",
        session["difficulty_count"],
    )

    print(
        "final_phase:",
        session["final_phase"],
    )