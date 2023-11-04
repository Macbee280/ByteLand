import os
from apikey import apikey

import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from langchain.memory import ConversationBufferMemory


os.environ['OPENAI_API_KEY'] = apikey

st.title('Test Application')
prompt = st.text_input('Plug in your prompt')

title_template = PromptTemplate(
    input_variables=['topic'],
    template='Write me a youtube vieo title about {topic}'
)

script_template = PromptTemplate(
    input_variables=['title'],
    template='Write me a youtube vieo script based on this title TITLE: {title}'
)

memory = ConversationBufferMemory(input_key='topic', memory='chat_history')

llm = OpenAI(temperature=0.9)
title_chain = LLMChain(llm=llm, prompt=title_template, verbose=True, output_key='title')
script_chain = LLMChain(llm=llm, prompt=script_template, verbose=True, output_key='script')
sequential_chain = SequentialChain(chains=[title_chain,script_chain],input_variables=['topic'],output_variables=['title','script'], verbose=True)

if prompt:
    response = sequential_chain({'topic':prompt})
    st.write(response['title'])
    st.write(response['script'])

    with st.expander('Message History'):
        st.info(memory.buffer)