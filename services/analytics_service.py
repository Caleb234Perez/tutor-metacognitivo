from pathlib import Path

import pandas as pd
from services.database_service import (
    get_participant_sessions,
    get_session,
    get_session_traces
)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"




def get_session_data(session_id):
    """
    Obtiene los rastros y el resumen asociados
    con una sesión específica desde SQLite.
    """

    session = get_session(session_id)
    traces = get_session_traces(session_id)

    if session is None:
        session_summary = pd.DataFrame()
    else:
        session_summary = pd.DataFrame(
            [session]
        )

    if not traces:
        session_traces = pd.DataFrame()
    else:
        session_traces = pd.DataFrame(
            traces
        )

    return {
        "traces": session_traces,
        "summary": session_summary,
    }

def calculate_session_metrics(session_id):
    """
    Calcula indicadores de Analítica de Aprendizaje
    para una sesión específica.
    """

    session_data = get_session_data(session_id)

    traces = session_data["traces"]
    summary = session_data["summary"]

    if summary.empty:
        return None

    # Datos generales de la sesión
    summary_row = summary.iloc[0]

    interaction_count = int(
        summary_row["interaction_count"]
    )

    difficulty_count = int(
        summary_row["difficulty_count"]
    )

    duration_seconds = int(
        summary_row["duration_seconds"]
    )

    final_phase = summary_row["final_phase"]

    # Datos obtenidos de las trazas
    if traces.empty:
        max_scaffolding_level = 1
        phases_visited = []
        pedagogical_events = []
        strategies_used = []
    else:
        max_scaffolding_level = int(
            traces["scaffolding_level"].max()
        )

        phases_visited = (
            traces["phase_after"]
            .dropna()
            .unique()
            .tolist()
        )

        pedagogical_events = (
            traces["pedagogical_event"]
            .dropna()
            .tolist()
        )
        if "metacognitive_strategy" in traces.columns:
            strategies_used = (
                traces["metacognitive_strategy"]
                .dropna()
                .loc[
                    lambda values:
                    values.astype(str).str.strip() != ""
                ]
                .unique()
                .tolist()
            )
        else:
            strategies_used = []
    if interaction_count > 0:
        difficulty_rate = (
            difficulty_count / interaction_count
        ) * 100
    else:
        difficulty_rate = 0.0

    difficulty_rate = round(
        difficulty_rate,
        2
    )

    phase_transition_count = 0

    if not traces.empty:
        for _, row in traces.iterrows():
            if (
                row["phase_before"]
                != row["phase_after"]
            ):
                phase_transition_count += 1
        # -------------------------------------------------
    # Distribución de interacciones por fase
    # -------------------------------------------------

    phase_distribution = {}

    if not traces.empty:
        phase_counts = (
            traces["phase_after"]
            .dropna()
            .value_counts()
        )

        phase_distribution = {
            phase: int(count)
            for phase, count
            in phase_counts.items()
        }
        # -------------------------------------------------
    # Trayectoria metacognitiva
    # -------------------------------------------------
    strategy_distribution = {}
    if (
        not traces.empty
        and "metacognitive_strategy" in traces.columns
    ):
        strategy_values = (
            traces["metacognitive_strategy"]
            .dropna()
        )
        strategy_values = strategy_values[
            strategy_values.astype(str).str.strip() != ""
        ]
        strategy_counts = (
            strategy_values.value_counts()
        )
        strategy_distribution = {
            strategy: int(count)
            for strategy, count
            in strategy_counts.items()
        }

    phase_path = []

    if not traces.empty:

        first_phase = (
            traces.iloc[0]["phase_before"]
        )

        if pd.notna(first_phase):
            phase_path.append(first_phase)

        for phase in traces["phase_after"]:

            if pd.isna(phase):
                continue

            if (
                not phase_path
                or phase_path[-1] != phase
            ):
                phase_path.append(phase)


    return {
        "session_id": session_id,
        "interaction_count": interaction_count,
        "difficulty_count": difficulty_count,
        "duration_seconds": duration_seconds,
        "final_phase": final_phase,
        "max_scaffolding_level": max_scaffolding_level,
        "phases_visited": phases_visited,
        "pedagogical_events": pedagogical_events,
        "difficulty_rate": difficulty_rate,
        "phase_transition_count": phase_transition_count,
        "phase_distribution":phase_distribution,
        "phase_path":phase_path,
        "strategies_used":strategies_used,
        "strategy_distribution": strategy_distribution,
    }


