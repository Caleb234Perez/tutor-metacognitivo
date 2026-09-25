from services.database_service import (
    get_connection,
)

connection = get_connection()

try:
    connection.row_factory = __import__(
        "sqlite3"
    ).Row

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            technical_event_id,
            timestamp,
            session_id,
            participant_id,
            component,
            error_type,
            error_message
        FROM technical_events
        WHERE component = ?
        ORDER BY technical_event_id DESC
        LIMIT 1;
        """,
        ("response_generator",),
    )

    event = cursor.fetchone()

finally:
    connection.close()


print("\nÚLTIMO ERROR DEL CLASIFICADOR")
print("=" * 50)

if event is None:

    print("No se encontró ningún evento.")

else:

    print(
        "technical_event_id:",
        event["technical_event_id"],
    )

    print(
        "timestamp:",
        event["timestamp"],
    )

    print(
        "session_id:",
        event["session_id"],
    )

    print(
        "participant_id:",
        event["participant_id"],
    )

    print(
        "component:",
        event["component"],
    )

    print(
        "error_type:",
        event["error_type"],
    )

    print(
        "error_message:",
        event["error_message"],
    )