from pedagogy.pedagogical_engine import (
    initialize_pedagogical_state,
    process_pedagogical_event,
)


state = initialize_pedagogical_state()

print("Estado inicial:")
print(state)


state = process_pedagogical_event(
    state,
    "plan_ready",
)

print("\nPlan definido:")
print(state)


state = process_pedagogical_event(
    state,
    "difficulty_detected",
)

print("\nDificultad detectada:")
print(state)


state = process_pedagogical_event(
    state,
    "difficulty_resolved",
)

print("\nDificultad superada:")
print(state)


state = process_pedagogical_event(
    state,
    "activity_completed",
)

print("\nActividad completada:")
print(state)