""" run.py

Run project for AI Civilization

"""

from general import Character
from general import *
from Backend.map import *
from Backend.navigation import *
from Backend.utilities import *

LOCATIONS = {'TAVERN': (2, 2), 'TOWNSQUARE': (4, 2), 'SMITHERY': (3, 6), 'MARKET': (5, 4)}
CHARACTERS = {}

def main():
    game_map = GameMap(MAP_WIDTH, MAP_HEIGHT, TILE_SIZE)
    collision_map = CollisionMap(game_map.map_data, COLLISION_CHAR)

    gabe = Character("GABE", "You are a villager in a small town of 4. You are new to this town and don't know many people. You are the new smith of the town.", "TOWNSQUARE",coordinates=TOWN_CENTER)
    CHARACTERS[gabe.name] = gabe
    #izzy = Character("IZZY", "You are a villager in a small town of 4. You are the bartender of this town and heard there's a newcomer to the town. You want to meet him, his name is GABE.", "TOWNSQUARE")
    command, variable = gabe.turn()

    if command == '[MOVE]':
        run_command(gabe, command, tuple(variable), collision_map=collision_map, LOCATIONS=LOCATIONS)
    else:
        run_command(gabe, command, variable, CHARACTERS=CHARACTERS)
    
    #print(izzy.turn())

main()