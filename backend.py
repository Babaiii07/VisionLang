import google.generativeai as genai
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding
import os
import tempfile
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import Settings
import time
from google.api_core.exceptions import GoogleAPIError
import streamlit as st

genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

llm = Gemini(model_name="models/gemini-1.5-pro")
embeddings = GeminiEmbedding(model_name="models/embedding-001")

def normal_response(query):
    prompt = """You are a helpful Bot named VisionLang Build by Parthib Karak.
    Given a question, generate answer based on the Question.
    Question: {question}
    """
    try:
        response = llm.complete(prompt + query)
        return response.text
    except GoogleAPIError as e:
        return f"Error generating response: {str(e)}"

def uploaded_file_to_response(file, query):
    file_extension = os.path.splitext(file.name)[-1].lower()
    try:
        if file_extension in [".pdf", ".docx", ".txt", ".py", ".js", ".java", ".cpp"]:
            temp_dir = tempfile.mkdtemp()
            temp_file_path = os.path.join(temp_dir, file.name)
            with open(temp_file_path, "wb") as f:
                f.write(file.read())
            
            document = SimpleDirectoryReader(temp_dir)
            data = document.load_data()
            Settings.llm = llm
            Settings.embed_model = embeddings
            index = VectorStoreIndex.from_documents(data, settings=Settings)
            query_engine = index.as_query_engine()
            response = query_engine.query(query)
            return response
        elif file_extension in [".mp4", ".avi", ".mov",".mkv"]:
            temp_dir = tempfile.mkdtemp()
            temp_file_path = os.path.join(temp_dir, file.name)
            with open(temp_file_path, "wb") as f:
                f.write(file.read())

            uploaded_file = genai.upload_file(temp_file_path, mime_type="video/mp4")
            st.success("video uploaded successfully")
            time.sleep(2)
            response = llm.complete([query, uploaded_file])
            return response.text
        elif file_extension in [".png", ".jpg", ".jpeg"]:
            uploaded_file = genai.upload_file(file, mime_type="image/jpeg")
            time.sleep(2)
            response = llm.complete([query, uploaded_file])
            return response.text
        else:
            uploaded_file = genai.upload_file(file, mime_type="application/octet-stream")
            time.sleep(2)
            response = llm.complete([query, uploaded_file])
            return response.text
    except GoogleAPIError as e:
        return f"Error processing file: {str(e)}"

