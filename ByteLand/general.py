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
from langchain.memory import ConversationSummaryBufferMemory


import os
from apikey import apikey

LOCATIONS = {"Town Square", "Tavern", "Market"}
CHARACTERS = {"Ancient Aiden", "Galliant Gabe", "Magical Miles", "Illusionary Izzy"}
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
        self.memory = ConversationSummaryBufferMemory(llm=self.llm, max_token_limit=10)
        
        bio_template = PromptTemplate(
            input_variables=['bio'],
            template='{bio} Commands must be enclosed in square brackets [], and variables are enclosed in angle brackets <>: [MOVE] <LOCATION>: To move to a specific location. [TALK] <NAME>: To engage in conversation with a named entity. [PICKUP] <ITEM>: To pick up a specified item. [USE] <ITEM>: To use a specific item.'
        )
        
        self.bio = bio_template
    
    def turn():
        pass
    
    def addItem():
        pass
    
    def removeItem():
        pass