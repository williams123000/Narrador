import random
import logging
import datetime
import os

# Crear el directorio de logs si no existe
log_directory = 'logs'
os.makedirs(log_directory, exist_ok=True)

# Generar un nombre de archivo único basado en la fecha y hora actuales
log_filename = os.path.join(log_directory, datetime.datetime.now().strftime("Narrator_%Y%m%d_%H%M%S.log"))

# Configuración de los logs para guardar la información en un archivo de texto
logging.basicConfig(
    filename=log_filename,
    filemode='w',
    level=logging.DEBUG,
    format='%(asctime)s - %(message)s',
    encoding='utf-8'
)

logging.info("Inicio de la ejecución del programa Narrator.py")
logging.info("Programa escrito por Williams Chan Pescador")

# Lista de ubicaciones
Locations = ["Recamara", "Inicio del pasillo", "Final del pasillo", "Baño"]

# Clase de personaje con sus atributos (nombre, ubicación y estado de seguridad)
class Character:
    def __init__(self, name, location, conditionsafety):
        self.name = name
        self.location = location
        self.conditionsafety = conditionsafety

# Clase de acción con sus atributos (nombre, personaje, precondiciones, postcondiciones y descripciones)
class StoryAction:
    def __init__(self, name, character, preconditions, postconditions, descriptions):
        self.name = name
        self.character = character
        self.preconditions = preconditions
        self.postconditions = postconditions
        self.descriptions = descriptions  # Lista de descripciones posibles

# Clase de meta con sus atributos (nombre, personaje, precondiciones y plan)
class Goal:
    def __init__(self, name, character, preconditions, plan):
        self.name = name
        self.character = character
        self.preconditions = preconditions
        self.plan = plan

# Función para seleccionar el personaje principal de la historia
def Select_Character():
    global Locations

    logging.info("Se inicia el proceso de selección del personaje principal")

    num_characters = int(input("Ingrese el número de personajes: "))

    listCharacters = []
    
    print("Opciones de ubicaciones:")
    for i, location in enumerate(Locations):
        print(f"{i}. {location}")

    for i in range(num_characters):
        name = input(f"Ingrese el nombre del personaje {i+1}: ")
        location_index = int(input(f"Ingrese el número de ubicación para {name}: "))
        location = Locations[location_index]
        conditionsafety = "Inseguro"  # Por defecto, todos los personajes empiezan inseguros
        character = Character(name, location, conditionsafety)
        listCharacters.append(character)

    CharacterSelected = random.choice(listCharacters)

    logging.info("Estado actual del mundo del cuento")
    logging.info(f"\t Estructura del personaje {CharacterSelected.name}:")
    logging.info(f"\t\t Nombre: {CharacterSelected.name}")
    logging.info(f"\t\t Ubicación: {CharacterSelected.location}")
    logging.info(f"\t\t Estado de seguridad: {CharacterSelected.conditionsafety}")
    
    return CharacterSelected

CharacterPrincipal = Select_Character()

