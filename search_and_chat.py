import streamlit as st
import requests
import json
import openai  # Ensure you have OpenAI Python package installed
from summarizer import Summarizer

from azure_openai import get_completion_from_messages_usr

AZURE_SEARCH_URL = "https://srch-smartresearch-sb.search.windows.net"
INDEX_NAME = "aclcompanylistone"
API_VERSION = "2020-06-30"
AZURE_SEARCH_KEY = "LXGNAQfvGiDRifhWoMDh5xI5z9KvMtxpUFbJdFcrR0AzSeABub2D"

# Construct the URL for the search request
url = f"{AZURE_SEARCH_URL}/indexes/{INDEX_NAME}/docs/search?api-version={API_VERSION}"

headers = {
    'Content-Type': 'application/json',
    'api-key': AZURE_SEARCH_KEY,
}

# Initialize OpenAI API with your API Key
openai.api_key = '8b1955bb34a2499d99c48f024fac82f8'

def fetch_company_names():
    url = f"{AZURE_SEARCH_URL}/indexes/{INDEX_NAME}/docs?api-version={API_VERSION}&$select=company_name"
    headers = {'api-key': AZURE_SEARCH_KEY}
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Check if request was successful
    
    results = response.json().get('value', [])
    return [result['company_name'] for result in results]

# Fetch company names at the startup and store in a list
company_names_list = fetch_company_names()


def generate_summary_with_bert(result):
    model = Summarizer()
    
    info_string = f"Company Name: {result.get('company_name', 'Unknown Company')}, " \
                  f"Marketing Class Description: {result.get('marketingClass_Description', 'N/A')}, " \
                  f"Net Income: {result.get('netIncome', 'N/A')}, " \
                  f"Market Cap: {result.get('marketCap', 'N/A')}."
    
    summary = model(info_string)
    return summary

def run_search_and_chat():
  
  st.title("Chat and Search Assistant")
    
  user_input = st.text_input("Start typing your message or search query:")
  if user_input:
    suggestions = [name for name in company_names_list if user_input.lower() in name.lower()]
    selected_suggestion = st.selectbox('Did you mean:', suggestions, key='selectbox')
    if st.button('Search'):
        user_input = selected_suggestion
    
    if user_input:
        try:
            # Assume every input as a search query initially
            payload = {
                "search": user_input,
                "count": True,
            }
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()  # Check if request was successful

            results_list = response.json().get('value', [])
            
        except requests.RequestException as e:
            st.error(f"An error occurred: {e}")
            return
        
        if results_list:  # If there are results from Azure Cognitive Search
            st.write("Search Results:")
            for result in results_list:
                summary = generate_summary_with_bert(result)
                st.write(f"ID: {result['id']}")
                st.write(f"Company Name: {result['company_name']}")
                st.write(f"Marketing Class Description: {result['marketingClass_Description']}")
                st.write(f"Net Income: {result['netIncome']}")
                st.write(f"Market Cap: {result['marketCap']}")
                st.write("---")
                
        else:  # If no results from Azure Cognitive Search, interact with OpenAI
            response = get_completion_from_messages_usr(user_input)
            st.write("Response:")
            st.write(response)

