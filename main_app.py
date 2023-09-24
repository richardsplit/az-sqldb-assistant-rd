import pyodbc
import pandas as pd
from prompts.prompts import SYSTEM_MESSAGE
from azure_openai import get_completion_from_messages
import json
import re
import sql_db

# SQL Connection String
connection_string = "Driver={ODBC Driver 18 for SQL Server};Server=sql-smartresearch-sb.database.windows.net,1433;Database=SmartResearch;Uid=test;Pwd=3edc#EDC4rfv;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;Authentication=SqlPassword"

def create_connection():
    try:
        connection = pyodbc.connect(connection_string)
        print("Connection to the database successful!")
        return connection
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

def query_database(query, conn):
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    print(f"Data: {data}")  # Debugging
    print(f"Columns: {columns}")  # Debugging

    # Convert tuples to lists (if needed)
    # data = [list(row) for row in data]

    try:
        df = pd.DataFrame.from_records(data, columns=columns)
        print(f"DataFrame shape: {df.shape}")  # Debugging
        print("Successfully created DataFrame.")
        return df
    except Exception as e:
        print(f"Error while creating DataFrame: {e}")
        return None

# Create or connect to database
conn = create_connection()

# Note: You would need to write your own function to replace `get_schema_representation()`
# Schema Representation for finances table
schemas = schemas = sql_db.get_schema_representation  # Replace with your own function to get the schema
print("Schemas:", schemas)  # Debugging line to inspect schemas

formatted_system_message = SYSTEM_MESSAGE.format(schema=schemas)

user_message = "SELECT TOP 5 * FROM ACL_List_Companies_Jsons ORDER BY company_name ASC;"

response = get_completion_from_messages(formatted_system_message, user_message)

match = re.search(r'\{.*?\}', response, re.DOTALL)
valid_json_str = match.group(0) if match else None

if valid_json_str:
    response_json = json.loads(valid_json_str)
    query_value = response_json.get("query", "")
    print(f"Successfully parsed JSON! Query value is: {query_value}")
    
    sql_results = query_database(query_value, conn)
    print(f"SQL result: {sql_results}")
