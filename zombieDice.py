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
from colorama import Fore as f

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

def turno(current_player, contador_turnos, numero_de_brains):

    # 1. Llenar el cubilete
    def fillPoolDice():  # Condicion inicial, se llena el cubilete de dados
        """
        :return: global_pool_dice: Los dados en la reserva (list of str)
        """
        global_pool_dice = []
        for i_red in range(AMOUNT_RED):
            global_pool_dice.append('red_dice')
        for i_yellow in range(AMOUNT_YELLOW):
            global_pool_dice.append('yellow_dice')
        for i_green in range(AMOUNT_GREEN):
            global_pool_dice.append('green_dice')
        random.shuffle(global_pool_dice)
        print(f"Hay un total de {len(global_pool_dice)} dados disponibles")
        return global_pool_dice

    # 2. Coger x dados
    def pickDices(amount_of_dices):  # Se coge un número int de dados
        """
        :param amount_of_dices: Número de dados (int)
        :return: global_pool_dice: Los dados en la reserva (list of str)
        :return: player_unknown_dice: Los dados en el cubilete (list of str)
        """
        nonlocal global_pool_dice
        nonlocal player_unknown_dice
        print(f"El {current_player} ha robado: ", end="")
        for dice in range(amount_of_dices):
            random_pick = random.choice(global_pool_dice)
            if random_pick == "red_dice":
                print(f"{f.RED} ■ {f.RESET}", end="")
            elif random_pick == "yellow_dice":
                print(f"{f.YELLOW} ■ {f.RESET}", end="")
            elif random_pick == "green_dice":
                print(f"{f.CYAN} ■ {f.RESET}", end="")
            global_pool_dice.remove(random_pick)
            player_unknown_dice.append(random_pick)
        print(f"\nDespués de robar, hay un total de {len(global_pool_dice)} dados disponibles\n")

    # 3. Lanzar los dados
    def throw_dice():  # Se vacía el player_pool_dice
        """
        :return: Una tirada con dados definidos (list of dicts)
        """
        nonlocal player_unknown_dice
        dado_definido = dict(dado_definido_template)
        player_throw = []
        print(f"El {current_player} lanza {len(player_unknown_dice)} dados y obtiene:")
        while len(player_unknown_dice) > 0:
            dado_definido = dict(dado_definido_template)
            if player_unknown_dice[0] == 'red_dice':
                dado_definido["resultado"] = RED_DICE_DEF[str(random.randint(1, 6))]
            elif player_unknown_dice[0] == 'yellow_dice':
                dado_definido["resultado"] = YELLOW_DICE_DEF[str(random.randint(1, 6))]
            elif player_unknown_dice[0] == 'green_dice':
                dado_definido["resultado"] = GREEN_DICE_DEF[str(random.randint(1, 6))]
            dado_definido["color"] = player_unknown_dice[0]
            player_throw.append(dado_definido)
            player_unknown_dice.pop(0)

        return player_throw  # [{"color": "x", "resultado": "y"}, {}, {}, ...]

    # 4. Mostrar resultados en pantalla
    def mostrar_resultados(lista):
        """
        :param dict_result: Una lista de dados definidos (list of dicts)
        :return: shotgun_break: Define si se han obtenido 3 o más shotguns esta tirada (boolean)
        """
        nonlocal shotgun_break
        player_result = dict(player_result_template)

        def daditos(lista, resultado):
            nonlocal player_result
            print(f"{resultado}s:" + (12-len(resultado))*" ", end="")
            for elemento in lista:
                if elemento["resultado"] == resultado and elemento["color"] == "red_dice":
                    print(f"{f.RED} ■ {f.RESET}", end="")
                elif elemento["resultado"] == resultado and elemento["color"] == "yellow_dice":
                    print(f"{f.YELLOW} ■ {f.RESET}", end="")
                elif elemento["resultado"] == resultado and elemento["color"] == "green_dice":
                    print(f"{f.CYAN} ■ {f.RESET}", end="")
                player_result[elemento["resultado"]] += 1
            return player_result[elemento["resultado"]]
        for resultado in ["Footstep", "Shotgun", "Brain"]:
            daditos(lista, resultado)
            print("")

        # Comprobar si se han obtenido 3 shotguns esta tirada
        shotgun_break = False
        if player_result["Shotgun"] >= 3:
            print("")
            print("Se han obtenido 3 shotguns esta tirada. Se pasa turno")
            shotgun_break = True

    # 5 Añadir resultado al pool
    def add_tirada(tirada):
        """
        :global tirada: La tirada, una lista de dados definidos (list of dicts)
        :global player_shown_dice:   El pool del jugador (list of dicts)
        :param global_pool_dice: El cubilete (list of str)
        :return:
        """
        nonlocal global_pool_dice
        nonlocal player_defined_dice
        while len(tirada) > 0:
            if tirada[0]["resultado"] == "Footstep":  # Primero desechamos los Footsteps y los devolvemos a la reserva
                global_pool_dice.append(tirada[0]["color"])
                global_pool_dice.append(tirada[0]["color"])
            else:
                player_defined_dice.append(tirada[0])
            tirada.pop(0)

    # 6. Elección
    def continue_or_stop():
        """
        :return: decision_is_continue: Continuamos (boolean)
        """
        nonlocal decision_is_continue
        decision_is_continue = False
        decision = input("(c)ontinue or (s)top?: ").lower()
        while decision != "c" and decision != "s":
            decision = input("(c)ontinue or (s)top?: ").lower()

        if decision == "c":
            decision_is_continue = True
        elif decision == "s":
            decision_is_continue = False

    # 7. Devolver dados
    def enough_dados():
        nonlocal numero_de_brains
        nonlocal global_pool_dice
        nonlocal player_defined_dice
        if len(global_pool_dice) < 3:
            for num, dado in enumerate(player_defined_dice):
                if dado["resultado"] == "Brain":
                    global_pool_dice.append(dado["color"])
                    player_defined_dice.pop(num)
                    numero_de_brains += 1

    # Condiciones iniciales de turno:
    player_unknown_dice = []
    player_defined_dice = []
    shotgun_break = False
    decision_is_continue = True


    print(f"\nTurno {contador_turnos} - {current_player}\n---------------------------------------\n")
    global_pool_dice = fillPoolDice()
    while True:

        input(f"\nEl {current_player} va a proceder a robar 3 dados:\n")
        # El jugador coge 3 dados al azar de la reserva
        pickDices(3)

        # Lanza los dados
        input(f"\nEl {current_player} va a proceder a lanzar los dados:\n")
        tirada = throw_dice()
        mostrar_resultados(tirada)

        # Comprueba si ha sacado 3 shotgun
        if shotgun_break == True:
            break

        # Añadir la tirada al pool
        add_tirada(tirada)

        print(f"\nEl {current_player} lleva acumulados los siguiente resultados:")
        mostrar_resultados(tirada)
        print(f'Dados restantes: {len(global_pool_dice)}')
        if shotgun_break == True:
            break

        continue_or_stop()

        if decision_is_continue == False:
            break

        enough_dados()
    return numero_de_brains

