import os
import sqlite3
from datetime import datetime
import uuid

DATA_DIRECTORY = "data"

DATABASE_FILE = os.path.join(
    DATA_DIRECTORY,
    "tutor_metacognitivo.db",
)


def get_connection():
    """
    Crea y devuelve una conexión a la base de datos SQLite.

    Las claves foráneas se activan explícitamente porque
    SQLite no las aplica por defecto en cada conexión.
    """

    os.makedirs(
        DATA_DIRECTORY,
        exist_ok=True,
    )

    connection = sqlite3.connect(
        DATABASE_FILE
    )

    connection.execute(
        "PRAGMA foreign_keys = ON;"
    )

    return connection


def initialize_database():
    """
    Inicializa la base de datos del prototipo y crea
    las tablas necesarias cuando todavía no existen.
    """

    connection = get_connection()

    try:

        cursor = connection.cursor()

        # -------------------------------------------------
        # Tabla de participantes
        # -------------------------------------------------

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS participants (
                participant_id TEXT PRIMARY KEY,
                created_at TEXT NOT NULL
            );
            """
        )

        # -------------------------------------------------
        # Tabla de sesiones
        # -------------------------------------------------

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                participant_id TEXT NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT,
                duration_seconds INTEGER,
                interaction_count INTEGER DEFAULT 0,
                difficulty_count INTEGER DEFAULT 0,
                final_phase TEXT,
                status TEXT NOT NULL,

                FOREIGN KEY (participant_id)
                    REFERENCES participants(participant_id)
            );
            """
        )

        # -------------------------------------------------
        # Tabla de learning traces
        # -------------------------------------------------

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS learning_traces (
                trace_id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                interaction_number INTEGER NOT NULL,
                student_message TEXT NOT NULL,
                tutor_response TEXT NOT NULL,
                phase_before TEXT NOT NULL,
                phase_after TEXT NOT NULL,
                pedagogical_event TEXT NOT NULL,
                metacognitive_strategy TEXT NOT NULL,
                scaffolding_level INTEGER NOT NULL,
                difficulty_count INTEGER NOT NULL,

                FOREIGN KEY (session_id)
                    REFERENCES sessions(session_id),

                UNIQUE (
                    session_id,
                    interaction_number
                )
            );
            """
        )

        cursor.execute(
            "PRAGMA table_info(learning_traces);"
        )

        learning_trace_columns = {
            row[1]
            for row in cursor.fetchall()
        }

        if "activity_id" not in learning_trace_columns:
            cursor.execute(
                """
                ALTER TABLE learning_traces
                ADD COLUMN activity_id TEXT;
                """
            )

        # -------------------------------------------------
# Tabla de eventos técnicos
# -------------------------------------------------

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS technical_events (
                technical_event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                session_id TEXT,
                participant_id TEXT,
                component TEXT NOT NULL,
                error_type TEXT NOT NULL,
                error_message TEXT,
                FOREIGN KEY (session_id)
                    REFERENCES sessions(session_id),
                FOREIGN KEY (participant_id)
                    REFERENCES participants(participant_id)
            );
            """
        )
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS participant_consents (
                consent_id INTEGER PRIMARY KEY AUTOINCREMENT,
                participant_id TEXT NOT NULL,
                consent_version TEXT NOT NULL,
                consent_given INTEGER NOT NULL,
                consent_timestamp TEXT NOT NULL,
                FOREIGN KEY (participant_id)
                    REFERENCES participants(participant_id)
            )
        """)

        connection.commit()

    finally:

        connection.close()
def create_participant():
    """
    Crea un nuevo participante utilizando un identificador
    pseudonimizado generado automáticamente.
    """

    initialize_database()

    participant_id = (
        f"P-{uuid.uuid4().hex[:8]}"
    )

    created_at = datetime.now().isoformat(
        timespec="seconds"
    )

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO participants (
                participant_id,
                created_at
            )
            VALUES (?, ?);
            """,
            (
                participant_id,
                created_at,
            ),
        )

        connection.commit()

    finally:

        connection.close()

    return participant_id


def participant_exists(participant_id):
    """
    Comprueba si existe un participante.
    """

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT 1
            FROM participants
            WHERE participant_id = ?;
            """,
            (participant_id,),
        )

        result = cursor.fetchone()

    finally:

        connection.close()

    return result is not None


def get_participant(participant_id):
    """
    Recupera la información de un participante.
    """

    connection = get_connection()

    try:

        connection.row_factory = sqlite3.Row

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                participant_id,
                created_at
            FROM participants
            WHERE participant_id = ?;
            """,
            (participant_id,),
        )

        row = cursor.fetchone()

    finally:

        connection.close()

    if row is None:
        return None

    return dict(row)
