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
player_result_template = {'Shotgun':0,'Brain':0}

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
        player_throw = []
        print(f"El {current_player} lanza {len(player_unknown_dice)} dados y obtiene:")
        while len(player_unknown_dice) > 0:
            dado_definido = dict(dado_definido_template)
            if player_unknown_dice[0] == 'red_dice':
                dado_definido["resultado"] = RED_DICE_DEF[str(random.randint(1, 6))]
                print(f"{f.RED} ■   {dado_definido['resultado']}{f.RESET}")
            elif player_unknown_dice[0] == 'yellow_dice':
                dado_definido["resultado"] = YELLOW_DICE_DEF[str(random.randint(1, 6))]
                print(f"{f.YELLOW} ■   {dado_definido['resultado']}{f.RESET}")
            elif player_unknown_dice[0] == 'green_dice':
                dado_definido["resultado"] = GREEN_DICE_DEF[str(random.randint(1, 6))]
                print(f"{f.CYAN} ■   {dado_definido['resultado']}{f.RESET}")
            dado_definido["color"] = player_unknown_dice[0]
            player_throw.append(dado_definido)
            player_unknown_dice.pop(0)

        return player_throw  # [{"color": "x", "resultado": "y"}, {}, {}, ...]

    # 4. Evaluar resultados
    def evaluar_resultados(lista):
        """
        :param      lista: list of dicts
        :return:    player_result: dict {'Shotgun':int, 'Brain':int}
                    lista: list of dicts (sin Footsteps)
        """
        nonlocal player_defined_dice
        nonlocal global_pool_dice
        nonlocal tirada
        player_result = dict(player_result_template)
        footsteps_a_eliminar = []
        for num, elemento in enumerate(lista):
            if elemento["resultado"] == "Footstep":
                footsteps_a_eliminar.append(num)
            else:
                player_result[elemento["resultado"]] += 1

        # Devolver Footsteps a la reserva
        if len(footsteps_a_eliminar) > 0:
            print("Se devuelve al pool los resultados 'Footstep': ", end="")
            footsteps_a_eliminar.reverse()
            contador_footsteps = 0
            for footstep in footsteps_a_eliminar:
                contador_footsteps += 1
                if lista[footstep]["color"] == "red_dice":
                    print(f"{f.RED} ■ {f.RESET}", end="")
                elif lista[footstep]["color"] == "yellow_dice":
                    print(f"{f.YELLOW} ■ {f.RESET}", end="")
                elif lista[footstep]["color"] == "green_dice":
                    print(f"{f.CYAN} ■ {f.RESET}", end="")
                global_pool_dice.append(lista[footstep]["color"])
                lista.pop(footstep)

        return player_result, lista

    def mostrar_resultados(resultados, lista):
        for tipo in resultados.keys():
            print(tipo + "s:" + (12 - len(tipo)) * ' ' + str(resultados[tipo]) + "  ", end="")
            for dado in lista:
                if dado["resultado"] == tipo and dado["color"] == "red_dice":
                    print(f"{f.RED} ■ {f.RESET}", end="")
                elif dado["resultado"] == tipo and dado["color"] == "yellow_dice":
                    print(f"{f.YELLOW} ■ {f.RESET}", end="")
                elif dado["resultado"] == tipo and dado["color"] == "green_dice":
                    print(f"{f.CYAN} ■ {f.RESET}", end="")
            print("")
        print("")

    # 5 Añadir resultado al pool
    def add_tirada(tirada, acumulado):
        """
        :global tirada: La tirada, una lista de dados definidos (list of dicts)
        :global player_shown_dice:   El pool del jugador (list of dicts)
        :param global_pool_dice: El cubilete (list of str)
        :return:
        """
        while len(tirada) > 0:
            acumulado.append(tirada[0])
            tirada.pop(0)
        return acumulado

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
        nonlocal brains_acumulados
        nonlocal global_pool_dice
        nonlocal player_defined_dice
        if len(global_pool_dice) < 3:
            for num, dado in enumerate(player_defined_dice):
                if dado["resultado"] == "Brain":
                    global_pool_dice.append(dado["color"])
                    player_defined_dice.pop(num)
                    brains_acumulados += 1

    # Condiciones iniciales de turno:
    player_unknown_dice = []
    player_defined_dice = []
    decision_is_continue = True

    print("---------------------------------------")
    print(f"{f.RED}Rojo   {player_red_brains}{f.RESET}   |   {f.BLUE}{player_blue_brains}   Azul{f.RESET}")
    print("---------------------------------------")
    print(f"\nTurno {contador_turnos} - {current_player}\n---------------------------------------")
    global_pool_dice = fillPoolDice()

    while True:

        input(f"\nEl {current_player} va a proceder a robar 3 dados:\n")
        # El jugador coge 3 dados al azar de la reserva
        pickDices(3)

        # Lanza los dados
        input(f"\nEl {current_player} va a proceder a lanzar los dados:\n")
        tirada = throw_dice()
        resultados_player, tirada = evaluar_resultados(tirada)

        # Comprueba si ha sacado 3 shotgun
        if resultados_player["Shotgun"] >= 3:
            print("")
            print("Se han obtenido 3 shotguns esta tirada. Se acaba la ronda")
            break

        # Añadir la tirada al pool
        print(f"\nEl {current_player} lleva acumulados los siguiente resultados:")
        player_defined_dice  = add_tirada(tirada, player_defined_dice)
        resultados_player = evaluar_resultados(player_defined_dice)[0]
        mostrar_resultados(resultados_player,player_defined_dice)

        # Comprueba si ha sacado 3 shotgun
        if resultados_player["Shotgun"] >= 3:
            print("")
            print("Se han acumulado 3 shotguns en este turno. Se acaba la ronda")
            break

        print(f'Dados restantes: {len(global_pool_dice)}')

        continue_or_stop()

        if decision_is_continue == False:
            numero_de_brains += resultados_player["Brain"]
            print(f"\nEl {current_player} ha obtenido {resultados_player['Brain']} Brains en esta ronda\n")
            break

        enough_dados()
    return numero_de_brains


# 8. Condiciones victoria

# 9. Empate


# Juego

#Condiciones iniciales del juego
player_blue_brains = 0
player_red_brains = 0
contador_turnos = 0
ronda_completa = True
fin_de_juego = False

print("\nComienza el juego de los dados Zombies")
print("----------------------------------------")
print("")
input("Se va a elegir al azar al jugador que comienza el juego...")
current_player = random.choice(["Jugador rojo","Jugador azul"])

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

while fin_de_juego == False:

    print("\nUltima Ronda\n")
    print("------------------------")
    input(f"Pulsa para comenzar la última ronda")
    if current_player == "Jugador rojo":
        player_red_brains = turno(current_player, "Final", player_red_brains)
        player_blue_brains = turno(current_player, "Final", player_blue_brains)
    else:
        player_blue_brains = turno(current_player, "Final", player_blue_brains)
        player_red_brains = turno(current_player, "Final", player_red_brains)

    if player_red_brains > player_blue_brains:
        ganador = "Jugador rojo"
        fin_de_juego = True
    elif player_red_brains < player_blue_brains:
        ganador = "Jugador azul"
        fin_de_juego = True
    else:
        pass

if ganador == "Jugador rojo":
    print(f.RED)
else:
    print(f.BLUE)

print(32*'*')
print(f"** El ganador es {ganador} **")
print(32*'*')

print(f.RESET)