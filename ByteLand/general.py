""" general.py

Collection of functions to generate and run the AI civilization

"""
#import Coding_Utils.coding_utils as cu
#from Coding_Utils.coding_utils import err
#from Coding_Utils.object import Object

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from langchain.memory import ConversationSummaryMemory

from Backend.navigation import *


import os
from apikey import apikey

CHARACTERS = {"Ancient Aiden", "Galliant Gabe", "Magical Miles", "Ye Olde Izzy"}
OBJECTS = {}

os.environ['OPENAI_API_KEY'] = apikey

# [USE] {SWORD}   [MOVE] {SMITHERY}

class Character():
    # TODO: Initialize location with a location class?
    def __init__(self, name = "", bio = "", location = "TOWNSQUARE", hand_item = "", coordinates = (0,0)):
        self.name = name
        self.location = location
        self.hand_item = hand_item
        self.coordinates = coordinates
        
        self.llm = OpenAI(temperature=0.9)
        self.memory = ConversationSummaryMemory(llm=self.llm)
        
        command = 'You must follow these rules: Commands must be enclosed in []. Input one total command. Enclosed text must be all uppercase. End commands with a "|". Your commands are: [MOVE] (LOCATION) and [TALK] (NAME) and [PICKUP] (ITEM) and [USE] - this uses the item in your hand'
        
        turn_template = PromptTemplate(
            input_variables=['bio', 'location', 'people', 'items', 'hand_item'],
            template='{bio}\n\nThere are three locations: TOWNSQUARE, TAVERN, and MARKET.\nYou are at {location} | PEOPLE: {people} | ITEMS: {items} | IN HAND ITEM: {hand_item}\nEnter command:'
        )
        
        talk_template = PromptTemplate(
            input_variables=['other_char', 'prev_dialogue'],
            template='Enter command [STOPTALKING] to end dialogue. You are talking to {other_char}. They have said {prev_dialoge}'
        )
        
        self.bio = f'{bio}\n{command}'
        self.turn_template = turn_template
        self.talk_template = talk_template
    
    # Input: A string of a list of people, and a string of a list of items
    # Output: The command given and the variable for that command. Both are None if input was invalid
    def turn(self, people = "", items = ""):
        # People looks like 'NOBODY' or 'JOAN, JOHN'. Items looks like 'NOTHING' or 'HAMMER, SHOVEL, SINK'
        
        turn_chain = LLMChain(llm=self.llm, prompt=self.turn_template, verbose=True, output_key='command')
        sequential_chain = SequentialChain(chains=[turn_chain],input_variables=['bio', 'location', 'people', 'items', 'hand_item'], output_variables=['command'], verbose=True)
        
        response = sequential_chain({'bio':self.bio, 'location':self.location, 'people':people, 'items':items, 'hand_item':self.hand_item})
        command, variable = self.command_parsing(response['command'])
        print(f"\n\n|||RESPONSE: {response['command']}")
        
        return command, variable

    # Input: The command the AI gives
    # Output: Divides the command into the command itself and the variable for that command
    def command_parsing(self, input):
        # Commands are: [MOVE] (LOCATION) | [TALK] (NAME) | [PICKUP] (ITEM) | [USE] (ITEM)
        if input.find("[MOVE]"):
            variable = input[input.find("]") + 1:input.find("|")].replace(" ", "")
            command = input[input.find("["):input.find("]") + 1]
            return command, variable
            
        elif input.find("[TALK]"):
            variable = input[input.find("]") + 1:input.find("|")].replace(" ", "")
            command = input[input.find("["):input.find("]") + 1]
            return command, variable
            
        elif input.find("[PICKUP]"):
            variable = input[input.find("]") + 1:input.find("|")].replace(" ", "")
            command = input[input.find("["):input.find("]") + 1]
            return command, variable
        
        elif input.find("[USE]"):
            if self.hand_item == "NOTHING":
                return None, None
            else:
                return "[USE]", None
        elif input.find("[STOPTALKING]"):
            return "[STOPTALKING]", None
        else:
            return None, None
        
    # Input: Other character's name and their previous dialogue
    # Output: This character's respone, and a true/false if they ended conversation.
    def talk(self, char, prev_dialogue = "nothing"):
        
        talking_chain = LLMChain(llm=self.llm, prompt=self.talk_template, verbose=True, output_key='char1')
        sequential_chain = SequentialChain(chains=[talking_chain],input_variables=['other_char', 'prev_dialoge'],output_variables=['dialogue'], verbose=True)
        
        response = sequential_chain({'other_char':char, 'prev_dialogue':prev_dialogue})
        
        command, v = self.command_parsing(response['dialogue'])
        if command == "[STOPTALKING]":
            return response['dialogue'], True
        
        return response['dialogue'], False
    
def run_command(character, command, variable, collision_map, opt):
    if command == "[MOVE]":
        if variable in opt['coordinates']:
            character.location = variable
            path = collision_map.find_path(character.coordinates, opt['coordinates'][variable])
            # Directly iterate over the path
            for location in path:
                character.coordinates = location
        else:
           pass
    elif command == "[TALK]":
        # Implement logic for the [TALK] command
        pass
    elif command == "[PICKUP]":
        # Implement logic for the [PICKUP] command
        pass
    elif command == "[USE]":
        # Implement logic for the [USE] command
        pass
    else:
        # Go Home
        print("hello world")