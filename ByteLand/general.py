""" general.py

Collection of functions to generate and run the AI civilization

"""
import Coding_Utils.coding_utils as cu
from Coding_Utils.coding_utils import err
from Coding_Utils.object import Object

# [USE] {SWORD}   [MOVE] {SMITHERY}

class Character(Object):
    # TODO: Initialize location with a location class?
    def __init__(self, full_name = "", bio = "", location = "", hand_item = "[NOTHING]"):
        self.full_name = full_name
        self.bio = bio
        self.location = location
        self.hand_item = hand_item
        
        llm = OpenAI(temperature=0)
        conversation_with_summary = ConversationChain(
            llm=llm,
            memory=ConversationSummaryMemory(llm=OpenAI()),
            verbose=True
        )
    
    def turn():
        pass
    
    def addItem():
        pass
    
    def removeItem():
        pass