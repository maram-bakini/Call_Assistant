from dotenv import load_dotenv
import os
from langchain_huggingface import HuggingFaceEndpoint

class LLMHandler:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        self.huggingfacehub_api_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
        
        # Ensure the API token is available
        if not self.huggingfacehub_api_token:
            raise ValueError("HUGGINGFACEHUB_API_TOKEN is not set in the environment variables.")

        # Initialize the LLM
        self.llm = HuggingFaceEndpoint(
            repo_id="meta-llama/Meta-Llama-3-8B-Instruct",
            task="text-generation",
            max_new_tokens=3000,
            huggingfacehub_api_token=self.huggingfacehub_api_token,
            do_sample=False,
        )
    
    def get_llm(self):
        """Returns the LLM instance."""
        return self.llm
