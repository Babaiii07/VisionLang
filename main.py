import streamlit as st
from backend import uploaded_file_to_response, normal_response
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key='AIzaSyDAG1Hlm4Ge_ou5czvTHP-tyokvYhdE8wA')

llm = Gemini(model_name="models/gemini-1.5-pro")
embeddings = GeminiEmbedding(model_name="models/embedding-001")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.markdown("""
<style>
    .stApp { background-color: #ffffff; color: black; font-family: 'Arial', sans-serif; }
    .title { font-size: 36px; font-weight: bold; text-align: center; animation: fadeIn 2s ease-in-out; }
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    .chat-container { max-height: 500px; overflow-y: auto; display: flex; flex-direction: column-reverse; padding: 10px; border-radius: 10px; background: rgba(0, 0, 0, 0.05); margin-top: 10px; }
    .user-message { background: #0078ff; color: white; padding: 10px; border-radius: 10px; margin-bottom: 5px; text-align: left; }
    .ai-message { background: #f1f1f1; color: black; padding: 10px; border-radius: 10px; margin-bottom: 5px; text-align: left; }
    .btn-style { background: linear-gradient(45deg, #ff007f, #ff0055); color: white; padding: 8px 16px; border-radius: 6px; font-size: 14px; margin-top: 10px; transition: 0.3s ease-in-out; border: none; cursor: pointer; }
    .btn-style:hover { background: linear-gradient(45deg, #ff0055, #d4005a); }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='title'>🧠 AI Code Companion</h1>", unsafe_allow_html=True)
st.caption("🚀 Upload files & chat with AI")

uploaded_file = st.file_uploader("Upload a File (Image, Document, Code, Video, or Audio)", type=["png", "jpg", "jpeg", "pdf", "docx", "txt", "py", "js", "java", "cpp", "mp4"], key="file_uploader")

user_input = st.text_input("Type your message here...", key="chat_input", help="Chat with AI", label_visibility="collapsed")

if st.button("Generate Response", key="generate_button", help="Click to get AI response", use_container_width=False):
    if user_input:
        with st.spinner("Processing..."):
            response = normal_response(user_input)
            if uploaded_file:
                response = uploaded_file_to_response(uploaded_file, user_input)
            st.session_state.chat_history.insert(0, (user_input, response))

if st.session_state.chat_history:
    chat_container = st.container()
    with chat_container:
        st.markdown("### Chat History")
        for user_msg, ai_response in st.session_state.chat_history:
            st.markdown(f"<div class='user-message'><b>You:</b> {user_msg}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='ai-message'><b>AI:</b> {ai_response}</div>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
