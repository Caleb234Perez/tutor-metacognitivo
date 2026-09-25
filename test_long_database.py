from services.analytics_service import (
    generate_longitudinal_feedback,
)


participant_id = "P-ae22ebd8"


feedback = generate_longitudinal_feedback(
    participant_id
)


print("\nRETROALIMENTACIÓN LONGITUDINAL")

print(feedback)