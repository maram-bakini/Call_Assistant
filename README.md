# **Customer Service Call Evaluation and Summarization System**

This project implements an AI-powered solution that processes customer service (CSR) call transcripts and generates a summary, key takeaways, follow-up actions, and evaluates the CSR's performance based on multiple criteria. The solution is capable of processing both JSON and audio call files generative AI models to analyze and evaluate the call content.

## **Table of Contents**
1. [Features](#features)
2. [Technologies Used](#technologies-used)

## **Features**
- **Call Summarization**: Automatically generates a concise summary of a customer service call.
- **Key Takeaways**: Extracts the most important information and points discussed during the call.
- **Follow-Up Actions**: Suggests potential follow-up actions based on the outcome of the conversation.
- **CSR Evaluation**: Evaluates the CSR's performance across multiple metrics such as:
  - Communication Skills
  - Problem Resolution
  - Customer Satisfaction
  - Technical Competence
  - Efficiency, and more.
- **Supports JSON and Audio Input**: The system can process both JSON files (containing the call transcript) and audio files (converted to text using speech-to-text models).
- **UI with Streamlit**: Built with **Streamlit**, providing an easy-to-use, interactive user interface for uploading files and displaying results.

## **Technologies Used**
- **LangChain**: A framework for building and managing LLM pipelines.
- **Groq**: For generative AI models used for summarization and evaluation.
- **Pydantic**: For data validation and parsing.
- **Streamlit**: For building the web interface.
- **Speech-to-Text Models**: For converting audio files into text.
- **Python**: For the main application logic.

