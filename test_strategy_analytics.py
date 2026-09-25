from services.analytics_service import (
    calculate_session_metrics,
)


session_id = input(
    "Introduce el ID de la sesión: "
).strip()

metrics = calculate_session_metrics(
    session_id
)

if metrics is None:
    print("No se encontró la sesión.")

else:
    print()
    print("Estrategias utilizadas:")

    for strategy in metrics["strategies_used"]:
        print(f"- {strategy}")

    print()
    print("Distribución de estrategias:")

    for strategy, count in (
        metrics["strategy_distribution"].items()
    ):
        print(
            f"- {strategy}: {count}"
        )