def create_session(
    participant_id,
    session_id=None,
):
    """
    Crea una nueva sesión asociada a un participante.

    Si no se proporciona un session_id, se genera
    automáticamente mediante UUID.
    """

    initialize_database()

    if session_id is None:
        session_id = str(
            uuid.uuid4()
        )

    start_time = datetime.now().isoformat(
        timespec="seconds"
    )

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO sessions (
                session_id,
                participant_id,
                start_time,
                interaction_count,
                difficulty_count,
                final_phase,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?);
            """,
            (
                session_id,
                participant_id,
                start_time,
                0,
                0,
                "planning",
                "active",
            ),
        )

        connection.commit()

    finally:

        connection.close()

    return session_id


def get_session(session_id):
    """
    Recupera la información de una sesión.
    """

    connection = get_connection()

    try:

        connection.row_factory = sqlite3.Row

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                session_id,
                participant_id,
                start_time,
                end_time,
                duration_seconds,
                interaction_count,
                difficulty_count,
                final_phase,
                status
            FROM sessions
            WHERE session_id = ?;
            """,
            (session_id,),
        )

        row = cursor.fetchone()

    finally:

        connection.close()

    if row is None:
        return None

    return dict(row)
def get_participant_sessions(
    participant_id,
    only_closed=True,
):
    """
    Recupera las sesiones asociadas a un participante,
    ordenadas cronológicamente.

    Por defecto devuelve únicamente sesiones cerradas,
    ya que son las que pueden utilizarse para análisis
    longitudinal.
    """

    connection = get_connection()

    try:

        connection.row_factory = sqlite3.Row

        cursor = connection.cursor()

        if only_closed:

            cursor.execute(
                """
                SELECT
                    session_id,
                    participant_id,
                    start_time,
                    end_time,
                    duration_seconds,
                    interaction_count,
                    difficulty_count,
                    final_phase,
                    status
                FROM sessions
                WHERE participant_id = ?
                  AND status = ?
                ORDER BY start_time ASC;
                """,
                (
                    participant_id,
                    "closed",
                ),
            )

        else:

            cursor.execute(
                """
                SELECT
                    session_id,
                    participant_id,
                    start_time,
                    end_time,
                    duration_seconds,
                    interaction_count,
                    difficulty_count,
                    final_phase,
                    status
                FROM sessions
                WHERE participant_id = ?
                ORDER BY start_time ASC;
                """,
                (participant_id,),
            )

        rows = cursor.fetchall()

    finally:

        connection.close()

    return [
        dict(row)
        for row in rows
    ]
def get_active_participant_sessions(
    participant_id,
):
    """
    Recupera las sesiones que permanecen activas
    para un participante.

    Esta función permite identificar sesiones que
    pudieron quedar abiertas por una interrupción
    inesperada de la aplicación.
    """

    connection = get_connection()

    try:

        connection.row_factory = sqlite3.Row

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                session_id,
                participant_id,
                start_time,
                end_time,
                duration_seconds,
                interaction_count,
                difficulty_count,
                final_phase,
                status
            FROM sessions
            WHERE participant_id = ?
              AND status = ?
            ORDER BY start_time ASC;
            """,
            (
                participant_id,
                "active",
            ),
        )

        rows = cursor.fetchall()

    finally:

        connection.close()

    return [
        dict(row)
        for row in rows
    ]

def abandon_database_session(
    session_id,
):
    """
    Marca como abandonada una sesión que permaneció
    activa debido a una interrupción inesperada.

    Antes de marcarla como abandonada, recupera la
    información disponible en sus rastros para
    conservar un resumen de la actividad realizada.

    Una sesión abandonada no se considera una sesión
    completada para el análisis longitudinal.
    """

    connection = get_connection()

    try:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        # -------------------------------------------------
        # Recuperar sesión activa
        # -------------------------------------------------

        cursor.execute(
            """
            SELECT
                start_time
            FROM sessions
            WHERE session_id = ?
              AND status = ?;
            """,
            (
                session_id,
                "active",
            ),
        )

        session_row = cursor.fetchone()

        if session_row is None:
            return False

        # -------------------------------------------------
        # Recuperar último rastro de la sesión
        # -------------------------------------------------

        cursor.execute(
            """
            SELECT
                interaction_number,
                difficulty_count,
                phase_after
            FROM learning_traces
            WHERE session_id = ?
            ORDER BY interaction_number DESC
            LIMIT 1;
            """,
            (session_id,),
        )

        last_trace = cursor.fetchone()

        # -------------------------------------------------
        # Reconstruir métricas disponibles
        # -------------------------------------------------

        if last_trace is not None:

            interaction_count = (
                last_trace["interaction_number"]
            )

            difficulty_count = (
                last_trace["difficulty_count"]
            )

            final_phase = (
                last_trace["phase_after"]
            )

        else:

            interaction_count = 0
            difficulty_count = 0
            final_phase = "planning"

        # -------------------------------------------------
        # Calcular duración
        # -------------------------------------------------

        end_datetime = datetime.now()

        start_datetime = datetime.fromisoformat(
            session_row["start_time"]
        )

        duration_seconds = int(
            (
                end_datetime
                - start_datetime
            ).total_seconds()
        )

        end_time = end_datetime.isoformat(
            timespec="seconds"
        )

        # -------------------------------------------------
        # Marcar sesión como abandonada
        # -------------------------------------------------

        cursor.execute(
            """
            UPDATE sessions
            SET
                end_time = ?,
                duration_seconds = ?,
                interaction_count = ?,
                difficulty_count = ?,
                final_phase = ?,
                status = ?
            WHERE session_id = ?
              AND status = ?;
            """,
            (
                end_time,
                duration_seconds,
                interaction_count,
                difficulty_count,
                final_phase,
                "abandoned",
                session_id,
                "active",
            ),
        )

        connection.commit()

        updated_rows = cursor.rowcount

    finally:
        connection.close()

    return updated_rows > 0

def close_database_session(
    session_id,
    duration_seconds,
    interaction_count,
    difficulty_count,
    final_phase,
):
    """
    Cierra una sesión activa y actualiza sus
    indicadores generales.
    """

    end_time = datetime.now().isoformat(
        timespec="seconds"
    )

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE sessions
            SET
                end_time = ?,
                duration_seconds = ?,
                interaction_count = ?,
                difficulty_count = ?,
                final_phase = ?,
                status = ?
            WHERE session_id = ?;
            """,
            (
                end_time,
                duration_seconds,
                interaction_count,
                difficulty_count,
                final_phase,
                "closed",
                session_id,
            ),
        )

        connection.commit()

        updated_rows = cursor.rowcount

    finally:

        connection.close()

    return updated_rows > 0
