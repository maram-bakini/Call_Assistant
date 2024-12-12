
import streamlit as st
import json
import re
from pydantic import  ValidationError
from typing import List
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain.chains import LLMChain
from Model_setup import LLMHandler
from langchain_core.output_parsers import JsonOutputParser



llm_handler = LLMHandler()
llm = llm_handler.get_llama_groq()







class TranscriptSummarizer:
    def __init__(self):
        self.llm = llm
        #ChatOllama(model=model_name, temperature=temperature)
        self.output_schema = {
    "properties": {
        "call_summary": {
            "description": "Call transcript summary: ",
            "title": "Call Summary",
            "type": "string"
        },
        "key_takeaways": {
            "description": "Call transcript key takeaways: ",
            "items": {"type": "string"},
            "title": "Key Takeaways",
            "type": "array"
        },
        "follow_up_actions": {
            "description": "Call transcript key action items: ",
            "items": {"type": "string"},
            "title": "Follow Up Actions",
            "type": "array"
        }
    },
    "required": ["call_summary", "key_takeaways", "follow_up_actions"]
}
        self.summarization_template = """

Please provide a summary of the following call transcript provided between <transcript></transcript> tags. 
Capture key takeaways and specific follow-up actions. 
Skip the preamble and go straight to the answer.

<transcript>{transcript}</transcript>


Format your response using the following JSON schema:
{output_schema}

Place your response between <output></output> tags.
"""
        self.parser = JsonOutputParser()
 

        self.summarization_prompt = ChatPromptTemplate.from_template(
        self.summarization_template,
    partial_variables={
        "output_schema": self.output_schema,
        },
)
        
        self.chain = ( self.summarization_prompt
    | self.llm
    | self.parser
)
    def summarize(self, transcript):
        try:
            
            response = self.chain.invoke(transcript)
            return response
        except Exception as e:
            raise ValueError(f"An error occurred during summarization: {str(e)}")