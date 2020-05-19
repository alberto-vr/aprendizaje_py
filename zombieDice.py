# prueba dentro ish

# Prueba tras git pull desde pc

# Prueba desde ish

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
RED_DICE_DEF = {'1':'red_Footstep','2':'red_Footstep','3':'red_Shotgun','4':'red_Shotgun','5':'red_Shotgun','6':'red_Brain'}
YELLOW_DICE_DEF = {'1':'yellow_Footstep','2':'yellow_Footstep','3':'yellow_Shotgun','4':'yellow_Shotgun','5':'yellow_Brain','6':'yellow_Brain'}
GREEN_DICE_DEF = {'1':'green_Footstep','2':'green_Footstep','3':'green_Shotgun','4':'green_Brain','5':'green_Brain','6':'green_Brain'}

AMOUNT_RED = 3
AMOUNT_YELLOW = 4
AMOUNT_GREEN = 6

player_board_template = {'Footstep':0,'Shotgun':0,'Brain':0}


# Cosas temporales
player_board = dict(player_board_template)
global_pool_dice = []
player_pool_dice = []

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
	player_board_throw = dict(player_board_template)
	while len(player_pool_dice)>0:
		if player_pool_dice[0] == 'red_dice':
			dice_result = RED_DICE_DEF[str(random.randint(1,6))]
		if player_pool_dice[0] == 'yellow_dice':
			dice_result = YELLOW_DICE_DEF[str(random.randint(1,6))]
		if player_pool_dice[0] == 'green_dice':
			dice_result = GREEN_DICE_DEF[str(random.randint(1,6))]
		player_board_throw[dice_result] += 1
		player_pool_dice.pop(0)
	return player_board_throw
    #print('Resultado de la tirada:' + \n\n)
    #for r,i in player_board_throw.items():
    #	print(str(i) + '	' + r + 's')
    	

# 4. Evaluar resultados
# 4A Añadir resultado al pool
def add_throw(player_board_throw):
	

# 5. Elección

# 6. Devolver dados

# 7. No quedan suficientes dados

# 8. Condiciones victoria

# 9. Empate



# Test
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
for r,i in player_board.items():
	print(str(i) + '	' + r + 's')
