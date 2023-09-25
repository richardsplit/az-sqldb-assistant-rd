import streamlit as st
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure_openai import get_completion_from_messages_usr

AZURE_SEARCH_URL = "https://srch-smartresearch-sb.search.windows.net"
AZURE_SEARCH_INDEX = "aclcompanylistone"
AZURE_SEARCH_KEY = "LXGNAQfvGiDRifhWoMDh5xI5z9KvMtxpUFbJdFcrR0AzSeABub2D"

search_client = SearchClient(AZURE_SEARCH_URL, AZURE_SEARCH_INDEX, AzureKeyCredential(AZURE_SEARCH_KEY))

def run_search_and_chat():
    st.title("Chat and Search Assistant")
    user_input = st.text_input("Enter your message or search query:")
    
    if user_input:
        try:
            # Assume every input as a search query initially
            results = search_client.search(user_input)
            results_list = [result for result in results]  # Convert search results to a list
            
        except Exception as e:
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