"""
13 dados
- 3 Rojos (2 footsteps, 3 shotguns, 1 brain)
- 4 Amarillos (2 footsteps, 2 shotguns, 2 brain)
- 6 Verdes (2 footsteps, 1 shotguns, 3 brain)

1. Se cogen 3 dados y se lanzan
- Si sacas 3 shotguns -> Fin de turno
- Puedes elegir entre Stop y Score o Continue

Stop -> 1 score por cada brain y devuelve todos los dados
Continue -> deja todos los footsteps -> Tira de nuevo 3 dados

Si no tienes suficientes dados en el vaso, apunta el numero de brains, conserva shotguns
y mete el resto de dados

Cuando alguien alcance 13 cerebros, será el último turno. Al final del turno, gana quien más cerebros tenga.

Si hay empate, juegan una ronda más.
"""

import random

# A. Definir juego
# 1. Definir los dados
RED_DICE_DEF = {'1':'Footstep','2':'Footstep','3':'Shotgun','4':'Shotgun','5':'Shotgun','6':'Brain'}
YELLOW_DICE_DEF = {'1':'Footstep','2':'Footstep','3':'Shotgun','4':'Shotgun','5':'Brain','6':'Brain'}
GREEN_DICE_DEF = {'1':'Footstep','2':'Footstep','3':'Shotgun','4':'Brain','5':'Brain','6':'Brain'}

AMOUNT_RED = 3
AMOUNT_YELLOW = 4
AMOUNT_GREEN = 6

dado_definido_template = {'color': None, 'resultado': None}
player_result_template = {'Footstep':0,'Shotgun':0,'Brain':0}


# Llenar el cubilete
def fillPoolDice(): # Condicion inicial, se llena el cubilete de dados
    """
    :return: global_pool_dice: Los dados en la reserva (list of str)
    """
    global global_pool_dice
    global_pool_dice = []
    for i_red in range(AMOUNT_RED):
        global_pool_dice.append('red_dice')
    for i_yellow in range(AMOUNT_YELLOW):
        global_pool_dice.append('yellow_dice')
    for i_green in range(AMOUNT_GREEN):
        global_pool_dice.append('green_dice')
    random.shuffle(global_pool_dice)

# 2. Coger x dados
def pickDices(amount_of_dices): # Se coge un número int de dados
    """
    :param amount_of_dices: Número de dados (int)
    :return: global_pool_dice: Los dados en la reserva (list of str)
    :return: player_pool_dice: Los dados en el cubilete (list of str)
    """
    global global_pool_dice
    global player_pool_dice
    print(f"El {current_player} ha escogido: ")
    for dice in range(amount_of_dices):
        random_pick = random.choice(global_pool_dice)
        print(f"- {random_pick}")
        global_pool_dice.remove(random_pick)
        player_pool_dice.append(random_pick)
    print("")

# 3. Lanzar los dados
def throw_dice(): # Se vacía el player_pool_dice
    """
    :return: Una tirada con dados definidos (list of dicts)
    """
    global player_pool_dice
    global dado_definido
    player_throw = []
    print(f"El {current_player} lanza los dados y obtiene:")
    while len(player_pool_dice)>0:
        dado_definido = dict(dado_definido_template)
        if player_pool_dice[0] == 'red_dice':
            dado_definido["resultado"] = RED_DICE_DEF[str(random.randint(1,6))]
        elif player_pool_dice[0] == 'yellow_dice':
            dado_definido["resultado"] = YELLOW_DICE_DEF[str(random.randint(1, 6))]
        elif player_pool_dice[0] == 'green_dice':
            dado_definido["resultado"] = GREEN_DICE_DEF[str(random.randint(1, 6))]
        dado_definido["color"] = player_pool_dice[0]
        player_throw.append(dado_definido)
        player_pool_dice.pop(0)

    return player_throw    # [{"color": "x", "resultado": "y"}, {}, {}, ...]

# 4. Extraer resultados de lista
def extraer_resultados(lista):  # Aquí se introduce una lista de dados definidos {color, resultado}
    """
    :rtype: object
    :param lista: Una lista de dados definidos (list of dicts)
    :return: Un diccionario con valores de Footstep, Shotgun y Brain (dict)
    """
    player_result = dict(player_result_template)
    for elemento in lista:
        player_result[elemento["resultado"]] += 1

    return player_result

