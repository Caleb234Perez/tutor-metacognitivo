import uuid
import copy
from services.activity_manager import (
    get_activity,
    get_available_activities,
)
import pandas as pd
import streamlit as st
import plotly.express as px
from services.evidence_classifier_service import (
    classify_pedagogical_evidence,
)

from pedagogy.pedagogical_engine import (
    initialize_pedagogical_state,
    get_current_phase,
    get_scaffolding_level,
    register_interaction,
    process_pedagogical_event,
    register_reflection_interaction,
)

from pedagogy.prompt_manager import (
    build_system_prompt,
)

from pedagogy.strategy_manager import(
    select_metacognitive_strategy
)

from services.ollama_service import (
    generate_response,
)

from services.learning_trace_service import (
    save_learning_trace,
    save_database_trace,
)

from services.session_service import (
    initialize_session,
    close_session,
    get_session_duration_seconds,
    save_session_summary,
    initialize_database_session,
    save_database_session_summary,
)

from services.analytics_service import (
    calculate_session_metrics,
    build_session_profile,
    generate_session_feedback,
    calculate_longitudinal_metrics,
    calculate_session_changes,
    generate_longitudinal_feedback,
)

from services.database_service import (
    initialize_database,
    create_participant,
    participant_exists,
    get_active_participant_sessions,
    abandon_database_session,
    save_technical_event,
    save_participant_consent,
    has_valid_consent,
)

# -----------------------------------------------------
# Configuración de desarrollo
# -----------------------------------------------------

DEBUG_MODE = False
CONSENT_VERSION = "1.0"
# ---------------------------------------------------------
# Configuración general
# ---------------------------------------------------------

st.set_page_config(
    page_title="Tutor Metacognitivo",
    page_icon="🎓",
    layout="centered",
)

st.title("🎓 Tutor Metacognitivo")
st.caption(
    "Un espacio para planear, monitorear y reflexionar sobre tu aprendizaje"
)



# ---------------------------------------------------------
# Función para crear nueva sesión
# ---------------------------------------------------------

def start_new_session():

    st.session_state.session_id = str(
        uuid.uuid4()
    )

    st.session_state.session_data = (
        initialize_session(
            st.session_state.session_id
        )
    )
    active_sessions = (
        get_active_participant_sessions(
            st.session_state.participant_id
        )
    )

    for active_session in active_sessions:

        abandon_database_session(
            active_session["session_id"]
        )
    
    initialize_database_session(
        participant_id=(
            st.session_state.participant_id
        ),
        session_id=(
            st.session_state.session_id
        ),
    )



    st.session_state.database_session_initialized = (
        True
    )
    st.session_state.pedagogical_state = (
        initialize_pedagogical_state()
    )
    st.session_state.last_pedagogical_event = (
        "none"
    )
    st.session_state.current_strategy = (
        "goal_setting"
    )
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hola. Soy tu tutor metacognitivo. "
                "Durante esta sesión te acompañaré en tu proceso de aprendizaje. "
                "Selecciona uno de los ejercicios disponibles y, cuando estés listo, "
                "cuéntame cómo planeas abordarlo."
            ),
        }
    ]


# ---------------------------------------------------------
# Inicialización del historial
# ---------------------------------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hola. Soy tu tutor metacognitivo. "
                "Durante esta sesión te acompañaré "
                "en tu proceso de aprendizaje."
            ),
        }
    ]


# ---------------------------------------------------------
# Inicialización del Motor Pedagógico
# ---------------------------------------------------------

if "pedagogical_state" not in st.session_state:

    st.session_state.pedagogical_state = (
        initialize_pedagogical_state()
    )
if "activity_completed_cycle" not in st.session_state:
    st.session_state.activity_completed_cycle = False

if "identified_participant_id" not in st.session_state:
    st.session_state.identified_participant_id = None


# ---------------------------------------------------------
# Último evento pedagógico
# ---------------------------------------------------------

if "last_pedagogical_event" not in st.session_state:

    st.session_state.last_pedagogical_event = (
        "none"
    )

if "current_strategy" not in st.session_state:

    st.session_state.current_strategy = (
        "goal_setting"
    )
if "confirm_end_session" not in st.session_state:
    st.session_state.confirm_end_session = False


