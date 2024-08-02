#Narrador automático
#Autor: Williams Chan Pescador

import random
import logging

#Configuración de los logs para guardar la información en un archivo de texto 
logging.basicConfig(filename='Narrador.log' ,filemode='w',level=logging.DEBUG, format='%(asctime)s - %(message)s')

#Listas de ubicaciones 
listLocationCharacter = ["Recamara", "Inicio del pasillo", "Final del pasillo", "Baño"]

#Diccionario de ubicaciones para la narración de la historia 
dictLocations = {
    "Recamara": ["la recamara", "su recamara", "la recamara de su casa", "su recamara de su casa"],
    "Inicio del pasillo": ["el inicio del pasillo", "el inicio del pasillo de su casa", "en el comienzo de su pasillo"],
    "Final del pasillo": ["el final del pasillo", "el final del pasillo de su casa", "la puerta del baño", "la puerta del baño de su casa"],
    "Baño": ["el baño", "su baño", "el baño de su casa", "su baño de su casa"],  
}

#Diccionario de palabras para la narración de la historia de acuerdo al personaje principal 
dictWordName = {
    "Miguel": {
        "conditionSafety": {
            "Seguro": "seguro",
            "Inseguro": "inseguro"
        }
    },
    "Sofia": {
        "conditionSafety": {
            "Seguro": "segura",
            "Inseguro": "insegura"
        }
    },
    "Carlos": {
        "conditionSafety": {
            "Seguro": "seguro",
            "Inseguro": "inseguro"
        }
    },
    "Ana": {
        "conditionSafety": {
            "Seguro": "segura",
            "Inseguro": "insegura"
        }
    },
    "Luis": {
        "conditionSafety": {
            "Seguro": "seguro",
            "Inseguro": "inseguro"
        }
    },
    "Maria": {
        "conditionSafety": {
            "Seguro": "segura",
            "Inseguro": "insegura"
        }
    },
    "Pedro": {
        "conditionSafety": {
            "Seguro": "seguro",
            "Inseguro": "inseguro"
        }
    },
    "Laura": {
        "conditionSafety": {
            "Seguro": "segura",
            "Inseguro": "insegura"
        }
    },
    "Juan": {
        "conditionSafety": {
            "Seguro": "seguro",
            "Inseguro": "inseguro"
        }
    },
    "Andrea": {
        "conditionSafety": {
            "Seguro": "segura",
            "Inseguro": "insegura"
        }
    }
}


#Clases de la historia 

#Clase de personaje con sus atributos (nombre, ubicación y estado de seguridad)
class Character:
    def __init__(self, name, location, conditionsafety):
        self.name = name
        self.location = location
        self.conditionsafety = conditionsafety

#Clase de acción con sus atributos (nombre, personaje, precondiciones y postcondiciones)
class StoryAction:
    def __init__(self, name, character, preconditions, postconditions):
        self.name = name
        self.character = character
        self.preconditions = preconditions
        self.postconditions = postconditions

#Clase de meta con sus atributos (nombre, personaje, precondiciones y plan)
class Goal:
    def __init__(self, name, character, preconditions, plan):
        self.name = name
        self.character = character
        self.preconditions = preconditions
        self.plan = plan

