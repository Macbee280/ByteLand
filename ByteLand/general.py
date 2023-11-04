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


import os
from apikey import apikey

LOCATIONS = {"Town Square", "Tavern", "Market"}
CHARACTERS = {"Ancient Aiden", "Galliant Gabe", "Magical Miles", "Ye Olde Izzy"}
OBJECTS = {}

os.environ['OPENAI_API_KEY'] = apikey

# [USE] {SWORD}   [MOVE] {SMITHERY}

class Character():
    # TODO: Initialize location with a location class?
    def __init__(self, name = "", bio = "", location = "", hand_item = "NOTHING"):
        self.name = name
        self.location = location
        self.hand_item = hand_item
        
        self.llm = OpenAI(temperature=0.9)
        self.memory = ConversationSummaryMemory(llm=self.llm)
        
        command = 'You must follow these rules: Commands must be enclosed in [] and variables are enclosed in (). Type commands 1 at a time. Enclosed text must be all uppercase. End commands with a "|". Your commands are: [MOVE] (LOCATION) | [TALK] (NAME) | [PICKUP] (ITEM) | [USE] - this uses the item in your hand'
        
        turn_template = PromptTemplate(
            input_variables=['bio', 'location', 'people', 'items', 'hand_item'],
            template='{bio}\n\nYou are at {location}. PEOPLE: {people} | ITEMS: {items} | IN HAND ITEM: {hand_item} '
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
    def turn(self, people = "NOBODY", items = "NOTHING"):
        # People looks like 'NOBODY' or 'JOAN, JOHN'. Items looks like 'NOTHING' or 'HAMMER, SHOVEL, SINK'
        
        turn_chain = LLMChain(llm=self.llm, prompt=self.turn_template, verbose=True, output_key='command')
        sequential_chain = SequentialChain(chains=[turn_chain],input_variables=['bio' 'location', 'people', 'items', 'hand_item'],output_variables=['command'], verbose=True)
        
        response = sequential_chain({'bio':self.bio, 'location':self.location, 'people':people, 'items':items, 'hand_item':self.hand_item})
        command, variable = self.command_parsing(response['command'])
        
        return command, variable

    # Input: The command the AI gives
    # Output: Divides the command into the command itself and the variable for that command
    def command_parsing(self, input):
        # Commands are: [MOVE] (LOCATION) | [TALK] (NAME) | [PICKUP] (ITEM) | [USE] (ITEM)
        if input.find("[MOVE]"):
            variable = input[input.find("]") + 1:input.find("|")].replace(" ", "")
            return "[MOVE]", variable
            
        elif input.find("[TALK]"):
            variable = input[input.find("]") + 1:input.find("|")].replace(" ", "")
            return "[TALK]", variable
            
        elif input.find("[PICKUP]"):
            variable = input[input.find("]") + 1:input.find("|")].replace(" ", "")
            return "[PICKUP]", variable
        
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
    