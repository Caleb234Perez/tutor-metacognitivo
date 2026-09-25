from services.analytics_service import (
    get_session_data,
    calculate_session_metrics,
    build_session_profile,
    generate_session_feedback,
)

from services.database_service import (
    get_participant_sessions,
)


participant_id = "P-ae22ebd8"

sessions = get_participant_sessions(
    participant_id,
    only_closed=True
)


if not sessions:
    print(
        "No se encontraron sesiones "
        "cerradas para el participante."
    )
    raise SystemExit


session_id = sessions[0][
    "session_id"
]


print("\nParticipante:")
print(participant_id)

print("\nSesión seleccionada:")
print(session_id)


session_data = get_session_data(
    session_id
)


print("\nTrazas de la sesión:")
print(
    session_data["traces"]
)

print("\nResumen de la sesión:")
print(
    session_data["summary"]
)


print("\n" + "=" * 50)
print(
    "INDICADORES DE ANALÍTICA "
    "DE APRENDIZAJE"
)
print("=" * 50)


metrics = calculate_session_metrics(
    session_id
)

if metrics is not None:
    for key, value in metrics.items():
        print(
            f"{key}: {value}"
        )
else:
    print(
        "No fue posible calcular "
        "los indicadores."
    )


print("\n" + "=" * 50)
print(
    "PERFIL ANALÍTICO DE LA SESIÓN"
)
print("=" * 50)


profile = build_session_profile(
    session_id
)

if profile is not None:
    for key, value in profile.items():
        print(
            f"{key}: {value}"
        )
else:
    print(
        "No fue posible construir "
        "el perfil de la sesión."
    )


print("\n" + "=" * 50)
print(
    "RETROALIMENTACIÓN METACOGNITIVA"
)
print("=" * 50)


feedback = generate_session_feedback(
    session_id
)

if feedback is not None:
    print(feedback)
else:
    print(
        "No fue posible generar "
        "retroalimentación."
    )