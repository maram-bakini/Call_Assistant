import streamlit as st
import json
import re
from pydantic import BaseModel, Field, ValidationError
from typing import List
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain_ollama import ChatOllama
from langchain.chains import LLMChain

class TranscriptSummarizerPage:
    def __init__(self, model_name="llama3.2", temperature=0):
        self.llm = ChatOllama(model=model_name, temperature=temperature)
        self.summarization_parser = PydanticOutputParser(pydantic_object=self.CallSummary)
        self.summarization_prompt = ChatPromptTemplate.from_template(
            """
            Please provide a summary of the following call transcript provided between <transcript></transcript> tags. 
            Capture key takeaways and specific follow up actions. 
            Skip the preamble and go straight to the answer.

            <transcript>{transcript}</transcript>

            Format your response per the instructions below: 
            {format_instructions} 

            dont show the properties of the instructions 
            Place your response between <output></output> tags. 
            """,
            partial_variables={
                "format_instructions": self.summarization_parser.get_format_instructions()
            },
        )

    class CallSummary(BaseModel):
        call_summary: str = Field(description="Call transcript summary: ")
        key_takeaways: List[str] = Field(description="Call transcript key takeaways: ")
        follow_up_actions: List[str] = Field(description="Call Transcript key action items: ")

    @staticmethod
    def extract_from_xml_tag(response: str, tag: str) -> str:
        tag_txt = re.search(rf'<{tag}>(.*?)</{tag}>', response, re.DOTALL)
        if tag_txt:
            return tag_txt.group(1)
        else:
            st.error("No JSON found in the response.")
            st.text(response)
            return ""

    def run(self):
        st.title("Call Transcript Summarizer")

        # File uploader widget
        uploaded_file = st.file_uploader("Upload a call transcript (JSON format):", type="json")

        if uploaded_file is not None:
            try:
                # Load and read the transcript
                transcript = uploaded_file.read().decode("utf-8")

                # Set up the LLMChain with the template and model
                chain = LLMChain(
                    llm=self.llm,
                    prompt=self.summarization_prompt,
                )

                # Run the chain and get the response
                response = chain.run(transcript=transcript)
                json_output = self.extract_from_xml_tag(response, "output")

                # Parse the output into structured data
                try:
                    summary = self.summarization_parser.parse(json_output)
                    st.subheader("Call Summary")
                    st.write(summary.call_summary)

                    st.subheader("Key Takeaways")
                    st.write("- " + "\n- ".join(summary.key_takeaways))

                    st.subheader("Follow Up Actions")
                    st.write("- " + "\n- ".join(summary.follow_up_actions))
                except ValidationError as e:
                    st.error("Error parsing response from the model:")
                    st.text(e)

            except Exception as e:
                st.error("An error occurred while processing the file:")
                st.text(e)
        else:
            st.info("Please upload a JSON file to begin.")