def build_session_profile(session_id):
    """
    Construye un perfil analítico básico de una sesión
    a partir de los indicadores de Learning Analytics.
    """

    metrics = calculate_session_metrics(session_id)

    if metrics is None:
        return None

    # ---------------------------------------------
    # Interpretación de dificultades
    # ---------------------------------------------

    difficulty_rate = metrics["difficulty_rate"]

    if difficulty_rate == 0:
        difficulty_level = "none"

    elif difficulty_rate <= 33.33:
        difficulty_level = "low"

    elif difficulty_rate <= 66.67:
        difficulty_level = "moderate"

    else:
        difficulty_level = "high"

    # ---------------------------------------------
    # Interpretación del scaffolding
    # ---------------------------------------------

    max_scaffolding = metrics[
        "max_scaffolding_level"
    ]

    if max_scaffolding == 1:
        support_level = "minimal"

    elif max_scaffolding == 2:
        support_level = "moderate"

    elif max_scaffolding == 3:
        support_level = "high"

    else:
        support_level = "intensive"

    # ---------------------------------------------
    # Perfil resultante
    # ---------------------------------------------

    return {
        "session_id": session_id,
        "difficulty_level": difficulty_level,
        "support_level": support_level,
        "final_phase": metrics["final_phase"],
        "phases_visited": metrics["phases_visited"],
        "phase_path": metrics["phase_path"],
        "phase_transition_count":
            metrics["phase_transition_count"],
        "interaction_count": metrics["interaction_count"],
    }
def generate_session_feedback(session_id):
    """
    Genera una retroalimentación metacognitiva básica
    a partir del perfil analítico de la sesión.
    """

    profile = build_session_profile(session_id)

    if profile is None:
        return None
    if profile["interaction_count"] == 0:
        return (
            "La sesión finalizó sin registrar interacciones "
            "del estudiante. Por lo tanto, no se dispone de "
            "evidencia suficiente para generar una "
            "retroalimentación metacognitiva sobre el proceso "
            "de aprendizaje."
        )

    feedback_parts = []

    # ---------------------------------------------
    # Dificultades
    # ---------------------------------------------

    difficulty_level = profile[
        "difficulty_level"
    ]

    if difficulty_level == "none":
        feedback_parts.append(
            "Durante la sesión no se registraron "
            "eventos explícitos de dificultad."
        )

    elif difficulty_level == "low":
        feedback_parts.append(
            "Durante la sesión se presentaron pocas "
            "dificultades en relación con el número "
            "de interacciones realizadas."
        )

    elif difficulty_level == "moderate":
        feedback_parts.append(
            "Durante la sesión se presentaron "
            "dificultades de manera recurrente, "
            "aunque estas formaron parte del proceso "
            "de resolución de la actividad."
        )

    else:
        feedback_parts.append(
            "Durante la sesión se registró una alta "
            "frecuencia de dificultades, por lo que "
            "fue necesario dedicar una parte importante "
            "de la interacción a superar bloqueos."
        )

    # ---------------------------------------------
    # Scaffolding
    # ---------------------------------------------

    support_level = profile[
        "support_level"
    ]

    if support_level == "minimal":
        feedback_parts.append(
            "El estudiante pudo continuar principalmente "
            "mediante preguntas orientadoras y apoyo mínimo."
        )

    elif support_level == "moderate":
        feedback_parts.append(
            "En algunos momentos fue necesario incrementar "
            "el apoyo mediante pistas conceptuales."
        )

    elif support_level == "high":
        feedback_parts.append(
            "El tutor proporcionó apoyos progresivamente "
            "más específicos para facilitar el avance."
        )

    else:
        feedback_parts.append(
            "La sesión requirió un nivel intensivo de "
            "andamiaje, incluyendo apoyos más explícitos "
            "para permitir que el estudiante continuara."
        )

    
    # ---------------------------------------------
    # Fase final
    # ---------------------------------------------

    final_phase = profile[
        "final_phase"
    ]

    if final_phase == "planning":
        feedback_parts.append(
            "La sesión finalizó durante la planeación, "
            "por lo que el proceso todavía se encontraba "
            "en la definición de objetivos o estrategias."
        )

    elif final_phase == "monitoring":
        feedback_parts.append(
            "La sesión finalizó durante el monitoreo, "
            "manteniendo la atención en la revisión "
            "del avance y la comprensión."
        )

    elif final_phase == "control":
        feedback_parts.append(
            "La sesión finalizó durante una etapa de control, "
            "lo que indica que al cierre todavía se estaba "
            "trabajando sobre una dificultad o ajuste "
            "de estrategia."
        )

    elif final_phase == "reflection":
        feedback_parts.append(
            "La sesión alcanzó la etapa de reflexión, "
            "permitiendo valorar el resultado y el proceso "
            "seguido durante la actividad."
        )

    # ---------------------------------------------
    # Pregunta para reflexión
    # ---------------------------------------------

    feedback_parts.append(
        "Como reflexión, puede ser útil identificar "
        "qué estrategia permitió avanzar cuando apareció "
        "una dificultad y qué podría hacerse de manera "
        "diferente en una actividad similar."
    )

    return " ".join(
        feedback_parts
    )