# ---------------------------------------------------------
# Identificación del participante
# ---------------------------------------------------------
if (
    "participant_id" not in st.session_state
    and st.session_state.identified_participant_id is None
):
    st.subheader(
        "Identificación del participante"
    )

    st.write(
        "Para acceder a tu historial en futuras sesiones, "
        "puedes generar un nuevo código de participante o "
        "utilizar uno que hayas recibido anteriormente."
    )

    access_mode = st.radio(
        "Selecciona una opción:",
        (
            "Nuevo participante",
            "Ya tengo un código",
        ),
        key="participant_access_mode",
    )

    # -----------------------------------------------------
    # Nuevo participante
    # -----------------------------------------------------

    if access_mode == "Nuevo participante":

        if (
            "pending_participant_id"
            not in st.session_state
        ):

            if st.button(
                "Generar código de participante"
            ):

                st.session_state[
                    "pending_participant_id"
                ] = create_participant()

                st.rerun()

        else:

            participant_code = (
                st.session_state[
                    "pending_participant_id"
                ]
            )

            st.success(
                "Tu código de participante "
                "ha sido generado."
            )

            st.code(
                participant_code,
                language=None,
            )

            st.warning(
                "Guarda este código. Lo necesitarás "
                "para acceder a tu historial "
                "en futuras sesiones."
            )

            if st.button(
                "Continuar"
            ):

                st.session_state.identified_participant_id = (
                    participant_code
                )

               
                del st.session_state[
                    "pending_participant_id"
                ]

                st.rerun()

    # -----------------------------------------------------
    # Participante existente
    # -----------------------------------------------------

    else:

        participant_code = st.text_input(
            "Código de participante",
            placeholder="P-xxxxxxxx",
        )

        if st.button(
            "Continuar con este código"
        ):

            participant_code = (
                participant_code.strip()
            )

            if not participant_code:
                st.error(
                    "Ingresa tu código de particpante"
                )
                
            elif participant_exists(
                participant_code
            ):
                st.session_state.identified_participant_id = (
                    participant_code
                )
                

                st.rerun()

            else:

                st.error(
                    "El código de participante "
                    "no existe."
                )

    st.stop()

# =====================================================
# VERIFICACIÓN DEL CONSENTIMIENTO
# =====================================================

identified_participant_id = (
    st.session_state.identified_participant_id
)

if identified_participant_id is not None:

    if has_valid_consent(
        identified_participant_id,
        CONSENT_VERSION,
    ):
        st.session_state.participant_id = (
            identified_participant_id
        )
        st.session_state.identified_participant_id = None
        st.rerun()
# =====================================================
# CONSENTIMIENTO INFORMADO
# =====================================================

if (
    st.session_state.identified_participant_id
    is not None
):

    st.subheader("Consentimiento informado")

    st.markdown(
        """
Has sido invitado(a) a participar en una investigación relacionada
con el uso de un **Tutor Metacognitivo basado en Inteligencia
Artificial Generativa y Analítica de Aprendizaje** como apoyo a los
procesos de autorregulación del aprendizaje en estudiantes
universitarios.

### ¿En qué consiste mi participación?

Si aceptas participar, realizarás un cuestionario inicial (**pretest**),
actividades académicas con el apoyo del tutor metacognitivo y,
posteriormente, un cuestionario final (**postest**).

### ¿Qué información registrará el sistema?

Durante las sesiones se registrará información derivada de tu
interacción con el tutor, como los mensajes intercambiados, número
de interacciones, duración de la sesión y otros rastros de interacción
necesarios para generar indicadores sobre el proceso desarrollado
durante las actividades.

### Confidencialidad

Para el funcionamiento del prototipo se utilizará un **código de
participante** en lugar de tu nombre dentro de los registros del
sistema.

La información recopilada será utilizada exclusivamente con fines
académicos y de investigación. Los resultados del estudio serán
presentados de manera agregada.

### Participación voluntaria

Tu participación es voluntaria. Puedes decidir no participar o
retirarte del estudio en cualquier momento, sin que ello implique
consecuencia alguna.

La participación no implica riesgos significativos previstos, aunque
requerirá tiempo para realizar las actividades y reflexionar sobre
tu propio proceso de aprendizaje.

Este prototipo tiene fines académicos y de investigación y
**no sustituye la orientación ni la evaluación de un docente.**

### Consentimiento

Al seleccionar la siguiente casilla, declaras que has leído y
comprendido la información presentada y que aceptas participar
de manera libre, informada y voluntaria.
"""
    )

    consent_checkbox = st.checkbox(
        "He leído la información anterior y acepto participar "
        "voluntariamente en el estudio."
    )

    if st.button(
        "Aceptar y continuar",
        type="primary",
        use_container_width=True,
    ):
        if consent_checkbox:
            participant_code = (
                st.session_state.identified_participant_id
            )

            if not has_valid_consent(
                participant_code,
                CONSENT_VERSION,
            ):
                save_participant_consent(
                    participant_code,
                    CONSENT_VERSION,
                )
            st.session_state.participant_id = (
                participant_code
            )
            st.session_state.identified_participant_id = None
            st.rerun()
        else:
            st.warning(
                "Para continuar debes confirmar que has leído "
                "la información y aceptas participar voluntariamente."
            )

    st.stop()

