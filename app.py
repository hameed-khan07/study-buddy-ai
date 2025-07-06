import streamlit as st
import google.generativeai as genai
import os

# --- Configuration ---
# API key ko load karein. Priority: Streamlit secrets (for deployment) -> Environment variable (for local testing)
try:
    # For Streamlit Cloud deployment, it fetches from .streamlit/secrets.toml
    API_KEY = st.secrets["GOOGLE_API_KEY"]
except KeyError:
    # For local testing, it fetches from environment variables (e.g., set in your terminal before running)
    # Windows PowerShell: $env:GOOGLE_API_KEY="YOUR_ACTUAL_API_KEY"
    # Linux/macOS Bash: export GOOGLE_API_KEY="YOUR_ACTUAL_API_KEY"
    API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("API Key not found. Please set your Google Gemini API Key as an environment variable `GOOGLE_API_KEY` or add it to your `.streamlit/secrets.toml` file.")
    st.stop() # Stop the app if the key is not found

genai.configure(api_key=API_KEY)

# Initialize the Gemini Generative Model
# You can use 'gemini-pro', or if you have access,
# 'gemini-1.5-pro-latest' for more advanced capabilities.
model = genai.GenerativeModel('gemini-2.0-flash') 

# --- AI Explanation Function ---
def get_ai_explanation(question):
    # Prompt Engineering: Give the AI a specific persona and define the output format
    # We've refined the prompt slightly to encourage better answers
    prompt = f"""
    You are a helpful, patient, and knowledgeable Study Buddy AI. Your primary goal is to
    explain complex concepts to students in a simple, understandable, and concise manner.
    Respond in English. If possible, provide a short and clear example that aids understanding.
    
    Question/Concept: '{question}'
    """
    
    # --- HERE IS THE 'TRY' BLOCK ---
    try:
        # Show a Streamlit spinner while the AI is generating the response
        with st.spinner("Understanding your question and preparing the answer... Please wait."):
            response = model.generate_content(prompt)
            # Ensure the response is text and not empty
            if response and response.text:
                return response.text
            else:
                return "Sorry, the AI could not generate a response. Please try to clarify the question slightly or try again."
    # --- THIS IS THE 'EXCEPT' BLOCK, ALIGNED WITH 'TRY' ---
    except Exception as e: 
        # Error handling: if there's an issue with the API call
        st.error(f"Sorry, a technical error occurred while trying to answer your question. Please try again. Error: {e}")
        return "Could not provide an answer."

# --- Streamlit User Interface ---
st.set_page_config(page_title="Study Buddy AI", page_icon="📚", layout="centered")

st.title("📚 Study Buddy AI: Your AI Study Companion")
st.markdown("""
Hello! I am your personal AI Study Buddy. You can ask me questions on any topic, and I will explain them to you in a simple and understandable way.
""")

# User input area
user_question = st.text_area(
    "What do you need explained? Type your question or concept here.",
    placeholder="e.g., What is photosynthesis? OR Explain recursion in programming.",
    height=120
)

# Button to trigger AI explanation
if st.button("Explain!", key="explain_button", help="Get an explanation for your question."):
    if user_question:
        # Call the AI explanation function
        explanation = get_ai_explanation(user_question)
        
        st.subheader("💡 Explanation:")
        st.markdown(explanation) # Markdown support for better formatting
    else:
        st.warning("Please enter your question or concept so I can help you.")

st.markdown("---")
st.caption("© 2025 Study Buddy AI. Built with Google Gemini and Streamlit.")
st.markdown("**Disclaimer:** This AI is intended to provide assistance. Always verify information for accuracy.")