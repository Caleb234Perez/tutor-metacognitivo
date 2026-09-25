from pedagogy.pedagogical_engine import (
    initialize_pedagogical_state,
    process_pedagogical_event,
)

from pedagogy.strategy_manager import (
    select_metacognitive_strategy,
)

state = initialize_pedagogical_state()

# Simulamos que el estudiante se encuentra en control
state["phase"] = "control"
state["scaffolding_level"] = 3
state["difficulty_count"] = 2

print("=== ANTES ===")
print("Fase:", state["phase"])
print(
    "Nivel de apoyo:",
    state["scaffolding_level"],
)
print(
    "Dificultades:",
    state["difficulty_count"],
)


# El estudiante termina la actividad
state = process_pedagogical_event(
    state,
    "activity_completed",
)


print("\n=== DESPUÉS ===")
print("Fase:", state["phase"])
print(
    "Nivel de apoyo:",
    state["scaffolding_level"],
)
print(
    "Dificultades:",
    state["difficulty_count"],
)
strategy = select_metacognitive_strategy(
    phase=state["phase"],
    scaffolding_level=state[
        "scaffolding_level"
    ],
    pedagogical_event="activity_completed",
)

print("\n=== ESTRATEGIA ===")
print("Estrategia:", strategy)
