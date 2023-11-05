""" general.py

Collection of functions to generate and run the AI civilization

"""
#import Coding_Utils.coding_utils as cu
#from Coding_Utils.coding_utils import err
#from Coding_Utils.object import Object
import streamlit as st

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from langchain.memory import ConversationSummaryMemory

from Backend.navigation import *
from gtts import gTTS
import tempfile
import os
from apikey2 import apikey
from IPython.display import Audio
import time
from mutagen.mp3 import MP3

os.environ['OPENAI_API_KEY'] = apikey

# [USE] {SWORD}   [MOVE] {SMITHERY}

def play_audio_and_wait(file_path):
    audio = Audio(file_path, autoplay=True)
    st.write(audio)
    audio

def get_audio_duration(file_path):
    audio = MP3(file_path)
    return audio.info.length

class Character():
    def __init__(self, name = "", bio = "", location = "TOWNSQUARE", hand_item = "", coordinates = (0,0)):
        self.name = name
        self.location = location
        self.hand_item = hand_item
        self.coordinates = coordinates
        
        self.llm = OpenAI(temperature=0.9)
        self.memory = ConversationSummaryMemory(llm=self.llm, memory_key='history', input_key='input', human_prefix='instructions', ai_prefix=f"Human {self.name}")
        
        command = 'You must follow these rules: Commands must be enclosed in []. Input one total command. Enclosed text must be all uppercase. End commands with a "|". Your commands are: [MOVE] (LOCATION) and [TALK] (NAME) and [PICKUP] (ITEM) and [USE] - this uses the item in your hand'
        
        turn_template = PromptTemplate(
            input_variables=['input', 'history', 'bio', 'location', 'people', 'items', 'hand_item'],
            template='{bio}\nHistory: {history}\nYou can only [MOVE] to these locations: TOWNSQUARE, TAVERN, and MARKET.\nYou are at {location} | PEOPLE: {people} | ITEMS: {items} | IN HAND ITEM: {hand_item}\nEnter a single command:'
        )
        
        talk_template = PromptTemplate(
            input_variables=['input', 'history', 'other_char', 'location' 'prev_dialogue'],
            template='History: {history}\nEnter command [STOPTALKING] to end dialogue. You are talking to {other_char} at the {location}. They said "{prev_dialogue}"\nYour response:'
        )
        
        self.bio = f'{bio}\n{command}'
        self.turn_template = turn_template
        self.talk_template = talk_template
    
    # Input: A string of a list of people, and a string of a list of items
    # Output: The command given and the variable for that command. Both are None if input was invalid
    def turn(self, people="", items = ""):
        # People looks like 'NOBODY' or 'JOAN, JOHN'. Items looks like 'NOTHING' or 'HAMMER, SHOVEL, SINK'
        
        turn_chain = LLMChain(llm=self.llm, prompt=self.turn_template, memory=self.memory, verbose=True, output_key='command')
        
        response = turn_chain({'bio':self.bio, 'input':"", 'location':self.location, 'people':people, 'items':items, 'hand_item':self.hand_item})
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
    def talk(self, char, prev_dialogue = ""):
        
        talking_chain = LLMChain(llm=self.llm, prompt=self.talk_template, verbose=True, output_key='dialogue', memory=self.memory)
        response = talking_chain({'input':"", 'other_char':char, 'location':self.location, 'prev_dialogue':prev_dialogue})
        
        command, v = self.command_parsing(response['dialogue'])
        if command.find("STOPTALKING") != -1:
            return response['dialogue'], True
        
        return response['dialogue'], False
    
def run_command(character, command, variable, collision_map, opt, CHARACTERS={}):
    if command == "[MOVE]":
        if variable in opt['coordinates']:
            st.write(f"[{character.name} moved from {character.location} to {variable} ]")
            character.location = variable
            path = collision_map.find_path(character.coordinates, opt['coordinates'][variable])
            # Directly iterate over the path
            for location in path:
                #TODO: Interface with frontend here
                character.coordinates = location
        else:
            pass
    elif command == "[TALK]":
        # Implement logic for the [TALK] command
        prev_dialogue = ""
        try:
            other_char = CHARACTERS[variable]
        except Exception as exception:
            print("Made up a person")
            return
            
        for i in range(2):
            dialogue, end = character.talk(variable, prev_dialogue)
            st.write(f"{character.name}: {dialogue}")  #TODO: Interface with frontend here
            tts = gTTS(f"{character.name}: {dialogue}")

            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                tts.save(tmp_file.name)

            play_audio_and_wait(tmp_file.name)
            duration = get_audio_duration(tmp_file.name)
            time.sleep(duration-1)
            os.unlink(tmp_file.name)

            if end:
                break
            
            prev_dialogue, end = other_char.talk(character.name, dialogue)
            st.write(f"{other_char.name}: {prev_dialogue}") #TODO: Interface with frontend here
            tts = gTTS(f"{other_char.name}: {prev_dialogue}")

            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                tts.save(tmp_file.name)

            play_audio_and_wait(tmp_file.name)
            duration = get_audio_duration(tmp_file.name)
            time.sleep(duration-1)
            os.unlink(tmp_file.name)
                    
            if end:
                break
            
    elif command == "[PICKUP]":
        # Implement logic for the [PICKUP] command
        pass
    elif command == "[USE]":
        # Implement logic for the [USE] command
        pass
    else:
        # Go Home
        print("hello world")