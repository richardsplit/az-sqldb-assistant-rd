#from dotenv import load_dotenv
import os
import openai
#load_dotenv()
os.environ["OPENAI_API_TYPE"] = "azure" 
os.environ["OPENAI_API_KEY"] = "2510fbfb504c4091acb34d1a8adfdee0" #Can be found in your Azure Open AI Resource under Keys 
os.environ["OPENAI_API_BASE"] = "https://openai-mpi-smartresearch-sbx.openai.azure.com/" #Can be found in your Azure Open AI Resource under Endpoint.
os.environ["OPENAI_API_VERSION"] = "2023-05-15"
os.environ["OPENAI_DEPLOYMENT_NAME"] = "chatgpt35model" #You can create a deployment of a Model within the Azure Open Ai studio - reference the name here. 
os.environ["OPENAI_MODEL_NAME"] ="gpt-35-turbo"   #"gpt-35-turbo" #This is selected when creating the deployment of the Model 
os.environ["DATABASE_CONNECTION_STRING"] = "mssql+pymssql://test:3edc#EDC4rfv@sql-smartresearch-sb.database.windows.net:1433/SmartResearch" # Uses the following format "mssql+pyodbc://username:password@hostnameurl:port/databasename?driver=ODBC+Driver+18+for+SQL+Server"

openai.api_type = "azure"
openai.api_base = os.getenv('OPENAI_API_BASE')  #"https://openai-mpi-smartresearch-sbx.openai.azure.com/"
#openai.api_base = "https://azureopenai-vastmindz.openai.azure.com/"
openai.api_version = "2023-03-15-preview"
openai.api_key = os.getenv("OPENAI_API_KEY")


def get_completion_from_messages(system_message, user_message, model="gpt-4", temperature=0, max_tokens=500) -> str:

    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': f"{user_message}"}
    ]
    
    response = openai.ChatCompletion.create(
        engine=model,
        messages=messages,
        temperature=temperature, 
        max_tokens=max_tokens, 
    )
    
    return response.choices[0].message["content"]

if __name__ == "__main__":
    system_message = "You are a helpful assistant"
    user_message = "Hello, how are you?"
    print(get_completion_from_messages(system_message, user_message))