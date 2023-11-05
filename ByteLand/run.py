""" run.py

Run project for AI Civilization

"""

from general import Character
from general import *
from Backend.map import *
from Backend.navigation import *
from Backend.utilities import *

CHARACTERS = {}

def main():
    opt = {}
    opt = configure_opt(opt)
    game_map = GameMap(opt['map_width'], opt['map_height'], opt['tile_size'])
    collision_map = CollisionMap(game_map.map_data, opt['collision_char'])

    gabe = Character("GABE", "You are a villager in a small town of 4. You are new to this town and don't know many people. You are the new smith of the town.", "TOWNSQUARE",coordinates=opt['coordinates']['TOWNSQUARE'])
    CHARACTERS[gabe.name] = gabe
    izzy = Character("IZZY", "You are a villager in a small town of 4. You are the bartender of this town and heard there's a newcomer to the town. You want to meet him, his name is GABE.", "TOWNSQUARE")
    CHARACTERS[izzy.name] = izzy
    command, variable = gabe.turn(people="IZZY")

    if command == '[MOVE]':
        run_command(gabe, command, variable, collision_map, opt)
    else:
        run_command(gabe, command, variable, CHARACTERS=CHARACTERS)
    
    #print(izzy.turn())

main()