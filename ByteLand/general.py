""" general.py

Collection of functions to generate and run the AI civilization

"""
import Coding_Utils.coding_utils as cu
from Coding_Utils.coding_utils import err
from Coding_Utils.object import Object

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from langchain.memory import ConversationKGMemory


import os
from apikey import apikey

LOCATIONS = {"Town Square", "Tavern", "Market"}
CHARACTERS = {"Ancient Aiden", "Galliant Gabe", "Magical Miles", "Ye Olde Izzy"}
OBJECTS = {}

os.environ['OPENAI_API_KEY'] = apikey

# [USE] {SWORD}   [MOVE] {SMITHERY}

class Character(Object):
    # TODO: Initialize location with a location class?
    def __init__(self, full_name = "", bio = "", location = "", hand_item = "[NOTHING]"):
        self.full_name = full_name
        self.location = location
        self.hand_item = hand_item
        
        self.llm = OpenAI(temperature=0.9)
        self.memory = ConversationKGMemory(llm=self.llm)
        
        command = 'You must follow these rules: Commands must be enclosed in [] and variables are enclosed in (). Type commands 1 at a time. Enclosed text must be all uppercase. End commands with a "|".Your commands are: [MOVE] (LOCATION) | [TALK] (NAME) | [PICKUP] (ITEM) | [USE] (ITEM)'
        
        turn_template = PromptTemplate(
            input_variable=['location', 'people', 'items'],
            template='You are at {location}. PEOPLE: {people} | ITEMS: {items}'
        )
        
        self.bio = f'{bio}\n{command}'
        self.turn_template = turn_template
    
    def turn(self, location, people, items):
        # People looks like 'NOBODY' or 'JOAN, JOHN'. Items looks like 'NOTHING' or 'HAMMER, SHOVEL, SINK'
        
        turn_chain = LLMChain(llm=self.llm, prompt=self.turn_template, verbose=True, output_key='command')
        sequential_chain = SequentialChain(chains=[turn_chain],input_variables=['location', 'people', 'items'],output_variables=['command'], verbose=True)
        
        response = sequential_chain({'location':location, 'people':people, 'items':items})
        print(response['command'])
        
        
    def talk():
        pass
    
    def addItem():
        pass
    
    def removeItem():
        pass