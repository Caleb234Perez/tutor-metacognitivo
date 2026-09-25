ACTIVITIES = {
    "loops_01": {
        "activity_id": "loops_01",
        "title": "Suma hasta cincuenta",
        "topic": "Ciclos",
        "programming_language": "C",
        "statement": (
            "Crea una variable que se llame total, después pide a tu usuario "
            "que ingrese un número y lo sume al valor de total. Haz que esto "
            "se repita hasta que el valor de total sea mayor a 50 y muestra "
            "el resultado en pantalla."
        ),
        "difficulty": "basic",
    },

    "loops_02": {
        "activity_id": "loops_02",
        "title": "Más allá del cuarenta y dos",
        "topic": "Ciclos",
        "programming_language": "C",
        "statement": (
            "Crea un código que pida al usuario un número y se repita hasta "
            "que coloque un número mayor a 42. Cuando se cumpla esta condición "
            "muestra el resultado en pantalla indicando esto al usuario y "
            "finaliza el ciclo."
        ),
        "difficulty": "basic",
    },

    "loops_03": {
        "activity_id": "loops_03",
        "title": "Sumas consecutivas",
        "topic": "Ciclos",
        "programming_language": "C",
        "statement": (
            "Pide al usuario que ingrese dos números y los sume. Después "
            "pregunta si quiere añadir otro número: si la respuesta es "
            "afirmativa añádelo al total; en caso contrario finaliza el ciclo "
            "y muestra el resultado total en pantalla."
        ),
        "difficulty": "basic",
    },

    "loops_04": {
        "activity_id": "loops_04",
        "title": "Lista de invitados",
        "topic": "Ciclos",
        "programming_language": "C",
        "statement": (
            "Estás organizando un banquete al que quieres invitar a tus amigos. "
            "Crea un programa que pida el nombre de uno de tus amigos, al hacerlo "
            "aumenta en uno una variable contadora, después pregunta si quieres "
            "invitar a alguien más: si la respuesta es afirmativa entonces "
            "pregunta por una persona más; en caso contrario cierra el ciclo "
            "y muestra en pantalla cuantos invitados son."
        ),
        "difficulty": "basic",
    },

    "loops_05": {
        "activity_id": "loops_05",
        "title": "Adivina el número secreto",
        "topic": "Ciclos",
        "programming_language": "C",
        "statement": (
            "Crea un programa donde tendrás la variable numero_secreto, la cual "
            "toma un valor aleatorio entre 1 y 100. Después pide a tu usuario "
            "que indique un número para intentar adivinarlo: en caso de acertar "
            "indícale cual era el número secreto y cuantos intentos le tomó; "
            "en caso contrario indícale si el número ingresado es mayor o menor "
            "al número secreto."
        ),
        "difficulty": "intermediate",
    },

    "loops_06": {
        "activity_id": "loops_06",
        "title": "Un elefante se balanceaba…",
        "topic": "Ciclos",
        "programming_language": "C",
        "statement": (
            "Escribe un programa que inicie mostrando en pantalla la letra de "
            "“Un elefante se balanceaba” iniciando con el número 1, después "
            "pregunta al usuario cuantos elefantes más se balancearán y debe "
            "responder un número más al mostrado. En caso de ingresar un número "
            "diferente pedirle que intente de nuevo y repetir el ciclo hasta "
            "tener 10 elefantes. Tomar en cuenta cuando el texto muestra un solo "
            "elefante y varios elefantes."
        ),
        "difficulty": "intermediate",
    },

    "loops_07": {
        "activity_id": "loops_07",
        "title": "Mi edad",
        "topic": "Ciclos",
        "programming_language": "C",
        "statement": (
            "Escribir un programa que pregunte al usuario su edad y muestre "
            "por pantalla todos los años que ha cumplido (desde 1 hasta su edad)."
        ),
        "difficulty": "basic",
    },

    "loops_08": {
        "activity_id": "loops_08",
        "title": "Intereses",
        "topic": "Ciclos",
        "programming_language": "C",
        "statement": (
            "Escribir un programa que pregunte al usuario una cantidad a invertir, "
            "el interés anual y el número de años, y muestre por pantalla el capital "
            "obtenido en la inversión cada año que dura la inversión."
        ),
        "difficulty": "intermediate",
    },

    "loops_09": {
        "activity_id": "loops_09",
        "title": "Triángulos de *",
        "topic": "Ciclos",
        "programming_language": "C",
        "statement": (
            "Escribir un programa que pida al usuario un número entero y muestre "
            "por pantalla un triángulo rectángulo de asteriscos cuya altura sea "
            "el número introducido."
        ),
        "difficulty": "intermediate",
    },

    "loops_10": {
        "activity_id": "loops_10",
        "title": "Triángulos de dígitos",
        "topic": "Ciclos",
        "programming_language": "C",
        "statement": (
            "Escribir un programa que pida al usuario un número entero y muestre "
            "por pantalla un triángulo rectángulo de dígitos siguiendo el patrón "
            "indicado en el ejercicio."
        ),
        "difficulty": "intermediate",
    },

    "loops_11": {
        "activity_id": "loops_11",
        "title": "Contraseña",
        "topic": "Ciclos",
        "programming_language": "C",
        "statement": (
            "Escribir un programa que almacene la cadena de caracteres contraseña "
            "en una variable, pregunte al usuario por la contraseña hasta que "
            "introduzca la contraseña correcta."
        ),
        "difficulty": "basic",
    },

    "loops_12": {
        "activity_id": "loops_12",
        "title": "Primos",
        "topic": "Ciclos",
        "programming_language": "C",
        "statement": (
            "Escribir un programa que pida al usuario un número entero y muestre "
            "por pantalla si es un número primo o no."
        ),
        "difficulty": "intermediate",
    },
}


def get_activity(activity_id):
    """
    Recupera una actividad mediante su identificador.
    """
    return ACTIVITIES.get(activity_id)


def get_available_activities():
    """
    Devuelve la lista de actividades disponibles.
    """
    return list(ACTIVITIES.values())