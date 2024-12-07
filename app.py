import streamlit as st
from langchain_ollama import ChatOllama
from Summarizer import TranscriptSummarizerPage  # Assuming the class is in `transcript_summarizer_page.py`
from evaluation import CallAssessmentPage  # Assuming the class is in `call_assessment_page.py`

# Initialize the CallAssessmentPage
assessment_page = CallAssessmentPage()

# Initialize the summarizer page
summarizer_page = TranscriptSummarizerPage()
llm = ChatOllama(model="llama3.2", temperature=0)

def main():
    # --- Streamlit Configuration ---
    st.set_page_config(
        page_title="AI-Powered Customer Support Tools", 
        layout="wide", 
        page_icon="💼"
    )
    st.title("💼 AI-Powered Customer Support Tools")
    st.sidebar.title("Navigation")

    # Sidebar navigation
    app_mode = st.sidebar.radio(
        "Choose a Tool:",
        [
            "Home",
            "Call Transcript Summarizer",
            "Call Assessment"
        ]
    )

    if app_mode == "Home":
        st.markdown("""
        ## Welcome to AI-Powered Customer Support Tools!
        
        Streamline your customer support operations with cutting-edge AI solutions:
        
        - **Call Transcript Summarizer**: Summarize and extract actionable insights from customer calls.
        - **Customer Feedback Analyzer**: Gain insights into customer sentiment and preferences from feedback.
        - **Chatbot Optimization Advisor**: Improve your chatbot's effectiveness through AI analysis.
        """)
        
        st.image("https://source.unsplash.com/1200x300/?customer-support", caption="Empowering Support Teams")
        st.info(
            "💡 Tip: Use these tools to enhance customer satisfaction, reduce response times, and improve support team efficiency."
        )

    elif app_mode == "Call Transcript Summarizer":
        st.header("📞 Call Transcript Summarizer")
        st.markdown("""
        Use this tool to quickly analyze customer call transcripts. The AI generates:
        - A concise **summary** of the call.
        - Key **takeaways** to share with your team.
        - Follow-up **action items** to ensure nothing is missed.
        """)
        summarizer_page.run()
    elif app_mode == "Call Assessment":
        assessment_page.run()
    
        

if __name__ == "__main__":
    main()
