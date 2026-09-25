from services.database_service import (
    initialize_database,
    save_participant_consent,
    has_valid_consent,
)

initialize_database()

participant_id = "P-4e1f84f8"

print("=== PRUEBA DE CONSENTIMIENTO ===")

before = has_valid_consent(
    participant_id,
    "1.0",
)

print(
    "Consentimiento antes de guardar:",
    before,
)

if not before:
    save_participant_consent(
        participant_id,
        "1.0",
    )

after = has_valid_consent(
    participant_id,
    "1.0",
)

print(
    "Consentimiento después de guardar:",
    after,
)

other_version = has_valid_consent(
    participant_id,
    "1.1",
)

print(
    "Consentimiento versión 1.1:",
    other_version,
)