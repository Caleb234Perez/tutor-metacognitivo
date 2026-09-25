VALID_PHASES = (
    "planning",
    "monitoring",
    "control",
    "reflection",
)

VALID_EVENTS = (
    "plan_ready",
    "difficulty_detected",
    "difficulty_resolved",
    "activity_completed",
)


def initialize_pedagogical_state():
    """
    Devuelve el estado pedagógico inicial de una sesión.
    """

    return {
        "phase": "planning",
        "interaction_count": 0,
        "difficulty_count": 0,
        "scaffolding_level": 1,
        "reflection_count": 0,
    }


def get_current_phase(state):
    """
    Obtiene la fase metacognitiva actual.
    """

    return state["phase"]


def register_interaction(state):
    """
    Registra una nueva intervención del estudiante.
    """

    state["interaction_count"] += 1

    return state

def get_scaffolding_level(state):
    """
    Obtiene el nivel actual de andamiaje.
    """

    return state["scaffolding_level"]


def increase_scaffolding_level(state):
    """
    Incrementa progresivamente el nivel de andamiaje
    hasta un máximo de 4.
    """

    if state["scaffolding_level"] < 4:
        state["scaffolding_level"] += 1

    return state


def reset_scaffolding_level(state):
    """
    Restablece el andamiaje al nivel inicial.
    """

    state["scaffolding_level"] = 1

    return state

def change_phase(state, new_phase):
    """
    Cambia la fase metacognitiva de la sesión.
    """

    if new_phase not in VALID_PHASES:
        raise ValueError(
            f"Fase metacognitiva no reconocida: {new_phase}"
        )

    state["phase"] = new_phase

    return state


def process_pedagogical_event(state, event):
    """
    Procesa un evento pedagógico y realiza una transición
    cuando la combinación fase-evento está permitida.
    """

    if event not in VALID_EVENTS:
        raise ValueError(
            f"Evento pedagógico no reconocido: {event}"
        )

    current_phase = state["phase"]

    transitions = {
        ("planning", "plan_ready"): "monitoring",
        ("monitoring", "difficulty_detected"): "control",
        ("control", "difficulty_resolved"): "monitoring",
        ("monitoring", "activity_completed"): "reflection",
        ("control", "activity_completed"): "reflection",
    }

    new_phase = transitions.get(
        (current_phase, event)
    )

    if new_phase is not None:
        state["phase"] = new_phase

    if event == "difficulty_detected":
        state["difficulty_count"] += 1

        if current_phase == "control":
            state = increase_scaffolding_level(state)

    if event == "difficulty_resolved":
        state = reset_scaffolding_level(state)


    return state

def register_reflection_interaction(state):
    """
    Registra una intervención del estudiante realizada
    durante la fase de reflexión.
    """

    if state["phase"] == "reflection":
        state["reflection_count"] += 1

    return state