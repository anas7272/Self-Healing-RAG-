import streamlit as st
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

@st.cache_resource
def get_llm():

    return ChatOpenAI(
        model="openai/gpt-4o",
        api_key=os.getenv("OPENAI_API_KEY"), #TODO: add your API key here
        base_url="https://models.github.ai/inference"
    )