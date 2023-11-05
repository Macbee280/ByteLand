""" run.py

Run project for AI Civilization

"""

from general import Character
from general import *
from Backend.map import *
from Backend.navigation import *
from Backend.utilities import *

CHARACTERS = {}

def find_people(prime_character):
    output = ""
    
    for index, name in enumerate(CHARACTERS.keys()):
        if name != prime_character.name:
            if CHARACTERS[name].location == prime_character.location:
                if output == "":
                    output = name
                else:
                    output += f", {name}"
                    
    return output

def character_turn(person, map, options):
    command, variable = person.turn(people=find_people(person))
    run_command(person, command, variable, map, options, CHARACTERS=CHARACTERS)

def main():
    opt = {}
    opt = configure_opt(opt)
    game_map = GameMap(opt['map_width'], opt['map_height'], opt['tile_size'])
    collision_map = CollisionMap(game_map.map_data, opt['collision_char'])

    gabe = Character("GABE", "You are a villager named GABE in a small medieval town of 4. You are new to this town and don't know many people. You are the new smith of the town.", "TOWNSQUARE", coordinates=opt['coordinates']['TOWNSQUARE'])
    CHARACTERS[gabe.name] = gabe
    izzy = Character("IZZY", "You are a villager named IZZY in a small medieval town of 4. You are the bartender of this town and heard there's a newcomer to the town. You want to meet him, his name is GABE.", "TOWNSQUARE", coordinates=opt['coordinates']['TOWNSQUARE'])
    CHARACTERS[izzy.name] = izzy
    aiden = Character("AIDEN", "You are a villager named AIDEN in a small medieval town of 4. You are the town leader, a retired wizard and you want to make sure the jester, MILES isn't too mischievous.", "MARKET", coordinates=opt['coordinates']['MARKET'])
    CHARACTERS[aiden.name] = aiden
    miles = Character("MILES", "You are a villager named MILES in a small medieval town of 4. You are the jester of this town and heard there's a newcomer to the town. You want to meet him, and prank him.", "MARKET", coordinates=opt['coordinates']['MARKET'])
    CHARACTERS[miles.name] = miles
    
    character_turn(gabe, collision_map, opt)
    character_turn(izzy, collision_map, opt)
    character_turn(aiden, collision_map, opt)
    character_turn(miles, collision_map, opt)


main()