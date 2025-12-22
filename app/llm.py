
from langchain_groq import ChatGroq
import os
# import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()
# google_api_key = os.getenv("GOOGLE_API_KEY")

groq_api_key = os.getenv("GROQ_API_KEY")



def get_llm():
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.2
    )


# def get_llm():
#     genai.configure(api_key=google_api_key)
#     model = genai.GenerativeModel("models/gemini-flash-latest")
#     return model








    























