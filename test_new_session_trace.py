from services.database_service import (
    get_session_traces,
)

SESSION_ID = "f6a83792-e879-4c95-8ee0-4fcce3340a86"

traces = get_session_traces(SESSION_ID)

print("\n=== RASTROS DE LA NUEVA SESIÓN ===")
print(f"Total de rastros: {len(traces)}")

for trace in traces:
    print("\n-----------------------------")
    print(
        "Interacción:",
        trace["interaction_number"],
    )
    print(
        "Mensaje:",
        trace["student_message"],
    )
    print(
        "Evento:",
        trace["pedagogical_event"],
    )
    print(
        "Fase:",
        trace["phase_before"],
        "->",
        trace["phase_after"],
    )
    print(
        "Estrategia:",
        trace["metacognitive_strategy"],
    )
    print(
        "Nivel de apoyo:",
        trace["scaffolding_level"],
    )