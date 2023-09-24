import streamlit as st
import sql_db
from prompts.prompts import SYSTEM_MESSAGE

from azure_openai import get_completion_from_messages  # You should have a function like this from your existing logic.

def run_search_and_chat():
    st.title("Chat and Search Assistant")
    
    schemas = sql_db.get_schema_representation  # Fetching the schema representation
    formatted_system_message = SYSTEM_MESSAGE.format(schema=schemas)  # Generating the formatted system message
    
    user_input = st.text_input("Enter your message or search query:")
    if user_input:
        response = get_completion_from_messages(formatted_system_message, user_input)
        st.write("Response:")
        st.write(response)