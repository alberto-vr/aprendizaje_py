# 13 dados
# - 3 Rojos (2 footsteps, 3 shotguns, 1 brain)
# - 4 Amarillos (2 footsteps, 2 shotguns, 2 brain)
# - 6 Verdes (2 footsteps, 1 shotguns, 3 brain)

# 1. Se cogen 3 dados y se lanzan
# - Si sacas 3 shotguns -> Fin de turno
# - Puedes elegir entre Stop y Score o Continue

# Stop -> 1 score por cada brain y devuelve todos los dados
# Continue -> deja todos los footsteps -> Tira de nuevo 3 dados

# Si no tienes suficientes dados en el vaso, apunta el numero de brains, conserva shotguns
 # y mete el resto de dados

# Cuando alguien alcance 13 cerebros, será el último turno. Al final del turno, gana quien más cerebros tenga.

# Si hay empate, juegan una ronda más.

import random

# A. Definir juego
# 1. Definir los dados
RED_DICE_DEF = {'1':'F','2':'F','3':'S','4':'S','5':'S','6':'B'}
YELLOW_DICE_DEF = {'1':'F','2':'F','3':'S','4':'S','5':'B','6':'B'}
GREEN_DICE_DEF = {'1':'F','2':'F','3':'S','4':'B','5':'B','6':'B'}

AMOUNT_RED = 3
AMOUNT_YELLOW = 4
AMOUNT_GREEN = 6

global_pool_dice = []
player_pool_dice = []
player_board = []

# Llenar el cubilete

def fillPoolDice():
    for i_red in range(AMOUNT_RED):
        global_pool_dice.append('red_dice')
    for i_yellow in range(AMOUNT_YELLOW):
        global_pool_dice.append('yellow_dice')
    for i_green in range(AMOUNT_GREEN):
        global_pool_dice.append('green_dice')
    random.shuffle(global_pool_dice)

# 2. Coger x dados
def pickDices(amount_of_dices):
    for dice in range(amount_of_dices):
        random_pick = random.choice(global_pool_dice)
        global_pool_dice.remove(random_pick)
        player_pool_dice.append(random_pick)

# 3. Lanzar los dados
def throw_dice():
    while len(player_pool_dice)>0:
        if player_pool_dice[0] == 'red_dice':
            dice_result = RED_DICE_DEF[str(random.randint(1,6))]
        if player_pool_dice[0] == 'yellow_dice':
            dice_result = YELLOW_DICE_DEF[str(random.randint(1,6))]
        if player_pool_dice[0] == 'green_dice':
            dice_result = GREEN_DICE_DEF[str(random.randint(1,6))]
        player_board.append(dice_result)
        player_pool_dice.pop(0)

fillPoolDice()
pickDices(3)
print('Antes de tirar:')
for i in range(len(player_pool_dice)):
    print(str(i+1) + ': ' +player_pool_dice[i])
throw_dice()
print('Después de tirar: ')
for i in range(len(player_pool_dice)):
    print(str(i+1) + ': ' +player_pool_dice[i])
print('Resultados: ')
for i in range(len(player_board)):
    print(player_board[i],end=' ')

# 4. Evaluar resultados

# 5. Elección

# 6. Devolver dados

# 7. No quedan suficientes dados

# 8. Condiciones victoria

# 9. Empate