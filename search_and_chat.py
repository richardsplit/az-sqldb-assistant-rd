import streamlit as st
import requests
import json
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



def run_search_and_chat():
    st.title("Chat and Search Assistant")
    user_input = st.text_input("Enter your message or search query:")
    
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
        
        st.write("results_list:")
        st.write(results_list)
        if results_list:  # If there are results from Azure Cognitive Search
            st.write("Search Results:")
            for result in results_list:
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