#Función para seleccionar el personaje principal de la historia
def Select_Character():
    #Se inicializan las variables globales (listLocationCharacter la cual contiene las ubicaciones de la historia)
    global listLocationCharacter


    logging.info("Se inicia el proceso de selección del personaje principal")

    #Listas de nombres de personajes y condiciones de seguridad
    listNameCharacter = ["Miguel", "Sofia", "Carlos", "Ana", "Luis", "Maria", "Pedro", "Laura", "Juan", "Andrea"]
    listConditionSafetyCharacter = ["Seguro", "Inseguro"]

    #Lista de personajes
    listCharacters = []

    #Se selecciona aleatoriamente un personaje principal
    for i in range(len(listNameCharacter)):
        #Se selecciona aleatoriamente un nombre de la lista de nombres de personajes
        Name = random.choice(listNameCharacter)
        #Se elimina el nombre seleccionado de la lista de nombres de personajes
        listNameCharacter.remove(Name)
        #Se selecciona aleatoriamente una ubicación de la lista de ubicaciones
        randomIndexLocation = random.randint(0, len(listLocationCharacter) - 1)
        """if randomIndexLocation == len(listLocationCharacter) - 1:
            character = Character(Name, listLocationCharacter[0], listConditionSafetyCharacter[1])
        else:
            character = Character(Name, listLocationCharacter[randomIndexLocation], listConditionSafetyCharacter[1])"""

        #Se crea un objeto de la clase Character con los atributos (nombre, ubicación y estado de seguridad) 
        character = Character(Name, listLocationCharacter[randomIndexLocation], listConditionSafetyCharacter[1])
        #Se añade el personaje a la lista de personajes
        listCharacters.append(character)
    
    

    #Se selecciona aleatoriamente un personaje principal de la lista de personajes 
    CharacterSelected = random.choice(listCharacters)

    logging.info("Se selecciona el personaje principal")
    logging.info("El personaje principal es: " + CharacterSelected.name)
    logging.info("Se encuentra en: " + CharacterSelected.location)
    logging.info("Estado de seguridad: " + CharacterSelected.conditionsafety)
     
    #Se retorna el personaje principal
    return CharacterSelected

#Se selecciona el personaje principal de la historia 
CharacterPrincipal = Select_Character()

#Función para crear las metas de la historia 
def Create_Goals(CharacterPrincipal):
    logging.info("Se inicia el proceso de creación de metas")
    
    #Se crean las acciones de la historia (Nombre, personaje, precondiciones y postcondiciones), las cuales son necesarias para cumplir las metas, Plan antes de llegar al final de la historia
    Plan_Pre = [
        StoryAction("Caminar hacia el inicio del pasillo", CharacterPrincipal, ["Debe de estar en la Recamara", "Debe de estar al final del pasillo"], ["Esta al inicio del pasillo"]),
        StoryAction("Caminar hacia el final del pasillo", CharacterPrincipal, ["Debe de estar al inicio del pasillo", "Debe de estar adentro del baño"], ["Esta al final del pasillo"]),
        StoryAction("Entrar al baño", CharacterPrincipal, ["Debe de estar al final del pasillo"], ["Esta adentro del baño"]),
    ]

    #Se crean las acciones de la historia (Nombre, personaje, precondiciones y postcondiciones), las cuales son necesarias para cumplir las metas, Plan después de llegar al final de la historia
    Plan_End = [
        StoryAction("Bloquear la puerta del baño", CharacterPrincipal, ["Debe de estar adentro del baño"], ["Esta a salvo"])
    ]

    #Se crean las metas de la historia (Nombre, personaje, precondiciones y plan), las cuales son necesarias para cumplir la historia (Meta Pre y Meta End)
    Goal_Pre = Goal("Mover al personaje a adentro del baño", CharacterPrincipal, None, Plan_Pre)
    Goal_End = Goal("Bloquear la puerta del baño para estar a salvo", CharacterPrincipal, Goal_Pre, Plan_End)

    #Se crea un diccionario con las metas de la historia 
    Dict_Goals = {
        "Goal_Pre": Goal_Pre,
        "Goal_End": Goal_End
    }

    logging.info("Se crean las metas")
    logging.info("Meta Pre: " + Goal_Pre.name)
    logging.info("Meta End: " + Goal_End.name)

    #Se retorna el diccionario con las metas de la historia
    return Dict_Goals

#Se crean las metas de la historia
Dict_Goals = Create_Goals(CharacterPrincipal)

#Se inicializa la meta actual con la meta Pre 
Goal_Current = None
Goal_Current = Dict_Goals["Goal_Pre"]