if "session_id" not in st.session_state:
    start_new_session()


# =========================================================
# SELECCIÓN DE ACTIVIDAD
# =========================================================

available_activities = get_available_activities()

activity_options = {
    activity["title"]: activity["activity_id"]
    for activity in available_activities
}

st.markdown("### 📚 Ejercicios para practicar ciclos")

selected_activity_title = st.selectbox(
    "Selecciona el ejercicio que deseas trabajar:",
    options=list(activity_options.keys()),
)

selected_activity_id = activity_options[selected_activity_title]

if "selected_activity_id" not in st.session_state:
    st.session_state.selected_activity_id = selected_activity_id
if st.session_state.selected_activity_id != selected_activity_id:

    previous_interaction_count = (
        st.session_state.pedagogical_state[
            "interaction_count"
        ]
    )

    st.session_state.pedagogical_state = (
        initialize_pedagogical_state()
    )

    st.session_state.pedagogical_state[
        "interaction_count"
    ] = previous_interaction_count
    st.session_state.activity_completed_cycle = False
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Has seleccionado un nuevo ejercicio. "
                "Antes de comenzar a programar, cuéntame cómo planeas abordarlo."
            ),
        }
    ]

    st.session_state.selected_activity_id = selected_activity_id
current_activity = get_activity(selected_activity_id)

st.markdown(
    f"""
### 📘 {current_activity["title"]}

**Tema:** {current_activity["topic"]}  
**Lenguaje:** {current_activity["programming_language"]}

{current_activity["statement"]}
"""
)
# ---------------------------------------------------------
# Mostrar historial conversacional
# ---------------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ---------------------------------------------------------
# Estado de sesión
# ---------------------------------------------------------

session_is_active = (
    st.session_state.session_data["status"]
    == "active"
)


# ---------------------------------------------------------
# Entrada del estudiante
# ---------------------------------------------------------

user_message = st.chat_input(
    (
        "Esta actividad ha concluido. "
        "Selecciona otro ejercicio para continuar."
        if st.session_state.activity_completed_cycle
        else "Cuéntame qué estás trabajando..."
    ),
    disabled=(
        not session_is_active
        or st.session_state.activity_completed_cycle
    ),
)


# ---------------------------------------------------------
# Procesamiento de interacción
# ---------------------------------------------------------