def get_participant_session_history(participant_id):
    """
    Recupera el historial de sesiones cerradas
    asociadas a un participante.

    Las sesiones se devuelven en orden cronológico
    y se distingue si contienen evidencia suficiente
    para análisis longitudinal.
    """

    sessions = get_participant_sessions(
        participant_id,
        only_closed=True,
    )

    history = []

    for session in sessions:

        interaction_count = int(
            session["interaction_count"] or 0
        )

        history.append(
            {
                "session_id": session["session_id"],
                "participant_id": session["participant_id"],
                "start_time": session["start_time"],
                "end_time": session["end_time"],
                "duration_seconds": int(
                    session["duration_seconds"] or 0
                ),
                "interaction_count": interaction_count,
                "difficulty_count": int(
                    session["difficulty_count"] or 0
                ),
                "final_phase": session["final_phase"],
                "status": session["status"],
                "has_learning_evidence": (
                    interaction_count > 0
                ),
            }
        )

    return history
def get_analyzable_participant_sessions(participant_id):
    """
    Recupera únicamente las sesiones cerradas de un
    participante que contienen evidencia de aprendizaje
    suficiente para ser consideradas en el análisis
    longitudinal.
    """

    history = get_participant_session_history(
        participant_id
    )

    analyzable_sessions = [
        session
        for session in history
        if session["has_learning_evidence"]
    ]

    return analyzable_sessions

def calculate_longitudinal_metrics(participant_id):
    """
    Calcula indicadores longitudinales descriptivos
    a partir de las sesiones analizables de un
    participante.

    Los resultados describen cambios observados entre
    sesiones y no representan por sí mismos evidencia
    de mejora o deterioro del aprendizaje.
    """

    sessions = get_analyzable_participant_sessions(
        participant_id
    )

    if not sessions:
        return None

    session_metrics = []

    for session in sessions:

        session_id = session["session_id"]

        metrics = calculate_session_metrics(
            session_id
        )

        if metrics is None:
            continue

        session_metrics.append(
            {
                "session_id": session_id,
                "start_time": session["start_time"],
                "interaction_count": (
                    metrics["interaction_count"]
                ),
                "difficulty_count": (
                    metrics["difficulty_count"]
                ),
                "difficulty_rate": (
                    metrics["difficulty_rate"]
                ),
                "max_scaffolding_level": (
                    metrics["max_scaffolding_level"]
                ),
                "phase_transition_count": (
                    metrics["phase_transition_count"]
                ),
                "final_phase": (
                    metrics["final_phase"]
                ),
                "phases_visited": (
                    metrics["phases_visited"]
                ),
                "strategies_used": (
                    metrics["strategies_used"]
                ),
            }
        )

    if not session_metrics:
        return None

    return {
        "participant_id": participant_id,
        "session_count": len(session_metrics),
        "has_longitudinal_evidence": (
            len(session_metrics) >= 2
        ),
        "sessions": session_metrics,
    }
def calculate_session_changes(participant_id):
    """
    Calcula cambios descriptivos entre sesiones
    consecutivas de un participante.

    Los cambios representan diferencias observadas
    en los indicadores registrados y no implican
    por sí mismos mejora o deterioro del aprendizaje.
    """

    longitudinal = calculate_longitudinal_metrics(
        participant_id
    )

    if longitudinal is None:
        return None

    sessions = longitudinal["sessions"]

    if len(sessions) < 2:
        return {
            "participant_id": participant_id,
            "comparison_count": 0,
            "comparisons": [],
        }

    comparisons = []

    for index in range(1, len(sessions)):

        previous_session = sessions[index - 1]
        current_session = sessions[index]

        difficulty_rate_change = round(
            current_session["difficulty_rate"]
            - previous_session["difficulty_rate"],
            2,
        )

        scaffolding_change = (
            current_session["max_scaffolding_level"]
            - previous_session["max_scaffolding_level"]
        )

        interaction_change = (
            current_session["interaction_count"]
            - previous_session["interaction_count"]
        )

        transition_change = (
            current_session["phase_transition_count"]
            - previous_session["phase_transition_count"]
        )

        comparisons.append(
            {
                "previous_session_id": (
                    previous_session["session_id"]
                ),
                "current_session_id": (
                    current_session["session_id"]
                ),
                "difficulty_rate_change": (
                    difficulty_rate_change
                ),
                "scaffolding_change": (
                    scaffolding_change
                ),
                "interaction_change": (
                    interaction_change
                ),
                "transition_change": (
                    transition_change
                ),
                "previous_final_phase": (
                    previous_session["final_phase"]
                ),
                "current_final_phase": (
                    current_session["final_phase"]
                ),
            }
        )

    return {
        "participant_id": participant_id,
        "comparison_count": len(comparisons),
        "comparisons": comparisons,
    }
