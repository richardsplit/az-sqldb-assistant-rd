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
        if "search:" in user_input.lower():  # perform a search
            search_query = user_input.replace("search:", "").strip()
            results = search_client.search(search_query)
            st.write("Search Results:")
            for result in results:
                st.write(result)
        else:  
            response = get_completion_from_messages_usr(user_input)
            st.write("Response:")
            st.write(response)