if user_message:

    # -----------------------------------------------------
    # Guardar mensaje
    # -----------------------------------------------------

    user_data = {
        "role": "user",
        "content": user_message,
    }

    st.session_state.messages.append(
        user_data
    )

    with st.chat_message("user", avatar="🎓"):

        st.markdown(
            user_message
        )

    # -----------------------------------------------------
    # Guardar estado antes de procesar la interacción
    # ---------------------------------------------------
    pedagogical_state_before = copy.deepcopy(
        st.session_state.pedagogical_state
    )
    
    last_event_before =(
        st.session_state.last_pedagogical_event
    )
    
    current_strategy_before = (
        st.session_state.current_strategy
    )
    # -----------------------------------------------------
    # Registrar interacción
    # -----------------------------------------------------

    st.session_state.pedagogical_state = (
        register_interaction(
            st.session_state.pedagogical_state
        )
    )


    # -----------------------------------------------------
    # Fase previa
    # -----------------------------------------------------

    phase_before = get_current_phase(
        st.session_state.pedagogical_state
    )
    if phase_before == "reflection":
        st.session_state.pedagogical_state = (
            register_reflection_interaction(
                st.session_state.pedagogical_state
            )
        )

    # -----------------------------------------------------
    # Detectar evidencia
    # -----------------------------------------------------

    classification_result = (
        classify_pedagogical_evidence(
            user_message
        )
    )

    classification_success = (
        classification_result["success"]
    )

    detected_event = (
        classification_result["event"]
    )

    if not classification_success:
        st.session_state.pedagogical_state =(
            pedagogical_state_before
        )
        st.session_state.last_pedagogical_event =(
            last_event_before
        )
        st.session_state.current_strategy =(
            current_strategy_before
        )
        save_technical_event(
            session_id=(
                st.session_state.session_id
            ),
            participant_id=(
                st.session_state.participant_id
            ),
            component="evidence_classifier",
            error_type=(
                classification_result[
                    "error_type"
                ]
            ),
            error_message=(
                classification_result[
                    "error_message"
                ]
            ),
        )
        st.warning(
            "No fue posible analizar tu mensaje"
            "en este momento. Intenta nuevamente"
        )
        st.stop()
                
    st.session_state.last_pedagogical_event = (
        detected_event
    )            
    # -----------------------------------------------------
    # Procesar evento
    # -----------------------------------------------------

    if detected_event != "none":

        st.session_state.pedagogical_state = (
            process_pedagogical_event(
                st.session_state.pedagogical_state,
                detected_event,
            )
        )


    # -----------------------------------------------------
    # Consultar estado actualizado
    # -----------------------------------------------------

    current_phase = get_current_phase(
        st.session_state.pedagogical_state
    )

    scaffolding_level = (
        get_scaffolding_level(
            st.session_state.pedagogical_state
        )
    )

    current_strategy = (
        select_metacognitive_strategy(
            phase=current_phase,
            scaffolding_level=scaffolding_level,
            pedagogical_event=detected_event,
        )
    )

    st.session_state.current_strategy = (
        current_strategy
    )

    reflection_completed = (
        current_phase == "reflection"
        and st.session_state.pedagogical_state[
            "reflection_count"
        ] >= 2
    )
    if reflection_completed:
        st.session_state.activity_completed_cycle = True
    if DEBUG_MODE:
        print(
            "DEBUG REFLECTION:",
            "phase_before =", phase_before,
            "| current_phase =", current_phase,
            "| reflection_count =",
            st.session_state.pedagogical_state[
                "reflection_count"
            ],
            "| completed =", reflection_completed,
        )
    # -----------------------------------------------------
    # Construir prompt
    # -----------------------------------------------------
    
    system_prompt = build_system_prompt(
        phase=current_phase,
        scaffolding_level=scaffolding_level,
        strategy=current_strategy,
        activity=current_activity,
    )
    if reflection_completed:
        system_prompt = """
            Eres un tutor metacognitivo que acompaña a estudiantes
            universitarios en su proceso de aprendizaje.

            El estudiante ya terminó la actividad y ha completado
            el proceso de reflexión sobre la estrategia utilizada
            y su posible aplicación futura.

            Cierra brevemente el acompañamiento pedagógico de esta
            actividad.

            Resume únicamente lo que el estudiante expresó sobre
            su estrategia y su posible aplicación futura.

            No evalúes su desempeño.
            No afirmes que tuvo éxito, que mejoró, que desarrolló
            una capacidad o que aprendió algo que no pueda observarse
            directamente en sus mensajes.
            No expreses satisfacción personal sobre su desempeño.

            No hagas ninguna pregunta.
            No solicites más reflexión.
            No propongas otra actividad.
            No continúes el proceso de tutoría.

            Termina la respuesta con esta indicación:
            "Has concluido el acompañamiento de esta actividad. Puedes seleccionar otro ejercicio para continuar o finalizar la sesión cuando lo desees."
            """
    else:
        system_prompt = build_system_prompt(
            phase=current_phase,
            scaffolding_level=scaffolding_level,
            strategy=current_strategy,
            activity=current_activity,
        )
    # -----------------------------------------------------
    # Generar respuesta
    # -----------------------------------------------------

    response_result = generate_response(
        st.session_state.messages,
        system_prompt,
    )

    tutor_response = response_result["content"]
    generation_success = response_result["success"]


    if not generation_success:

        st.session_state.pedagogical_state = (
            pedagogical_state_before
        )

        st.session_state.last_pedagogical_event = (
            last_event_before
        )

        st.session_state.current_strategy = (
            current_strategy_before
        )
        save_technical_event(
            session_id=(
                st.session_state.session_id
            ),
            participant_id=(
                st.session_state.participant_id
            ),
            component="response_generator",
            error_type=(
                response_result[
                    "error_type"
                ]
            ),
            error_message=(
                response_result[
                    "error_message"
                ]
            ),
        )
    # -----------------------------------------------------
    # Guardar respuesta
    # -----------------------------------------------------

    tutor_data = {
        "role": "assistant",
        "content": tutor_response,
    }

    st.session_state.messages.append(
        tutor_data
    )


    # -----------------------------------------------------
    # Guardar Learning Trace
    # -----------------------------------------------------
    if generation_success:
        save_learning_trace(

            session_id=(
                st.session_state.session_id
            ),

            interaction_number=(
                st.session_state.pedagogical_state[
                    "interaction_count"
                ]
            ),
            activity_id=(
                current_activity["activity_id"]
            ),
            student_message=(
                user_message
            ),

            tutor_response=(
                tutor_response
            ),

            phase_before=(
                phase_before
            ),

            phase_after=(
                current_phase
            ),

            pedagogical_event=(
                detected_event
            ),

            metacognitive_strategy=(
                current_strategy
            ),

            scaffolding_level=(
                scaffolding_level
            ),

            difficulty_count=(
                st.session_state.pedagogical_state[
                    "difficulty_count"
                ]
            ),
        )
        save_database_trace(

            session_id=(
                st.session_state.session_id
            ),

            interaction_number=(
                st.session_state.pedagogical_state[
                    "interaction_count"
                ]
            ),
            activity_id=(
                current_activity["activity_id"]
            ),

            student_message=(
                user_message
            ),

            tutor_response=(
                tutor_response
            ),

            phase_before=(
                phase_before
            ),

            phase_after=(
                current_phase
            ),

            pedagogical_event=(
                detected_event
            ),

            metacognitive_strategy=(
                current_strategy
            ),

            scaffolding_level=(
                scaffolding_level
            ),

            difficulty_count=(
                st.session_state.pedagogical_state[
                    "difficulty_count"
                ]
            ),
        )

    # -----------------------------------------------------
    # Mostrar respuesta
    # -----------------------------------------------------

    with st.chat_message(
        "assistant",
        avatar="🤖",
    ):

        st.markdown(
            tutor_response
        )


