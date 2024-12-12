import streamlit as st
from Summarizer import TranscriptSummarizerPage  
from evaluation import CallAssessmentPage 
from extract_transcript import ExtractTranscript
assessment_page = CallAssessmentPage()

summarizer_page = TranscriptSummarizerPage()


def main():
    st.set_page_config(
        page_title="AI-Powered Customer Support Tools", 
        layout="wide", 
        page_icon="💼"
    )
    st.title("💼 AI-Powered Customer Support Tools")
    st.sidebar.title("Navigation")

    app_mode = st.sidebar.radio(
        "Choose a Tool:",
        [
            "Home",
            "Call Transcript Summarizer",
            "Call Assessment",
        ]
    )

    if app_mode == "Home":
        st.markdown("""        
        Streamline your customer support operations with cutting-edge AI solutions:

        - **Call Transcript Summarizer**: Summarize and extract actionable insights from customer calls.
        - **Call Evaluation**: automatically evaluate customer service calls.
        """)
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