def Create_Goals(CharacterPrincipal):    
    # Planes de acción para mover al personaje principal a adentro del baño
    Plan_Pre = [
        StoryAction(
            "Caminar hacia el inicio del pasillo", 
            CharacterPrincipal, 
            ["Recamara", "Final del pasillo"], 
            ["Inicio del pasillo"],
            [f"{CharacterPrincipal.name} avanza cautelosamente hacia el inicio del pasillo,",
            f"{CharacterPrincipal.name} con paso firme, se dirige al inicio del pasillo,",
            f"{CharacterPrincipal.name} siente miedo y decide avanzar hacia el inicio del pasillo,",
            f"{CharacterPrincipal.name} avanza con rapidez hacia el inicio del pasillo,",
            f"{CharacterPrincipal.name} escucha ruidos extraños en la recámara, y decide avanzar hacia el inicio del pasillo,",
            f"{CharacterPrincipal.name} se siente inseguro, y decide avanzar hacia el inicio del pasillo,"]
        ),
        StoryAction(
            "Caminar hacia el final del pasillo", 
            CharacterPrincipal, 
            ["Inicio del pasillo", "Baño"], 
            ["Final del pasillo"],
            ["con mucho miedo se dirige hacia el final del pasillo,", 
            "con cautela se dirige hacia el final del pasillo,",
            "intenta avanzar hacia el final del pasillo, pero siente miedo,"]
        ),
        StoryAction(
            "Entrar al baño", 
            CharacterPrincipal, 
            ["Final del pasillo"], 
            ["Baño"],
            ["abre la puerta del baño y entra en él,", 
            "con cuidado, abre la puerta del baño y entra,", 
            "con decisión, entra en el baño,"]
        ),
    ]

    # Planes de acción para bloquear la puerta del baño
    Plan_End = [
        StoryAction(
            "Bloquear la puerta del baño", 
            CharacterPrincipal, 
            ["Baño"], 
            ["Baño","A salvo"],  
            ["bloquea la puerta del baño, asegurando su seguridad.", 
            "asegura la puerta del baño con un movimiento decidido.",
            "bloquea la puerta del baño para estar a salvo.",
            "bloquea la puerta del baño para protegerse."]
        )
    ]

    # Meta Pre: Mover al personaje a adentro del baño
    # Meta End: Bloquear la puerta del baño para estar a salvo
    Goal_Pre = Goal("Mover al personaje a adentro del baño", CharacterPrincipal, None, Plan_Pre)
    Goal_End = Goal("Bloquear la puerta del baño para estar a salvo", CharacterPrincipal, Goal_Pre, Plan_End)

    # Diccionario de metas
    Dict_Goals = {
        "Goal_Pre": Goal_Pre,
        "Goal_End": Goal_End
    }

    logging.info("Se crean las metas")
    logging.info(f"Meta Pre: {Goal_Pre.name}")
    logging.info(f"Meta End: {Goal_End.name}")

    return Dict_Goals

Dict_Goals = Create_Goals(CharacterPrincipal)

# Diccionario de acciones alternativas para ejecutar en caso de que no se cumplan las precondiciones de 
# las acciones principales del plan
new_actions = [
    StoryAction(
        "Caminar hacia la recámara",
        CharacterPrincipal,
        ["Inicio del pasillo"],
        ["Recamara"],
        [f"{CharacterPrincipal.name} avanza hacia la recámara,",
        f"{CharacterPrincipal.name} se dirige hacia la recámara,",
        f"{CharacterPrincipal.name} se regresa a la recámara,",
        f"{CharacterPrincipal.name} se siente tranquilo en la recámara,"]
    ),
    # Más acciones alternativas en caso de que no se cumplan las precondiciones de las acciones principales
]

def Select_Goal(Dict_Goals):
    print("Opciones de metas:")
    print("0. Mover al personaje a adentro del baño")
    print("1. Bloquear la puerta del baño para estar a salvo")
    goal_index = int(input("Seleccione el número de la meta inicial: "))
    
    if goal_index == 0:
        Goal_Current = Dict_Goals["Goal_Pre"]
    elif goal_index == 1:
        Goal_Current = Dict_Goals["Goal_End"]
    else:
        print("Selección inválida, se seleccionará la meta predeterminada (Mover al personaje a adentro del baño)")
        Goal_Current = Dict_Goals["Goal_Pre"]
    
    return Goal_Current

Goal_Current = Select_Goal(Dict_Goals)

logging.info("Se inicia la narración de la historia")
logging.info(f"Personaje principal: {CharacterPrincipal.name}")
logging.info(f"Meta actual: {Goal_Current.name}")

def Check_Preconditions(preconditions, CharacterPrincipal):
    logging.info("\tSe inicia la verificación de precondiciones")
    logging.info(f"\t\tUbicación actual del personaje: {CharacterPrincipal.location}")
    return CharacterPrincipal.location in preconditions

def is_goal_achieved(goal, character):
    # Verificar si la meta de bloquear la puerta del baño se ha alcanzado
    if goal.name == "Bloquear la puerta del baño para estar a salvo" and character.location == "Baño" and character.conditionsafety == "A salvo":
        return True
    # Verificar si la meta de moverse al baño se ha alcanzado
    elif goal.name == "Mover al personaje a adentro del baño" and character.location == "Baño":
        return True
    return False

