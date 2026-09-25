from services.learning_trace_service import (
    initialize_trace_storage,
    FIELDNAMES,
)


initialize_trace_storage()

print("Almacenamiento inicializado correctamente.")
print()
print("Campos actuales:")

for field in FIELDNAMES:
    print(f"- {field}")