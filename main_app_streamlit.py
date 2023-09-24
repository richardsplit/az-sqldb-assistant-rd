import streamlit as st
import re
import pyodbc
import pandas as pd
import sql_db
from prompts.prompts import SYSTEM_MESSAGE
from azure_openai import get_completion_from_messages
import json

# SQL Connection String
# connection_string = "Driver={ODBC Driver 18 for SQL Server};Server=sql-smartresearch-sb.database.windows.net,1433;Database=SmartResearch;Uid=test;Pwd=3edc#EDC4rfv;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;Authentication=SqlPassword"

# connection_string = (
#     "Driver={ODBC Driver 17 for SQL Server};"
#     "Server=sql-smartresearch-sb.database.windows.net,1433;"
#     "Database=SmartResearch;"
#     "Uid=test;"
#     "Pwd=3edc#EDC4rfv;"
#     "Encrypt=yes;"
#     "TrustServerCertificate=no;"
#     "Connection Timeout=30;"
#     "Authentication=SqlPassword"
# )

connection_string = "mssql+pymssql://test:3edc#EDC4rfv@sql-smartresearch-sb.database.windows.net:1433/SmartResearch"

# def create_connection():
#     try:
#         connection = pyodbc.connect(connection_string)
#         print("Connection to the database successfulss!")
#         return connection
#     except Exception as e:
#         st.write(f"Error connecting to the database: {e}")
#         return None

def init_connection():
    connection_string = (
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server=sql-smartresearch-sb.database.windows.net,1433;"
        "Database=SmartResearch;"
        "Uid=test;"
        "Pwd=3edc#EDC4rfv;"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
        "Authentication=SqlPassword"
    )
    return pyodbc.connect(connection_string)

# def query_database(query, conn):
#     cursor = conn.cursor()
#     cursor.execute(query)
#     data = cursor.fetchall()
#     st.write(data)
#     columns = [desc[0] for desc in cursor.description]
#     return pd.DataFrame(data, columns=columns)


def query_database(query, conn):
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    
    columns = [desc[0] for desc in cursor.description]
    df = pd.DataFrame.from_records(data, columns=columns)
    
    #st.write(df)  # Debugging , can be removed later
    
    return df


#conn = create_connection()
conn = init_connection()

# Debug: print connection type and value
#st.write(f"Connection: {conn}, Type: {type(conn)}")

if conn:

    schemas = sql_db.get_schema_representation 
    st.title("SQL Data Assistant")
    st.write("Enter your request to generate SQL and view results.")
    
    user_message = st.text_input("Enter your request:")
    
    if user_message:
        formatted_system_message = SYSTEM_MESSAGE.format(schema=schemas)
        
        response = get_completion_from_messages(formatted_system_message, user_message)
        match = re.search(r'\{.*?\}', response, re.DOTALL)
        
        valid_json_str = match.group(0) if match else None

        if valid_json_str:
            response_json = json.loads(valid_json_str)
            query_value = response_json.get("query", "")
            st.write("Generated SQL Query:")
            st.code(query_value, language="sql")
            #st.write(f"Debugging SQL: {query_value}")
            try:
                sql_results = query_database(query_value, conn)
                st.write("Query Results:")
                st.dataframe(sql_results)
                
            except Exception as e:
                st.write(f"An error occurred: {e}")

else:
    st.write("Failed to establish a database connection.")
