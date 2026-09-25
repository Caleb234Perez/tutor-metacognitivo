from pedagogy.pedagogical_engine import (
    initialize_pedagogical_state,
    process_pedagogical_event,
)


state = initialize_pedagogical_state()

print("Inicial:")
print(state)


state = process_pedagogical_event(
    state,
    "plan_ready",
)

print("\nPlan listo:")
print(state)


state = process_pedagogical_event(
    state,
    "difficulty_detected",
)

print("\nPrimera dificultad:")
print(state)


state = process_pedagogical_event(
    state,
    "difficulty_detected",
)

print("\nDificultad persiste:")
print(state)


state = process_pedagogical_event(
    state,
    "difficulty_detected",
)

print("\nDificultad continúa:")
print(state)


state = process_pedagogical_event(
    state,
    "difficulty_resolved",
)

print("\nDificultad resuelta:")
print(state)