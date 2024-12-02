import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain.chains import LLMChain




# --- Streamlit Configuration ---
st.set_page_config(page_title="AI-Powered Clinical Tools", layout="wide")
st.title("🏥 AI-Powered Clinical Tools")
st.sidebar.title("Navigation")

app_mode = st.sidebar.selectbox(
    "Choose a Tool",
    [
        "Home",
        "Clinical Documentation Assistant",
        "Research Paper Summarizer",
        "Heart Disease QA Chatbot",
    ]
)


if app_mode == "Home":
    st.markdown("""
    ### Welcome to AI-Powered Clinical Tools!
    - **Clinical Documentation Assistant**: Automatically generate structured notes (SOAP notes).
    - **Research Paper Summarizer**: Extract key insights from dense research papers.
    - **Heart Disease QA Chatbot**: Answer questions related to heart disease based on curated documents.
    """)
    


llm = ChatOllama(model="llama3.2", temperature=0)
chain = LLMChain(
            llm=llm,
            prompt=PromptTemplate(
                input_variables=["text"],
                template="Generate a SOAP note from the following clinical details:\n\n{text}"
            )
        )

st.header("📝 Clinical Documentation Assistant")
user_input = st.text_area("Enter or paste clinical details here:")
if st.button("Generate SOAP Note"):
    
    if user_input:
        soap_note = chain.run({"text": user_input})
        st.subheader("Generated SOAP Note:")
        st.text_area("SOAP Note Output", soap_note, height=300)
        st.download_button("Download SOAP Note", data=soap_note, file_name="SOAP_Note.txt")
    else:
        st.warning("Please provide clinical details.")