# 7. No quedan suficientes dados

# 8. Condiciones victoria

# 9. Empate


# Juego

#Condiciones iniciales del juego
player_blue_brains = 0
player_red_brains = 0
contador_turnos = 0
ronda_completa = True

print("\nComienza el juego de los dados Zombies")
print("----------------------------------------")
print("")
input("Se va a elegir al azar al jugador que comienza el juego...")
current_player = random.choice(["Judador rojo","Jugador azul"])

print(f"\nComienza el juego el {current_player}\n")

# Turnos intermedios normales
while player_blue_brains < 13 and player_red_brains < 13:
    
    # Contador de turnos
    if ronda_completa == True:
        contador_turnos += 1
        ronda_completa = False
    else:
        ronda_completa = True

    # Se definen los valores en función del jugador
    input(f"Pulsa para comenzar el turno {contador_turnos}")
    if current_player == "Jugador rojo":
        player_red_brains = turno(current_player, contador_turnos, player_red_brains)
    else:
        player_blue_brains = turno(current_player, contador_turnos, player_blue_brains)



    
    # Cambio de jugador
    print(f'Fin del turno de {current_player}\n')
    input('Press any key to continue')
    print('')
    if current_player == 'Jugador rojo':
        current_player = 'Jugador azul'
    else:
        current_player = 'Jugador rojo'


