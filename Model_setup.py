from dotenv import load_dotenv
import os
from langchain_huggingface import HuggingFaceEndpoint
from langchain_groq import ChatGroq
from groq import Groq


class LLMHandler:
    def __init__(self):
        load_dotenv()
        self.huggingfacehub_api_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        if not self.huggingfacehub_api_token:
            raise ValueError("HUGGINGFACEHUB_API_TOKEN is not set in the environment variables.")

        self.llama3 = HuggingFaceEndpoint(
            repo_id="meta-llama/Meta-Llama-3-8B-Instruct",
            task="text-generation",
            huggingfacehub_api_token=self.huggingfacehub_api_token,
            do_sample=False,
        )
        
        
        self.llama_groq= ChatGroq(
    model="llama3-8b-8192",
    temperature=0.3,
    top_p=1,
    max_retries=2,
    stream=False,
    response_format={"type": "json_object"},
    stop=None,
)
        
    
    def get_llama3(self):
        """Returns the LLM instance."""
        return self.llama3
    
    def get_llama_groq(self):
        
        return self.llama_groq
    
    def get_transcript(filename):
        
        with open(filename, "rb") as file:
            transcription = Groq().audio.transcriptions.create(
      file=(filename, file.read()),
      model="whisper-large-v3",
      response_format="verbose_json",
    )
        return transcription.text
       
    
        