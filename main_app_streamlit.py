import streamlit as st
import re
import pyodbc
import pandas as pd
import sql_db
from prompts.prompts import SYSTEM_MESSAGE
from azure_openai import get_completion_from_messages
import json
import io , os
import base64

# SQL Connection String
# connection_string = "Driver={ODBC Driver 18 for SQL Server};Server=sql-smartresearch-sb.database.windows.net,1433;Database=SmartResearch;Uid=test;Pwd=3edc#EDC4rfv;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;Authentication=SqlPassword"

# ODBC Driver 17 Connection String 
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

def query_database(query, conn):
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    
    columns = [desc[0] for desc in cursor.description]
    df = pd.DataFrame.from_records(data, columns=columns)
    
    #st.write(df)  # Debugging , can be removed later
    
    return df


#conn = create_connection() # For SQL Alchemy or other ..

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
                
                # available file formats
                file_formats = ["CSV", "Excel", "PDF"]
                
                
                selected_format = st.selectbox("Select a file format to download:", file_formats)
                
                # download button by format
                if selected_format == "CSV":
                        csv = sql_results.to_csv(index=False)
                        b64_csv = base64.b64encode(csv.encode()).decode()  # encode to base64
                        st.download_button(
                            label='Download CSV File',
                            data=b64_csv,
                            file_name='csv_query_results.csv',
                            mime='text/csv'
                        )
                    
                elif selected_format == "Excel":
                    towrite = io.BytesIO()
                    sql_results.to_excel(towrite, index=False, engine='openpyxl')
                    towrite.seek(0)
                    st.download_button(
                        label='Download Excel File',
                        data=towrite,
                        file_name='excel_query_results.xlsx',
                        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                    )
                    
                elif selected_format == "PDF":
                    pdf_file_path = "query_results.pdf"
                    sql_results.to_html('temp.html')
                    os.system(f'wkhtmltopdf temp.html {pdf_file_path}')
                    os.remove('temp.html')
                    with open(pdf_file_path, "rb") as f:
                        st.download_button(
                            label='Download PDF File',
                            data=f,
                            file_name='pdf_query_results.pdf',
                            mime='application/pdf'
                        )
                    os.remove(pdf_file_path)
                
            except Exception as e:
                st.write(f"An error occurred: {e}")

else:
    st.write("Failed to establish a database connection.")
