import csv
import os
from datetime import datetime
from services.database_service import (
    save_database_trace,
)

DATA_DIRECTORY = "data"
TRACE_FILE = os.path.join(
    DATA_DIRECTORY,
    "learning_traces.csv",
)


FIELDNAMES = [
    "timestamp",
    "session_id",
    "interaction_number",
    "activity_id",
    "student_message",
    "tutor_response",
    "phase_before",
    "phase_after",
    "pedagogical_event",
    "metacognitive_strategy",
    "scaffolding_level",
    "difficulty_count",
]


def migrate_trace_storage():
    """
    Actualiza el archivo de trazas cuando aparecen
    nuevos campos en FIELDNAMES.

    Conserva las trazas existentes y agrega valores
    vacíos para las columnas que todavía no existían.
    """

    if not os.path.exists(TRACE_FILE):
        return

    with open(
        TRACE_FILE,
        "r",
        newline="",
        encoding="utf-8",
    ) as file:

        reader = csv.DictReader(file)

        existing_fieldnames = (
            reader.fieldnames or []
        )

        # Si el encabezado ya está actualizado,
        # no es necesario hacer nada.
        if existing_fieldnames == FIELDNAMES:
            return

        rows = list(reader)

    migrated_rows = []

    for row in rows:

        migrated_row = {}

        for field in FIELDNAMES:

            migrated_row[field] = row.get(
                field,
                "",
            )

        migrated_rows.append(
            migrated_row
        )

    with open(
        TRACE_FILE,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=FIELDNAMES,
        )

        writer.writeheader()

        writer.writerows(
            migrated_rows
        )


def initialize_trace_storage():
    """
    Crea el directorio y el archivo de trazas
    cuando todavía no existen.

    Si el archivo ya existe, verifica que su
    estructura corresponda con FIELDNAMES.
    """

    os.makedirs(
        DATA_DIRECTORY,
        exist_ok=True,
    )

    if not os.path.exists(TRACE_FILE):

        with open(
            TRACE_FILE,
            "w",
            newline="",
            encoding="utf-8",
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=FIELDNAMES,
            )

            writer.writeheader()

    else:

        migrate_trace_storage()


def save_learning_trace(
    session_id,
    interaction_number,
    activity_id,
    student_message,
    tutor_response,
    phase_before,
    phase_after,
    pedagogical_event,
    metacognitive_strategy,
    scaffolding_level,
    difficulty_count,
):
    """
    Guarda una interacción como traza de aprendizaje.
    """

    initialize_trace_storage()

    trace = {
        "timestamp": datetime.now().isoformat(
            timespec="seconds"
        ),
        "session_id": session_id,
        "interaction_number": interaction_number,
        "activity_id": activity_id,
        "student_message": student_message,
        "tutor_response": tutor_response,
        "phase_before": phase_before,
        "phase_after": phase_after,
        "pedagogical_event": pedagogical_event,
        "metacognitive_strategy": (
            metacognitive_strategy
        ),
        "scaffolding_level": (
            scaffolding_level
        ),
        "difficulty_count": (
            difficulty_count
        ),
    }

    with open(
        TRACE_FILE,
        "a",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=FIELDNAMES,
        )

        writer.writerow(trace)

    return trace
def save_learning_trace_to_database(
    session_id,
    interaction_number,
    student_message,
    tutor_response,
    phase_before,
    phase_after,
    pedagogical_event,
    metacognitive_strategy,
    scaffolding_level,
    difficulty_count,
):
    """
    Guarda una learning trace en SQLite.
    """

    return save_database_trace(
        session_id=session_id,
        interaction_number=interaction_number,
        student_message=student_message,
        tutor_response=tutor_response,
        phase_before=phase_before,
        phase_after=phase_after,
        pedagogical_event=pedagogical_event,
        metacognitive_strategy=metacognitive_strategy,
        scaffolding_level=scaffolding_level,
        difficulty_count=difficulty_count,
    )