# ---------------------------------------------------------
# Barra lateral
# ---------------------------------------------------------
if DEBUG_MODE:
    with st.sidebar:

        st.subheader(
            "Estado pedagógico"
        )

        st.write(
            "Fase actual:",
            st.session_state.pedagogical_state[
                "phase"
            ],
        )

        st.write(
            "Nivel de scaffolding:",
            st.session_state.pedagogical_state[
                "scaffolding_level"
            ],
        )

        st.write(
            "Interacciones:",
            st.session_state.pedagogical_state[
                "interaction_count"
            ],
        )

        st.write(
            "Dificultades detectadas:",
            st.session_state.pedagogical_state[
                "difficulty_count"
            ],
        )

        st.write(
            "Último evento:",
            st.session_state.last_pedagogical_event,
        )
        st.write(
            "Estrategia actual:",
            st.session_state.current_strategy,
        )

        st.caption(
            "Panel temporal utilizado durante el "
            "desarrollo para verificar el funcionamiento "
            "del Motor Pedagógico."
        )

       
with st.sidebar:
    #st.divider()
    
    st.subheader(
        "Mi Sesión"
            )
    st.caption(
        "Información de tu sesión actual"
    )
    session_status = (
        st.session_state.session_data[
            "status"
        ]
    )


    # -----------------------------------------------------
    # Estado
    # -----------------------------------------------------

    if session_status == "active":

        st.success(
            "● Estado: En curso"
        )

    elif session_status == "closed":

        st.error(
            "● Estado: Finalizada"
        )

    else:
        st.warning(
            "● Estado: Interrumpida"
        )

    # -----------------------------------------------------
    # Inicio
    # -----------------------------------------------------

    start_time = (
        st.session_state.session_data[
            "start_time"
        ]
    )

    


    # -----------------------------------------------------
    # Duración
    # -----------------------------------------------------

    duration = (
    get_session_duration_seconds(
        st.session_state.session_data
    )
    )

    if duration < 60:

        duration_text = (
            f"{duration} s"
        )

    elif duration < 3600:

        minutes = duration // 60
        seconds = duration % 60

        duration_text = (
            f"{minutes} min {seconds} s"
        )

    else:

        hours = duration // 3600
        minutes = (
            duration % 3600
        ) // 60

        duration_text = (
            f"{hours} h {minutes} min"
        )

    time_col, duration_col = st.columns(2)
    with time_col:
        st.caption(
            "🕐 Inicio"
        )

        st.write(
            start_time.strftime(
                "%H:%M"
            )
        )
    with duration_col:
        st.caption(
             "⏱️ Duración"
        )
        st.write(
            duration_text
        )

    # -----------------------------------------------------
    # ID
    # -----------------------------------------------------
    if DEBUG_MODE:
        st.write(
            "ID de sesión:"
        )

        st.code(
            st.session_state.session_id,
            language=None,
        )
    
    st.write(
        "Código de participante:"
    )
    
    st.code(
        st.session_state.participant_id,
        language=None,
    )
    st.caption(
        "Conserva este código para acceder a tu "
        "historial en futuras sesiones."
    )


    # -----------------------------------------------------
    # Sesión activa
    # -----------------------------------------------------

    if session_status == "active":

        if st.button(
            "🛑 Finalizar sesión",
            use_container_width=True,
        ):

            '''st.session_state.session_data = (
                close_session(
                    st.session_state.session_data
                )
            )

            save_session_summary(

                session_state=(
                    st.session_state.session_data
                ),

                interaction_count=(
                    st.session_state.pedagogical_state[
                        "interaction_count"
                    ]
                ),

                difficulty_count=(
                    st.session_state.pedagogical_state[
                        "difficulty_count"
                    ]
                ),

                final_phase=(
                    st.session_state.pedagogical_state[
                        "phase"
                    ]
                ),
            )
            save_database_session_summary(
                session_state=(
                    st.session_state.session_data
                ),
                interaction_count=(
                    st.session_state.pedagogical_state[
                        "interaction_count"
                    ]
                ),
                difficulty_count=(
                    st.session_state.pedagogical_state[
                        "difficulty_count"
                    ]
                ),
                
                final_phase=(
                    st.session_state.pedagogical_state[
                        "phase"
                    ]
                ),
            )'''
            st.session_state.confirm_end_session = True
            st.rerun()

        if st.session_state.confirm_end_session:

            st.warning(
                "¿Seguro que deseas finalizar esta sesión? "
                "Después de finalizar no podrás enviar "
                "nuevos mensajes."
            )

            col_cancel, col_confirm = st.columns(2)

            with col_cancel:

                if st.button(
                    "Cancelar",
                    use_container_width=True,
                ):
                    st.session_state.confirm_end_session = False
                    st.rerun()

            with col_confirm:

                if st.button(
                    "Sí, finalizar",
                    use_container_width=True,
                ):

                    st.session_state.session_data = (
                        close_session(
                            st.session_state.session_data
                        )
                    )

                    save_session_summary(
                        session_state=(
                            st.session_state.session_data
                        ),
                        interaction_count=(
                            st.session_state.pedagogical_state[
                                "interaction_count"
                            ]
                        ),
                        difficulty_count=(
                            st.session_state.pedagogical_state[
                                "difficulty_count"
                            ]
                        ),
                        final_phase=(
                            st.session_state.pedagogical_state[
                                "phase"
                            ]
                        ),
                    )

                    save_database_session_summary(
                        session_state=(
                            st.session_state.session_data
                        ),
                        interaction_count=(
                            st.session_state.pedagogical_state[
                                "interaction_count"
                            ]
                        ),
                        difficulty_count=(
                            st.session_state.pedagogical_state[
                                "difficulty_count"
                            ]
                        ),
                        final_phase=(
                            st.session_state.pedagogical_state[
                                "phase"
                            ]
                        ),
                    )

                    st.session_state.confirm_end_session = False

                    st.rerun()
        st.caption(
            "Al finalizar la sesión no podrás "
            "enviar nuevos mensajes."
        )


    # -----------------------------------------------------
    # Sesión cerrada
    # -----------------------------------------------------

    else:

        st.warning(
            "✅La sesión ha finalizado. "
            "Has completado tu sesión con el Tutor Metacognitivo."
        )
        st.caption(
            "A continuación puedes revisar un resumen descriptivo "
            "de tu proceso durante esta sesión."
        )

        if st.button(
            "🔄 Nueva sesión",
            use_container_width=True,
        ):

            start_new_session()

            st.rerun()