# 5. Mostrar resultados en pantalla
def mostrar_resultados(dict_result):
    """
    :param dict_result: Una lista de dados definidos (list of dicts)
    :return: shotgun_break: Define si se han obtenido 3 o más shotguns esta tirada (boolean)
    """
    global shotgun_break
    if dict_result['Footstep'] > 0:
        print(f"{dict_result['Footstep']}   Footsteps")
    if dict_result['Shotgun'] > 0:
        print(f"{dict_result['Shotgun']}   Shotguns")
    if dict_result['Brain'] > 0:
        print(f"{dict_result['Brain']}   Brains")

    # Comprobar si se han obtenido 3 shotguns esta tirada
    shotgun_break = False
    if dict_result["Shotgun"] >= 3:
        print("")
        print("Se han obtenido 3 shotguns esta tirada. Se pasa turno")
        shotgun_break = True


# 6 Añadir resultado al pool
def add_tirada(tirada):
    """
    :global tirada: La tirada, una lista de dados definidos (list of dicts)
    :global player_pool_dice:   El pool del jugador (list of dicts)
    :param global_pool_dice: El cubilete (list of str)
    :return:
    """
    global player_pool_dice
    global global_pool_dice
    while len(tirada) > 0:
        if tirada[0]["resultado"] == "Footstep":  # Primero desechamos los Footsteps y los devolvemos a la reserva
            print("\nGlobal - Antes: " + str(global_pool_dice))
            print(tirada[0]["color"])
            global_pool_dice.append(tirada[0]["color"])
            print("Global - Despues: " + str(global_pool_dice) + "\n")
        else:
            print("\nPlayer - Antes: " + str(player_pool_dice))
            print(tirada[0])
            player_pool_dice.append(tirada[0])
            print("Player - Despues: " + str(player_pool_dice) + "\n")
        tirada.pop(0)


# 7. Elección
def continue_or_stop():
    """
    :return: decision_is_continue: Continuamos (boolean)
    """
    global decision_is_continue
    decision_is_continue = False
    decision = input("(c)ontinue or (s)top?: ").lower()
    while decision != "c" and decision != "s":
        decision = input("(c)ontinue or (s)top?: ").lower()

    if decision == "c":
        decision_is_continue = True
    elif decision == "s":
        decision_is_continue = False


# 6. Devolver dados
def enough_dados():
    global numero_de_brains
    if len(global_pool_dice) < 3:
        for num, dado in enumerate(player_pool_dice):
            if dado["resultado"] == "brain":
                global_pool_dice.append(dado["color"])
                player_pool_dice.pop(num)
                numero_de_brains += 1



# 7. No quedan suficientes dados

# 8. Condiciones victoria

# 9. Empate


# Juego

#Condiciones iniciales del juego
player_blue_brains = 0
player_red_brains = 0
contador_turnos = 0
ronda_completa = True
dado_definido = dict(dado_definido_template)

print("Comienza el juego de los dados Zombies")
print("----------------------------------------")
print("")

current_player = random.choice(["Judador rojo","Jugador azul"])

print(f"Comienza el juego el {current_player}\n")

# Turnos intermedios normales
while player_blue_brains < 13 or player_red_brains < 13:
    # Condiciones iniciales de turno:
    global_pool_dice = []
    player_pool_dice = []
    fillPoolDice()
    shotgun_break = False
    decision_is_continue = True

    # Adaptación de variables a jugador
    if current_player == "Jugador rojo":
        numero_de_brains = player_red_brains
    else:
        numero_de_brains = player_blue_brains

    # Contador de turnos
    if ronda_completa == True:
        contador_turnos += 1
        ronda_completa = False
    else:
        ronda_completa = True

    print(f"Turno {contador_turnos} - {current_player}\n---------------------------------------\n")

    while shotgun_break == False or decision_is_continue == True:
        # El jugador coge 3 dados al azar de la reserva
        pickDices(3)

        # Lanza los dados
        tirada = throw_dice()
        resultados_tirada = extraer_resultados(tirada)
        mostrar_resultados(resultados_tirada)

        # Comprueba si ha sacado 3 shotgun
        if shotgun_break == True:
            continue

        # Añadir la tirada al pool
        add_tirada(tirada)

        print(f"\nEl {current_player} lleva acumulados los siguiente resultados:")
        resultados_ronda = extraer_resultados(player_pool_dice)
        mostrar_resultados(resultados_ronda)

        continue_or_stop()

    break













# Test
"""
pickDices(3)
print("")
print('Antes de tirar:')

for i in range(len(player_pool_dice)):
    print(str(i+1) + ': ' +player_pool_dice[i])

print("")
print('Después de tirar: ')

tirada = throw_dice()

resultados_tirada = extraer_resultados(tirada)

mostrar_resultados(resultados_tirada)

"""