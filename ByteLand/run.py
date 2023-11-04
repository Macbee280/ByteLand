""" run.py

Run project for AI Civilization

"""

from general import Character
from general import *

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
    gabe = Character("GABE", "You are a villager in a small town of 4. You are new to this town and don't know many people. You are the new smith of the town.", "TOWNSQUARE")
    #izzy = Character("IZZY", "You are a villager in a small town of 4. You are the bartender of this town and heard there's a newcomer to the town. You want to meet him, his name is GABE.", "TOWNSQUARE")
    print(gabe.turn())
    #print(izzy.turn())
    
    # '[MOVE]',  'TAVERN'
main()