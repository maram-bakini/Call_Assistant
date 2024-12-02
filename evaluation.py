import streamlit as st
import json
from pydantic import BaseModel, Field
from typing import List
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain_ollama import ChatOllama
from langchain_core.runnables import RunnableLambda
from enum import Enum


class ScoreValue(Enum):
    
    High = "High"
    Medium = "Medium"
    Low = "Low"
    
class Score(BaseModel):
        score: ScoreValue
        score_explanation: str

class CallAssessmentPage:
    def __init__(self, model_name="llama3.2", temperature=0):
        self.llm = ChatOllama(model=model_name, temperature=temperature)

        # Define the one-shot example
        self.one_shot_example = """
        Evaluation:
{{
  "Communication_Skills": {{
    "score": "Medium",
    "score_explanation": "The CSR communicated adequately but could have been more concise and used more empathetic language when addressing the customer's frustration."
  }},
  "Problem_Resolution": {{
    "score": "High",
    "score_explanation": "The CSR resolved the customer's issue by offering an immediate refund and finding an alternative flight that met the customer's needs."
  }},
  "Product_Knowledge": {{
    "score": "High",
    "score_explanation": "The CSR showed a strong understanding of the company's policies and was able to clearly explain the details of the flight refund process."
  }},
  "Professionalism": {{
    "score": "High",
    "score_explanation": "The CSR maintained a professional demeanor throughout the conversation, addressing the customer's concerns respectfully and patiently."
  }},
  "Problem_Escalation": {{
    "score": "Medium",
    "score_explanation": "The CSR acknowledged the issue but did not transfer the call to a supervisor until further prompting from the customer."
  }},
  "Resolution_Follow_Up": {{
    "score": "High",
    "score_explanation": "The CSR mentioned the follow-up procedure and confirmed that an email would be sent to the customer for further details."
  }},
  "Efficiency": {{
    "score": "Medium",
    "score_explanation": "The call was handled in a reasonable timeframe but included pauses to verify flight details, causing some delays."
  }},
  "Adherence_to_Policies_and_Procedures": {{
    "score": "High",
    "score_explanation": "The CSR accurately followed all company policies, ensuring that the refund and rebooking were processed correctly."
  }},
  "Technical_Competence": {{
    "score": "Medium",
    "score_explanation": "The CSR navigated the systems well but took longer than expected to find the necessary information for the refund."
  }},
  "Customer_Satisfaction": {{
    "score": "High",
    "score_explanation": "The customer expressed appreciation for the quick response and the options provided, despite initial frustration."
  }},
  "Language_Proficiency": {{
    "score": "High",
    "score_explanation": "The CSR used clear and professional language throughout the call, ensuring that the customer understood the process."
  }},
  "Conflict_Resolution": {{
    "score": "Medium",
    "score_explanation": "The CSR managed the customer's irritation well, though some de-escalation techniques could have been more proactive."
  }}
}}
        """

        # Prompt template with one-shot example
        self.assessment_template = f"""
        {{{{call_transcript}}}}

        {self.one_shot_example}
        Now evaluate the given call transcript and provide the output in the same format as the example.
        Ensure that the evaluation uses the exact category names and underscores as shown in the example.
        Ensure that the output is only JSON without any additional text.
        """
        self.assessment_prompt = ChatPromptTemplate.from_template(self.assessment_template)

        # Define processing functions
        self.process_transcript = RunnableLambda(self._process_transcript)
        self.extract_content = RunnableLambda(self._extract_content)

   



    class Evaluation(BaseModel):
        Communication_Skills: Score
        Problem_Resolution: Score
        Product_Knowledge: Score
        Professionalism: Score
        Problem_Escalation: Score
        Resolution_Follow_Up: Score
        Efficiency: Score
        Adherence_to_Policies_and_Procedures: Score
        Technical_Competence: Score
        Customer_Satisfaction: Score
        Language_Proficiency: Score
        Conflict_Resolution: Score

    def _process_transcript(self, transcript: str) -> str:
        """
        Extracts and formats the call transcript from the input JSON.
        """
        json_transcript = json.loads(transcript)
        call_transcript = "\n".join(json_transcript.get("call_transcript", []))
        return f"Call Transcript:\n{call_transcript}"

    def _extract_content(self, message):
        """
        Extracts the content from the message, converting it to a string if necessary.
        """
        if hasattr(message, 'content') and isinstance(message.content, str):
            return message.content
        return str(message)  # Fallback to string conversion

    def run(self):
        st.title("📈 Call Assessment Tool")
        st.markdown("""
        Use this tool to automatically evaluate customer service calls based on multiple criteria.
        Upload a call transcript in JSON format, and the AI will analyze it and provide structured feedback.
        """)

        # File uploader
        uploaded_file = st.file_uploader("Upload a call transcript (JSON format):", type="json")

        if uploaded_file:
            try:
                # Read the uploaded file
                transcript = uploaded_file.read().decode("utf-8")

                # Construct the assessment chain
                assessment_chain = (
                    {"transcript": self.process_transcript}
                    | self.assessment_prompt
                    | self.llm
                    | self.extract_content
                )

                # Run the chain
                call_assessment = assessment_chain.invoke(transcript)
                parsed_evaluation = self.Evaluation.parse_raw(call_assessment)

                # Display results
                st.subheader("Call Evaluation Results")
                for category, score in parsed_evaluation.dict().items():
                    st.markdown(f"### {category}")
                    st.write(f"**Score:** {score['score']}")
                    st.write(f"**Explanation:** {score['score_explanation']}")

            except Exception as e:
                st.error("An error occurred while processing the file:")
                st.text(e)
        else:
            st.info("Please upload a JSON file to begin.")
