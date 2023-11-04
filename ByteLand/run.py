""" run.py

Run project for AI Civilization

"""

from general import Character
from general import *
from Backend.map import *
from Backend.navigation import *
from Backend.utilities import *

def run_command(command, variable):
    
    if command == "[MOVE]":
        pass
    elif command == "[TALK]":
        pass
    elif command == "[PICKUP]":
        pass
    elif command == "[USE]":
        pass
    else:
        pass
        # Move to house

def main():
    game_map = GameMap(MAP_WIDTH, MAP_HEIGHT, TILE_SIZE)
    collision_map = CollisionMap(game_map.map_data, COLLISION_CHAR)

    gabe = Character("GABE", "You are a villager in a small town of 4. You are new to this town and don't know many people. You are the new smith of the town.", "TOWNSQUARE",coordinates=TOWN_CENTER)
    #izzy = Character("IZZY", "You are a villager in a small town of 4. You are the bartender of this town and heard there's a newcomer to the town. You want to meet him, his name is GABE.", "TOWNSQUARE")
    print(gabe.turn())
    if gabe.turn()[0] == '[MOVE]':
        gabe.location = gabe.turn()[1]
        path = collision_map.find_path(gabe.coordinates, VARIABLE)
        gabe.coordinates = VARIABLE
    #print(izzy.turn())
    
    # '[MOVE]',  'TAVERN'
main()