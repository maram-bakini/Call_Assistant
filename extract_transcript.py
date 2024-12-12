from langchain.prompts import ChatPromptTemplate
from Model_setup import LLMHandler
from langchain_core.output_parsers import JsonOutputParser
import streamlit as st
import tempfile
import os
import json
from pathlib import Path
from pydantic import BaseModel, Field, ValidationError
from sum import TranscriptSummarizer


llm_handler = LLMHandler()
llm = llm_handler.get_llama_groq()
summarizerClass=TranscriptSummarizer()



class ExtractTranscript:
    def __init__(self,uploaded_audio_file):
        self.uploaded_file=uploaded_audio_file
        self.llm = llm
        
        self.output_schema="""
{
  "call_transcript": [
    "CSR: ",
    "Custumer: ",
  ]
}

"""
        self.transcript_template = """
List each line of dialogue in the transcript provided between <transcript></transcript> tags, labeling the speaker appropriately.
<transcript>{transcription}</transcript>

Format your response using the following JSON schema:
{output_schema} 

"""     

        self.prompt= ChatPromptTemplate.from_template(
  self.transcript_template,
  partial_variables={
        "output_schema": self.output_schema,
        },
   
)
        self.parser = JsonOutputParser()
        self.chain= ( self.prompt
        |self.llm
        |self.parser
        )
        
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
        
        if self.uploaded_file is not None:
            
            try:
                st.write(f"uploaded_file: {self.uploaded_file.name}")
                st.audio(self.uploaded_file, format='audio/mp3') 
                
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
                    temp_file.write(self.uploaded_file.read())
                    temp_file_path = temp_file.name 
                    
                
                transcription= LLMHandler.get_transcript(temp_file_path)
                
                #st.subheader("Transcription:")
                #st.write(transcription) 
                
                st.subheader("formatted transcript:")
                response=self.chain.invoke(transcription)
                st.write(response)
                response_json = json.dumps(response, indent=2)
                
                    
        
                output_directory = "data"
                if not os.path.exists(output_directory):
                        
                    
                    os.makedirs(output_directory)

                file_path = os.path.join(output_directory, f"Calltranscriptresult.json")
                
                with open(file_path, 'w') as file:
                    file.write(response_json)
                    
                transcripts = Path(r"C:\Users\utente\OneDrive\Bureau\project\Notebooks\data")

                transcript_file = "Calltranscriptresult.json"
                transcript_path = transcripts / transcript_file

                with transcript_path.open("r") as file:
                        
                    transcript = file.read()
                        
                response= summarizerClass.summarize(transcript)
                self.print_summary(response)
                    
            except Exception as e:
                st.error(f"An error occurred while processing the file: {e}")

                
            except Exception as e:
                st.error(f"An error occurred while processing the file: {e}")
        
       
            
                    
                