def generate_longitudinal_feedback(participant_id):
    """
    Genera una interpretación descriptiva de los cambios
    observados entre las dos sesiones analizables más
    recientes de un participante.

    La retroalimentación describe diferencias registradas
    en los indicadores y no implica por sí misma mejora
    o deterioro del aprendizaje.
    """

    changes = calculate_session_changes(
        participant_id
    )

    if changes is None:
        return None

    comparisons = changes["comparisons"]

    if not comparisons:
        return (
            "Todavía no hay suficientes sesiones "
            "con evidencia de aprendizaje para realizar "
            "una comparación longitudinal."
        )

    latest_comparison = comparisons[-1]

    feedback_parts = []

    # -------------------------------------------------
    # Tasa de dificultad
    # -------------------------------------------------

    difficulty_change = (
        latest_comparison[
            "difficulty_rate_change"
        ]
    )

    if difficulty_change < 0:

        feedback_parts.append(
            "En la sesión más reciente se registró "
            "una menor proporción de interacciones "
            "con dificultad que en la sesión anterior."
        )

    elif difficulty_change > 0:

        feedback_parts.append(
            "En la sesión más reciente se registró "
            "una mayor proporción de dificultades "
            "con dificultad que en la sesión anterior."
        )

    else:

        feedback_parts.append(
            "La proporción de interacciones con dificultades "
            "se mantuvo sin cambios entre las dos "
            "sesiones más recientes."
        )

    # -------------------------------------------------
    # Scaffolding
    # -------------------------------------------------

    scaffolding_change = (
        latest_comparison[
            "scaffolding_change"
        ]
    )

    if scaffolding_change < 0:

        feedback_parts.append(
            "En la sesión más reciente se registró"
            "un nivel máximo de apoyo menor que "
            "en la sesión anterior."
        )

    elif scaffolding_change > 0:

        feedback_parts.append(
            "En la sesión más reciente se registró "
            "un nivel máximo de apoyo mayor que "
            "en la sesión anterior."
        )

    else:

        feedback_parts.append(
            "El nivel máximo de de apoyo se mantuvo "
            "sin cambios entre ambas sesiones "
            "más recientes."
        )

    # -------------------------------------------------
    # Interacciones
    # -------------------------------------------------

    interaction_change = (
        latest_comparison[
            "interaction_change"
        ]
    )

    if interaction_change < 0:

        feedback_parts.append(
            "La sesión más reciente tuvo menos "
            "interacciones que la anterior."
        )

    elif interaction_change > 0:

        feedback_parts.append(
            "La sesión más reciente tuvo más "
            "interacciones que la anterior."
        )

    else:

        feedback_parts.append(
            "El número de interacciones se mantuvo "
            "igual entre ambas sesiones."
        )

    # -------------------------------------------------
    # Transiciones
    # -------------------------------------------------

    transition_change = (
        latest_comparison[
            "transition_change"
        ]
    )

    if transition_change < 0:

        feedback_parts.append(
            "En la sesión más reciente se registraron "
            "menos cambios entre fases metacognitivas "
            "que en la sesión anterior."
        )

    elif transition_change > 0:

        feedback_parts.append(
            "En la sesión más reciente se registraron "
            "más cambios entre fases metacognitivas "
            "que en la sesión anterior."
        )

    else:

        feedback_parts.append(
            "El número de cambios entre fases "
            "metacognitivas se mantuvo sin cambios "
            "entre las dos sesiones más recientes."
        )

    phase_labels = {
        "planning": "Planeación",
        "monitoring": "Monitoreo",
        "control": "Control",
        "reflection": "Reflexión",
    }
    # -------------------------------------------------
    # Fase final
    # -------------------------------------------------

    previous_phase = phase_labels.get(
        latest_comparison[
            "previous_final_phase"
        ],
        latest_comparison[
            "previous_final_phase"
        ],
    )

    current_phase = phase_labels.get(
        latest_comparison[
            "current_final_phase"
        ],
        latest_comparison[
            "current_final_phase"
        ],
    )

    if previous_phase != current_phase:

        feedback_parts.append(
            "La fase al finalizar la sesión cambió de "
            f"{previous_phase} a {current_phase}."
        )

    else:

        feedback_parts.append(
            "La fase al finalizar fue la misma "
            "en ambas sesiones."
        )

    # -------------------------------------------------
    # Cierre interpretativo
    # -------------------------------------------------

    feedback_parts.append(
        "Los cambios observados entre sesiones no indican "
        "por sí solos una mejora o un retroceso en tu aprendizaje. "
        "Es importante interpretarlos considerando el contexto "
        "y las características de las actividades realizadas."
    )

    return " ".join(
        feedback_parts
    )