from services.database_service import (
    get_active_participant_sessions,
)

participant_id = "P-ae22ebd8"

active_sessions = (
    get_active_participant_sessions(
        participant_id
    )
)

print(
    "\nSESIONES ACTIVAS DEL PARTICIPANTE"
)
print("=" * 50)
print(f"Total: {len(active_sessions)}")

for session in active_sessions:

    print("\n---")
    print(
        "session_id:",
        session["session_id"],
    )
    print(
        "start_time:",
        session["start_time"],
    )
    print(
        "status:",
        session["status"],
    )
    print(
        "interaction_count:",
        session["interaction_count"],
    )