def save_database_trace(
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
    Guarda una learning trace asociada a una sesión.
    """

    timestamp = datetime.now().isoformat(
        timespec="seconds"
    )

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO learning_traces (
                session_id,
                timestamp,
                interaction_number,
                activity_id,
                student_message,
                tutor_response,
                phase_before,
                phase_after,
                pedagogical_event,
                metacognitive_strategy,
                scaffolding_level,
                difficulty_count
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """,
            (
                session_id,
                timestamp,
                interaction_number,
                student_message,
                activity_id,
                tutor_response,
                phase_before,
                phase_after,
                pedagogical_event,
                metacognitive_strategy,
                scaffolding_level,
                difficulty_count,
            ),
        )

        connection.commit()

        trace_id = cursor.lastrowid

    finally:

        connection.close()

    return trace_id

def save_technical_event(
    session_id,
    participant_id,
    component,
    error_type,
    error_message=None,
):
    """
    Registra una incidencia técnica del prototipo.

    Estos eventos se almacenan de forma independiente
    de los rastros pedagógicos y no intervienen en las
    métricas de aprendizaje.
    """

    timestamp = datetime.now().isoformat(
        timespec="seconds"
    )

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO technical_events (
                timestamp,
                session_id,
                participant_id,
                component,
                error_type,
                error_message
            )
            VALUES (?, ?, ?, ?, ?, ?);
            """,
            (
                timestamp,
                session_id,
                participant_id,
                component,
                error_type,
                error_message,
            ),
        )

        connection.commit()

        technical_event_id = (
            cursor.lastrowid
        )

    finally:
        connection.close()

    return technical_event_id

def get_session_traces(session_id):
    """
    Recupera las learning traces de una sesión
    ordenadas por número de interacción.
    """

    connection = get_connection()

    try:

        connection.row_factory = sqlite3.Row

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                trace_id,
                session_id,
                timestamp,
                interaction_number,
                student_message,
                tutor_response,
                phase_before,
                phase_after,
                pedagogical_event,
                metacognitive_strategy,
                scaffolding_level,
                difficulty_count
            FROM learning_traces
            WHERE session_id = ?
            ORDER BY interaction_number ASC;
            """,
            (session_id,),
        )

        rows = cursor.fetchall()

    finally:

        connection.close()

    return [
        dict(row)
        for row in rows
    ]
def save_participant_consent(
    participant_id,
    consent_version="1.0",
):
    """
    Registra la aceptación del consentimiento informado
    de un participante.
    """

    conn = get_connection()
    cursor = conn.cursor()

    consent_timestamp = datetime.now().isoformat()

    cursor.execute(
        """
        INSERT INTO participant_consents (
            participant_id,
            consent_version,
            consent_given,
            consent_timestamp
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            participant_id,
            consent_version,
            1,
            consent_timestamp,
        ),
    )

    conn.commit()
    conn.close()
def has_valid_consent(
    participant_id,
    consent_version="1.0",
):
    """
    Verifica si el participante ya aceptó
    la versión actual del consentimiento.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT consent_id
        FROM participant_consents
        WHERE participant_id = ?
          AND consent_version = ?
          AND consent_given = 1
        LIMIT 1
        """,
        (
            participant_id,
            consent_version,
        ),
    )

    result = cursor.fetchone()

    conn.close()

    return result is not None