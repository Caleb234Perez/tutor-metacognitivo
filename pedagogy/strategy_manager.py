def select_metacognitive_strategy(
    phase: str,
    scaffolding_level: int = 1,
    pedagogical_event: str = "none",
) -> str:
    """
    Selecciona la estrategia metacognitiva que debe utilizar
    el tutor de acuerdo con la fase pedagógica, el nivel de
    scaffolding y el evento detectado.
    """

    if phase == "planning":
        if pedagogical_event == "none":
            return "goal_setting"

        return "planning_steps"

    if phase == "monitoring":
        if pedagogical_event == "difficulty_resolved":
            return "self_explanation"

        if pedagogical_event == "activity_completed":
            return "progress_check"

        return "comprehension_check"

    if phase == "control":
        if scaffolding_level <= 1:
            return "guiding_question"

        if scaffolding_level == 2:
            return "conceptual_hint"

        if scaffolding_level == 3:
            return "specific_hint"

        return "partial_support"

    if phase == "reflection":
        if pedagogical_event == "activity_completed":
            return "strategy_reflection"

        return "transfer_reflection"

    return "comprehension_check"