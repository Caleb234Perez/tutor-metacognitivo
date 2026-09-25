from pedagogy.strategy_manager import select_metacognitive_strategy


tests = [
    ("planning", 1, "none"),
    ("planning", 1, "plan_ready"),

    ("monitoring", 1, "none"),
    ("monitoring", 1, "difficulty_resolved"),

    ("control", 1, "difficulty_detected"),
    ("control", 2, "difficulty_detected"),
    ("control", 3, "difficulty_detected"),
    ("control", 4, "difficulty_detected"),

    ("reflection", 1, "activity_completed"),
]


for phase, level, event in tests:
    strategy = select_metacognitive_strategy(
        phase=phase,
        scaffolding_level=level,
        pedagogical_event=event,
    )

    print(
        f"Fase: {phase:12} | "
        f"Scaffolding: {level} | "
        f"Evento: {event:22} | "
        f"Estrategia: {strategy}"
    )