# ---------------------------------------------------------
# DASHBOARD METACOGNITIVO
# ---------------------------------------------------------

if (
    st.session_state.session_data["status"]
    == "closed"
):

    st.divider()

    st.header(
        "📊 Resumen de la sesión"
    )


    # -----------------------------------------------------
    # Obtener analítica
    # -----------------------------------------------------

    metrics = calculate_session_metrics(
        st.session_state.session_id
    )

    profile = build_session_profile(
        st.session_state.session_id
    )

    feedback = generate_session_feedback(
        st.session_state.session_id
    )


    if metrics is not None:

        # -------------------------------------------------
        # Métricas principales
        # -------------------------------------------------

        col1, col2, col3, col4 = (
            st.columns(4)
        )

        with col1:

            st.metric(
                "Interacciones",
                metrics[
                    "interaction_count"
                ],
            )

        with col2:

            st.metric(
                "Dificultades",
                metrics[
                    "difficulty_count"
                ],
            )

        with col3:

            st.metric(
                "Duración",
                (
                    f'{metrics["duration_seconds"]} s'
                ),
            )

        with col4:

            st.metric(
                "Nivel máximo de apoyo",
                metrics[
                    "max_scaffolding_level"
                ],
            )


        # -------------------------------------------------
        # Etiquetas de fases
        # -------------------------------------------------

        phase_labels = {

            "planning":
                "Planeación",

            "monitoring":
                "Monitoreo",

            "control":
                "Control",

            "reflection":
                "Reflexión",
        }


        # -------------------------------------------------
        # Trayectoria
        # -------------------------------------------------

        phase_path = (
            metrics["phase_path"]
        )

        if phase_path:

            st.subheader(
                "Trayectoria metacognitiva"
            )

            trajectory = " → ".join(

                phase_labels.get(
                    phase,
                    phase,
                )

                for phase
                in phase_path
            )

            st.write(
                trajectory
            )


        # -------------------------------------------------
        # Distribución por fase
        # -------------------------------------------------

        phase_distribution = (
            metrics[
                "phase_distribution"
            ]
        )

        if phase_distribution:

            st.subheader(
                "Distribución de "
                "interacciones por fase"
            )

            phase_df = pd.DataFrame(
                {
                    "Fase": [

                        phase_labels.get(
                            phase,
                            phase,
                        )

                        for phase
                        in phase_distribution.keys()
                    ],

                    "Interacciones": list(
                        phase_distribution.values()
                    ),
                }
            )

            st.bar_chart(
                phase_df,
                x="Fase",
                y="Interacciones",
            )


        # -------------------------------------------------
        # Perfil de sesión
        # -------------------------------------------------

        if profile is not None:

            st.subheader(
                "Perfil de la sesión"
            )

            difficulty_labels = {
                "none": "Sin dificultades registradas",
                "low": "Bajo",
                "moderate": "Moderado",
                "high": "Alto",
            }

            support_labels = {
                "minimal": "Mínimo",
                "moderate": "Moderado",
                "high": "Alto",
                "intensive": "Intensivo",
            }

            st.write(
                "Dificultades durante la sesión:",
                difficulty_labels.get(
                    profile[
                        "difficulty_level"
                    ],
                    profile[
                        "difficulty_level"
                    ],
                ),
            )

            st.write(
                "Nivel de apoyo:",
                support_labels.get(
                    profile[
                        "support_level"
                    ],
                    profile[
                        "support_level"
                    ],
                ),
            )

            st.write(
                "Fase al finalizar:",
                phase_labels.get(
                    profile[
                        "final_phase"
                    ],
                    profile[
                        "final_phase"
                    ],
                ),
            )

            st.write(
                "Cambios de fase:",
                profile[
                    "phase_transition_count"
                ],
            )


        # -------------------------------------------------
        # Retroalimentación
        # -------------------------------------------------

        if feedback is not None:

            st.subheader(
                "Retroalimentación metacognitiva"
            )

            st.info(
                feedback
            )
        if (
            st.session_state.session_data["status"]
            == "closed"
        ):
        # ---------------------------------------------------------
        # ANALÍTICA LONGITUDINAL
        # ---------------------------------------------------------

            st.divider()

            st.header(
                "📈 Evolución entre sesiones"
            )

            longitudinal_metrics = (
                calculate_longitudinal_metrics(
                    st.session_state.participant_id
                )
            )

            session_changes = (
                calculate_session_changes(
                    st.session_state.participant_id
                )
            )

            longitudinal_feedback = (
                generate_longitudinal_feedback(
                    st.session_state.participant_id
                )
            )


            # ---------------------------------------------------------
            # Verificar disponibilidad de evidencia longitudinal
            # ---------------------------------------------------------

            if (
                longitudinal_metrics is None
                or not longitudinal_metrics[
                    "has_longitudinal_evidence"
                ]
            ):

                st.info(
                    "Todavía no hay suficientes sesiones "
                    "con evidencia de aprendizaje para realizar "
                    "una comparación longitudinal. "
                    "Se requieren al menos dos sesiones "
                    "analizables."
                )

            else:

                sessions = longitudinal_metrics[
                    "sessions"
                ]

                st.write(
                    "Sesiones con actividad registrada: ",
                    longitudinal_metrics[
                        "session_count"
                    ],
                )

                # -----------------------------------------------------
                # Tabla histórica
                # -----------------------------------------------------

                st.subheader(
                    "Historial de sesiones"
                )

                longitudinal_rows = []

                phase_labels_longitudinal = {
                    "planning": "Planeación",
                    "monitoring": "Monitoreo",
                    "control": "Control",
                    "reflection": "Reflexión",
                }

                for index, session in enumerate(
                    sessions,
                    start=1,
                ):

                    longitudinal_rows.append(
                        {
                            "Sesión": index,
                            "Interacciones": (
                                session[
                                    "interaction_count"
                                ]
                            ),
                            "Dificultades": (
                                session[
                                    "difficulty_count"
                                ]
                            ),
                            "Interacciones con dificultad (%)": (
                                session[
                                    "difficulty_rate"
                                ]
                            ),
                            "Nivel máximo de apoyo": (
                                session[
                                    "max_scaffolding_level"
                                ]
                            ),
                            "Cambios de fase": (
                                session[
                                    "phase_transition_count"
                                ]
                            ),
                            "Fase al finalizar": (
                                phase_labels_longitudinal.get(
                                    session[
                                        "final_phase"
                                    ],
                                    session[
                                        "final_phase"
                                    ],
                                )
                            ),
                        }
                    )

                longitudinal_df = pd.DataFrame(
                    longitudinal_rows
                )

                st.dataframe(
                    longitudinal_df,
                    use_container_width=True,
                    hide_index=True,
                )


                # -----------------------------------------------------
                # Evolución de la tasa de dificultad
                # -----------------------------------------------------

                st.subheader(
                    "Interacciones con dificultad"
                )

                difficulty_chart_df = (
                    longitudinal_df[
                        [
                            "Sesión",
                            "Interacciones con dificultad (%)",
                        ]
                    ]
                    .set_index(
                        "Sesión"
                    )
                )

               
                difficulty_figure = px.line(
                    longitudinal_df,
                    x="Sesión",
                     y="Interacciones con dificultad (%)",
                    markers=True,
                )
                difficulty_figure.update_layout(
                    xaxis_title="Sesión",
                    yaxis_title="Interacciones con dificultad (%)",
                )

                difficulty_figure.update_xaxes(
                    tickmode="linear",
                    dtick=1,
                )

                difficulty_figure.update_yaxes(
                    range=[0, 100],
                )

                st.plotly_chart(
                    difficulty_figure,
                    use_container_width=True,
                )
                


                # -----------------------------------------------------
                # Evolución del scaffolding
                # -----------------------------------------------------

                st.subheader(
                    "Nivel máximo de apoyo"
                )

                scaffolding_chart_df = (
                    longitudinal_df[
                        [
                            "Sesión",
                            "Nivel máximo de apoyo",
                        ]
                    ]
                    .set_index(
                        "Sesión"
                    )
                )

                scaffolding_figure = px.line(
                    longitudinal_df,
                    x="Sesión",
                    y="Nivel máximo de apoyo",
                    markers=True,
                )

                scaffolding_figure.update_layout(
                    xaxis_title="Sesión",
                    yaxis_title="Nivel máximo de apoyo",
                )

                scaffolding_figure.update_xaxes(
                    tickmode="linear",
                    dtick=1,
                )

                scaffolding_figure.update_yaxes(
                    range=[0, 4],
                    tickmode="linear",
                    dtick=1,
                )

                st.plotly_chart(
                    scaffolding_figure,
                    use_container_width=True,
                )


                # -----------------------------------------------------
                # Cambios entre las sesiones más recientes
                # -----------------------------------------------------

                if (
                    session_changes is not None
                    and session_changes[
                        "comparisons"
                    ]
                ):

                    latest_change = (
                        session_changes[
                            "comparisons"
                        ][-1]
                    )

                    st.subheader(
                        "Cambios observados entre las "
                        "dos sesiones más recientes"
                    )

                    col1, col2  = (
                        st.columns(2)
                    )

                    with col1:

                        st.metric(
                            "Cambio en dificultades",
                            (
                                f'{latest_change["difficulty_rate_change"]} '
                                "puntos"
                            ),
                        )

                    with col2:

                        st.metric(
                            "Cambio en nivel de apoyo",
                            latest_change[
                                "scaffolding_change"
                            ],
                        )
                    col3, col4 = (
                        st.columns(2)
                    )
                    with col3:

                        st.metric(
                            "Cambio en interacciones",
                            latest_change[
                                "interaction_change"
                            ],
                        )

                    with col4:

                        st.metric(
                            "Cambio en transiciones de fase",
                            latest_change[
                                "transition_change"
                            ],
                        )

                    previous_phase = (
                        phase_labels_longitudinal.get(
                            latest_change[
                                "previous_final_phase"
                            ],
                            latest_change[
                                "previous_final_phase"
                            ],
                        )
                    )

                    current_phase = (
                        phase_labels_longitudinal.get(
                            latest_change[
                                "current_final_phase"
                            ],
                            latest_change[
                                "current_final_phase"
                            ],
                        )
                    )

                    st.write(
                        "Fase entre sesiones:",
                        f"{previous_phase} → {current_phase}",
                    )


                # -----------------------------------------------------
                # Retroalimentación longitudinal
                # -----------------------------------------------------

                if longitudinal_feedback is not None:

                    st.subheader(
                        "Retroalimentación longitudinal"
                    )

                    st.info(
                        longitudinal_feedback
                    )