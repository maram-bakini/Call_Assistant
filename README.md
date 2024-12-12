# **Customer Service Call Evaluation and Summarization System**

This project implements an AI-powered solution that processes customer service (CSR) call transcripts and generates a summary, key takeaways, follow-up actions, and evaluates the CSR's performance based on multiple criteria. The solution is capable of processing both JSON and audio call files, leveraging advanced natural language processing (NLP) and generative AI models to analyze and evaluate the call content.

## **Table of Contents**
1. [Overview](#overview)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [Prerequisites](#prerequisites)
5. [Installation](#installation)
6. [How It Works](#how-it-works)
    - [Step 1: Call Transcript Summarization](#step-1-call-transcript-summarization)
    - [Step 2: Key Takeaways & Follow-Up Actions](#step-2-key-takeaways--follow-up-actions)
    - [Step 3: Evaluation of CSR Performance](#step-3-evaluation-of-csr-performance)
7. [File Formats](#file-formats)
8. [Running the Application](#running-the-application)
9. [Customization and Improvements](#customization-and-improvements)
10. [Contributing](#contributing)
11. [License](#license)

## **Overview**

The Customer Service Call Evaluation and Summarization System is a comprehensive tool for processing customer service call data. The system can:
- Process a call transcript (either in JSON or audio format).
- Automatically generate a summary of the call.
- Extract key takeaways and recommend follow-up actions.
- Evaluate CSR performance based on predefined criteria like communication skills, problem resolution, professionalism, etc.

This solution leverages **Generative AI models** and **Natural Language Processing (NLP)** techniques to provide detailed and actionable insights for customer service management.

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
- **Real-Time Processing with Streamlit**: Built with **Streamlit**, providing an easy-to-use, interactive user interface for uploading files and displaying results.

## **Technologies Used**
- **LangChain**: A framework for building and managing LLM pipelines.
- **OpenAI API / Ollama**: For generative AI models used for summarization and evaluation.
- **Pydantic**: For data validation and parsing.
- **Streamlit**: For building the web interface.
- **Speech-to-Text Models**: For converting audio files into text.
- **Python**: For the main application logic.

## **Prerequisites**
Before running this project, make sure you have the following installed:
- Python 3.7 or later
- Streamlit
- Pydantic
- LangChain
- OpenAI or Ollama API credentials
- Libraries for audio processing (e.g., **pydub**, **speech_recognition**)

### Install dependencies:
```bash
pip install streamlit langchain openai pydantic
