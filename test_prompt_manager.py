from pedagogy.prompt_manager import build_system_prompt


tests = [
    ("planning", 1, "goal_setting"),
    ("planning", 1, "planning_steps"),
    ("monitoring", 1, "comprehension_check"),
    ("monitoring", 1, "self_explanation"),
    ("control", 1, "guiding_question"),
    ("control", 2, "conceptual_hint"),
    ("control", 3, "specific_hint"),
    ("control", 4, "partial_support"),
    ("reflection", 1, "strategy_reflection"),
]


for phase, level, strategy in tests:
    prompt = build_system_prompt(
        phase=phase,
        scaffolding_level=level,
        strategy=strategy,
    )

    print("=" * 70)
    print(
        f"FASE: {phase} | "
        f"SCAFFOLDING: {level} | "
        f"ESTRATEGIA: {strategy}"
    )
    print(f"Longitud del prompt: {len(prompt)} caracteres")
    print()