def update_safety_status(character, action):
    if character.location == "Baño" and character.conditionsafety != "A salvo" and action.name == "Bloquear la puerta del baño":
        character.conditionsafety = "A salvo"
        logging.info(f"{character.name} ahora está a salvo.")


def Execute_Plan(Goal_Current, CharacterPrincipal):
    # Verificar si hay precondiciones para la meta actual y ejecutar la meta previa si es necesario
    if Goal_Current.preconditions:
        logging.info(f"Verificando precondiciones para la meta: {Goal_Current.name}")
        # Verificar si se cumplen las precondiciones de la meta actual y ejecutar la meta previa si no se cumplen las precondiciones 
        if not Check_Preconditions(Goal_Current.preconditions.plan[0].postconditions, CharacterPrincipal):
            logging.info(f"Las precondiciones para la meta {Goal_Current.name} no se cumplen.")
            logging.info(f"Ejecutando la meta previa: {Goal_Current.preconditions.name}")
            Execute_Plan(Goal_Current.preconditions, CharacterPrincipal)
    
    logging.info(f"Ejecutando el plan para la meta: {Goal_Current.name}")
    plan = Goal_Current.plan
    for action in plan:
        if Check_Preconditions(action.preconditions, CharacterPrincipal):
            description = random.choice(action.descriptions)
            logging.info(f"\t\tEjecutando acción: {action.name}")
            logging.info(f"{CharacterPrincipal.name} se encuentra {CharacterPrincipal.conditionsafety}.")
            CharacterPrincipal.location = action.postconditions[0]
            print(description)
            logging.info(description)
            logging.info(f"{CharacterPrincipal.name} ahora está en {CharacterPrincipal.location}")

            update_safety_status(CharacterPrincipal, action) # Actualizar el estado de seguridad del personaje
        else:
            logging.info(f"No se puede ejecutar la acción: {action.name} debido a precondiciones no cumplidas.")
            for new_action in new_actions:
                if Check_Preconditions(new_action.preconditions, CharacterPrincipal):
                    logging.info(f"Se ejecuta una nueva acción alternativa: {new_action.name}")
                    description = random.choice(new_action.descriptions)
                    logging.info(f"Ejecutando acción: {new_action.name}")
                    logging.info(f"{CharacterPrincipal.name} se encuentra {CharacterPrincipal.conditionsafety}.")
                    CharacterPrincipal.location = new_action.postconditions[0]
                    print(description)
                    logging.info(description)
                    logging.info(f"{CharacterPrincipal.name} ahora está en {CharacterPrincipal.location}")
                    logging.info(f"\t Estructura del personaje {CharacterPrincipal.name}:")
                    logging.info(f"\t\t Nombre: {CharacterPrincipal.name}")
                    logging.info(f"\t\t Ubicación: {CharacterPrincipal.location}")
                    logging.info(f"\t\t Estado de seguridad: {CharacterPrincipal.conditionsafety}")
                    Execute_Plan(Goal_Current, CharacterPrincipal) # Llamar recursivamente a la función para continuar con el plan de la meta actual
                    return
            return
        logging.info(f"\t Estructura del personaje {CharacterPrincipal.name}:")
        logging.info(f"\t\t Nombre: {CharacterPrincipal.name}")
        logging.info(f"\t\t Ubicación: {CharacterPrincipal.location}")
        logging.info(f"\t\t Estado de seguridad: {CharacterPrincipal.conditionsafety}")

    # Verificar si la meta se ha alcanzado
    if is_goal_achieved(Goal_Current, CharacterPrincipal):
        #print("Fin de la historia")
        logging.info(f"Meta alcanzada: {Goal_Current.name}")
        #logging.info("Fin de la historia")
    else:
        print(f"{CharacterPrincipal.name} no ha alcanzado la meta.")
        logging.info(f"{CharacterPrincipal.name} no ha alcanzado la meta.")


Execute_Plan(Goal_Current, CharacterPrincipal)