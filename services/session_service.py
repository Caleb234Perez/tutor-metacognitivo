from datetime import datetime
from pathlib import Path
import csv
from services.database_service import (
    create_session,
    close_database_session,
)


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
SESSION_FILE = DATA_DIR / "session_summaries.csv"

DATA_DIR.mkdir(parents=True, exist_ok=True)


SESSION_FIELDS = [
    "session_id",
    "start_time",
    "end_time",
    "duration_seconds",
    "interaction_count",
    "difficulty_count",
    "final_phase",
    "status",
]


def initialize_session(session_id):
    """
    Crea el estado inicial de una sesión.
    """

    return {
        "session_id": session_id,
        "start_time": datetime.now(),
        "end_time": None,
        "status": "active",
    }


def close_session(session_state):
    """
    Finaliza una sesión activa.
    """

    if session_state["status"] == "closed":
        return session_state

    session_state["end_time"] = datetime.now()
    session_state["status"] = "closed"

    return session_state


def get_session_duration_seconds(session_state):
    """
    Calcula la duración de la sesión en segundos.
    """

    start_time = session_state["start_time"]

    if session_state["end_time"] is not None:
        end_time = session_state["end_time"]
    else:
        end_time = datetime.now()

    return int(
        (end_time - start_time).total_seconds()
    )


def save_session_summary(
    session_state,
    interaction_count,
    difficulty_count,
    final_phase,
):
    """
    Guarda el resumen final de una sesión.
    """

    file_exists = SESSION_FILE.exists()

    duration = get_session_duration_seconds(
        session_state
    )

    summary = {
        "session_id": session_state["session_id"],
        "start_time": session_state[
            "start_time"
        ].isoformat(timespec="seconds"),
        "end_time": session_state[
            "end_time"
        ].isoformat(timespec="seconds"),
        "duration_seconds": duration,
        "interaction_count": interaction_count,
        "difficulty_count": difficulty_count,
        "final_phase": final_phase,
        "status": session_state["status"],
    }

    with SESSION_FILE.open(
        "a",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=SESSION_FIELDS,
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow(summary)

    return summary

def initialize_database_session(
    participant_id,
    session_id,
):
    """
    Registra en SQLite una nueva sesión asociada
    a un participante ya existente.
    """

    return create_session(
        participant_id=participant_id,
        session_id=session_id,
    )


def save_database_session_summary(
    session_state,
    interaction_count,
    difficulty_count,
    final_phase,
):
    """
    Actualiza en SQLite el estado final de una sesión.
    """

    duration = get_session_duration_seconds(
        session_state
    )

    return close_database_session(
        session_id=session_state["session_id"],
        duration_seconds=duration,
        interaction_count=interaction_count,
        difficulty_count=difficulty_count,
        final_phase=final_phase,
    )