logging.info("Se inicia la narración de la historia")
logging.info("Personaje principal: " + CharacterPrincipal.name)
logging.info("Meta actual: " + Goal_Current.name)
print (CharacterPrincipal.name)

# Seleccionar la meta actual aleatoriamente dependiendo si esta en el baño o no
if CharacterPrincipal.location == "Baño":
    #Se selecciona la meta actual aleatoriamente entre la meta End y la meta Pre 
    Goal_Current = random.choice([Dict_Goals["Goal_End"], Dict_Goals["Goal_Pre"]])
    logging.info("Meta actual: " + Goal_Current.name)

print("esta en " + random.choice(dictLocations[CharacterPrincipal.location]) + ",")


print("y se encuentra " + dictWordName[CharacterPrincipal.name]["conditionSafety"][CharacterPrincipal.conditionsafety] + ".")
print("y su objetivo es " + Dict_Goals["Goal_End"].name.lower() + ".")

#Se inicia el ciclo de la historia 
while True:
    #Se obtiene el plan de la meta actual 
    plan = Goal_Current.plan
    logging.info("Se inicia la ejecución del plan")
    logging.info("Plan: " + Goal_Current.name)
    #Locacion se actualiza con la ubicación actual del personaje principal 
    location = CharacterPrincipal.location.lower()
    logging.info("Ubicación actual: " + location)

    #Se crea una lista de acciones válidas
    listValidActions = []
    #Se recorre el plan de la meta actual 
    for action in plan:
        #Se recorren las precondiciones de la acción
        for precondition in action.preconditions:
            #Se verifica si la ubicación actual del personaje principal se encuentra en la precondición de la acción
            if location in precondition.lower():
       
                logging.info("Se cumple la precondición")
                logging.info("Precondición: " + precondition)
                logging.info("Acción: " + action.name)
                #Se añade la acción a la lista de acciones válidas
                listValidActions.append(action)

    #Se verifica si la lista de acciones válidas está vacía 
    for i in range(len(listValidActions)):
        #Se imprime la acción válida seleccionada 
        if i == len(listValidActions) - 1:
            print("puede " + listValidActions[i].name.lower())
        else:
            #Se imprime la acción válida seleccionada si hay más de una acción válida 
            if len(listValidActions) > 1:
                print("puede " + listValidActions[i].name.lower())
                print("o")
            else:
                #Se imprime la acción válida seleccionada si hay solo una acción válida
                print("puede " + listValidActions[i].name.lower())

    #Se selecciona aleatoriamente una acción válida de la lista de acciones válidas
    actionExecute = random.choice(listValidActions)
    print("decide", actionExecute.name.lower())
    logging.info("Acción seleccionada: " + actionExecute.name)

    #Se recorren las postcondiciones de la acción seleccionada 
    for locationGlobal in listLocationCharacter:
        #Se actualiza la ubicación del personaje principal si la ubicación global se encuentra en el nombre de la acción seleccion
        if locationGlobal.lower() in actionExecute.name.lower():
            #Se actualiza la ubicación del personaje principal
            CharacterPrincipal.location = locationGlobal
            logging.info("Se actualiza la ubicación (ESTADO) del personaje principal")
            logging.info("Ubicación actual: " + locationGlobal)

           #Se verifica si la ubicación actual del personaje principal es igual a la ubicación del baño para cambiar la meta actual 
            if CharacterPrincipal.location == "Baño":
                #Se actualiza la meta actual a la meta End 
                Goal_Current = Dict_Goals["Goal_End"]
                

    #Se verifica si la acción seleccionada es igual a la acción de la meta End 
    if actionExecute.name == "Bloquear la puerta del baño":
        logging.info("Se cumple la meta")
        #Se actualiza el estado de seguridad del personaje principal a seguro
        CharacterPrincipal.conditionsafety = "Seguro"
        logging.info("Personaje principal seguro")
        print(CharacterPrincipal.name + " se encuentra a salvo.")
        print("Fin de la historia")
        logging.info("Fin de la historia")
        exit(0)
        



    