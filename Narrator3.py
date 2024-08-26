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

# Función para ir imprimiendo la estructura del personaje en el log
def Print_Character_Structure(CharacterPrincipal):
    logging.info(f"\t Estructura del personaje {CharacterPrincipal.name}:")
    logging.info(f"\t\t Nombre: {CharacterPrincipal.name}")
    logging.info(f"\t\t Ubicación: {CharacterPrincipal.location}")
    logging.info(f"\t\t Estado de seguridad: {CharacterPrincipal.conditionsafety}")

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

    Print_Character_Structure(CharacterSelected)
    
    return CharacterSelected

CharacterPrincipal = Select_Character()

# Función para crear las metas y acciones del personaje principal en la historia
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

    Plan_Find_Keys = [
        StoryAction(
            "Buscar llaves en el cajón",
            CharacterPrincipal,
            ["Baño"],
            ["Baño","Llaves encontradas"],
            [f"{CharacterPrincipal.name} busca en el cajón y encuentra las llaves.",
            f"{CharacterPrincipal.name} abre el cajón y ve las llaves allí."]
        ),
        StoryAction(
            "Buscar llaves pegadas a la puerta",
            CharacterPrincipal,
            ["Baño"],
            ["Baño","Llaves encontradas"],
            [f"{CharacterPrincipal.name} encuentra las llaves pegadas a la puerta.",
            f"{CharacterPrincipal.name} ve que las llaves están pegadas a la puerta."]
        ),
        StoryAction(
            "Buscar llaves pero no encuentra ninguna",
            CharacterPrincipal,
            ["Baño"],
            ["Inseguro","Llaves no encontradas"],
            [f"{CharacterPrincipal.name} busca por todo el baño pero no encuentra las llaves.",
            f"{CharacterPrincipal.name} revisa todo el baño pero no hay señales de las llaves."]
        ),
    ]

    # Selección aleatoria de la acción para encontrar las llaves
    Plan_Find_Keys = [random.choice(Plan_Find_Keys)]

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

    # Todas las acciones disponibles, incluyendo las alternativas
    all_actions = Plan_Pre + Plan_End + Plan_Find_Keys 

    # Meta Pre: Mover al personaje a adentro del baño
    # Meta End: Bloquear la puerta del baño para estar a salvo
    # Meta Find_Keys: Encontrar las llaves en el baño
    Goal_Pre = Goal("Mover al personaje a adentro del baño", CharacterPrincipal, None, Plan_Pre)
    Goal_Find_Keys = Goal("Encontrar las llaves en el baño", CharacterPrincipal, Goal_Pre, Plan_Find_Keys)
    Goal_End = Goal("Bloquear la puerta del baño para estar a salvo", CharacterPrincipal, Goal_Find_Keys, Plan_End)

    # Diccionario de metas
    Dict_Goals = {
        "Goal_Pre": Goal_Pre,
        "Goal_Find_Keys": Goal_Find_Keys,
        "Goal_End": Goal_End

    }

    logging.info("Se crean las metas")
    logging.info(f"Meta Pre: {Goal_Pre.name}")
    logging.info(f"Meta Find_Keys: {Goal_Find_Keys.name}")
    logging.info(f"Meta End: {Goal_End.name}")

    return Dict_Goals, all_actions

# Crear metas y acciones 
Dict_Goals, all_actions = Create_Goals(CharacterPrincipal)

# Función para seleccionar la meta inicial de la historia
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

# Seleccionar la meta inicial
Goal_Current = Select_Goal(Dict_Goals)

logging.info("Se inicia la narración de la historia")
logging.info(f"Personaje principal: {CharacterPrincipal.name}")
logging.info(f"Meta actual: {Goal_Current.name}")

    

# Funcion para verificar si se cumplen las precondiciones de una acción o meta 
def Check_Preconditions(preconditions, CharacterPrincipal):
    logging.info("\tSe inicia la verificación de precondiciones")
    return CharacterPrincipal.location in preconditions

# Función para verificar si se ha alcanzado la meta actual 
def is_goal_achieved(goal, character):
    # Verificar si la meta de bloquear la puerta del baño se ha alcanzado
    if goal.name == "Bloquear la puerta del baño para estar a salvo" and character.location == "Baño" and character.conditionsafety == "A salvo":
        return True
    # Verificar si la meta de moverse al baño se ha alcanzado
    elif goal.name == "Mover al personaje a adentro del baño" and character.location == "Baño":
        return True
    elif goal.name == "Encontrar las llaves en el baño" and character.location == "Baño":
        return True
    return False

# Función para actualizar el estado de seguridad del personaje si se bloquea la puerta del baño
def update_safety_status(character, action):
    if character.location == "Baño" and character.conditionsafety != "A salvo" and action.name == "Bloquear la puerta del baño":
        character.conditionsafety = "A salvo"
        logging.info(f"{character.name} ahora está a salvo.")

# Función para encontrar la siguiente acción a ejecutar si no se cumplen las precondiciones de la acción actual 
def find_next_action(all_actions, character):
    for action in all_actions:
        if Check_Preconditions(action.preconditions, character):
            return action
    return None

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
            
            # Verificar si no se encuentra ninguna llave en el baño para no 
            # poder bloquear la puerta del baño
            if action.name == "Buscar llaves pero no encuentra ninguna" and action.postconditions[1] == "Llaves no encontradas":
                logging.info(f"No se pueden ejecutar más acciones, ya que no se encontraron las llaves.")
                return
            
        else:
            logging.info(f"No se puede ejecutar la acción: {action.name} debido a precondiciones no cumplidas.")
            next_action = find_next_action(all_actions, CharacterPrincipal)
            if next_action:
                logging.info(f"Se ejecuta una acción alternativa: {next_action.name}")
                description = random.choice(next_action.descriptions)
                logging.info(f"Ejecutando acción: {next_action.name}")
                logging.info(f"{CharacterPrincipal.name} se encuentra {CharacterPrincipal.conditionsafety}.")
                CharacterPrincipal.location = next_action.postconditions[0]
                print(description)
                logging.info(description)
                logging.info(f"{CharacterPrincipal.name} ahora está en {CharacterPrincipal.location}")
                Execute_Plan(Goal_Current, CharacterPrincipal)  # Continuar con el plan original después de ejecutar la acción alternativa
                return
            return
        Print_Character_Structure(CharacterPrincipal)

    # Verificar si la meta se ha alcanzado
    if is_goal_achieved(Goal_Current, CharacterPrincipal):
        logging.info(f"Meta alcanzada: {Goal_Current.name}")
    else:
        #print(f"{CharacterPrincipal.name} no ha alcanzado la meta.")
        logging.info(f"{CharacterPrincipal.name} no ha alcanzado la meta.")

Execute_Plan(Goal_Current, CharacterPrincipal)
