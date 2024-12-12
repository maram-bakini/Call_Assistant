import streamlit as st
import json
import re
from pydantic import Field, ValidationError
from typing import List
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from Model_setup import LLMHandler
from langchain_core.output_parsers import JsonOutputParser
from extract_transcript import ExtractTranscript


llm_handler = LLMHandler()
llm = llm_handler.get_llama_groq()


class TranscriptSummarizerPage:
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
    def chain(self):
        return self.chain
        
        
    def print_summary(self, response):
            
            
        desired_response = {
            'call_summary': response['output'].get('call_summary'),
            'key_takeaways': response['output'].get('key_takeaways'),
            'follow_up_actions': response['output'].get('follow_up_actions'),
        }
        try:
                
            st.subheader("Call Summary")
            st.write(desired_response['call_summary'])
            st.subheader("Key Takeaways")
            st.write("- " + "\n- ".join(desired_response["key_takeaways"]))
            st.subheader("Follow Up Actions")
            st.write("- " + "\n- ".join(desired_response["follow_up_actions"]))
        except ValidationError as e:
            st.error("Error parsing response from the model:")
            st.text(e)
   

    def run(self):
              
        uploaded_json_file = st.file_uploader("Upload a call transcript (JSON format):", type="json")
        uploaded_audio_file = st.file_uploader("Upload a call transcript audio file:", type=["wav", "mp3", "ogg"])
        if uploaded_json_file  is not None:
            try:
                transcript = uploaded_json_file.read().decode("utf-8")
                response = self.chain.invoke(transcript)
                self.print_summary(response)
                
            except Exception as e:
                
                st.error("An error occurred while processing the file:")
                st.text(e)  
              
        elif uploaded_audio_file is not None:
            
            extracttranscript=ExtractTranscript(uploaded_audio_file)
            extracttranscript.run()
            
        
        else:
            st.info("Please upload a JSON or Audio file to begin.")
