import pyodbc
import pandas as pd

# SQL Alchemy MSSQL Conn String
connection_string = "Driver={ODBC Driver 18 for SQL Server};Server=sql-smartresearch-sb.database.windows.net,1433;Database=SmartResearch;Uid=test;Pwd=3edc#EDC4rfv;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;Authentication=SqlPassword"

def create_connection():
    """ Create a connection to the SQL Server database """
    try:
        connection = pyodbc.connect(connection_string)
        print("Connection to the database successful!")
        return connection
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

def query_database(connection, query):
    """ Run SQL query and return results in a dataframe """
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        return pd.DataFrame(data, columns=columns)
    except Exception as e:
        print(f"Error querying the database: {e}")
        return None

def get_schema_representation():
    """ Get the database schema in a JSON-like format """
    conn = create_connection()
    cursor = conn.cursor()
    
    # Query to get all table names
    cursor.execute("SELECT table_name = t.name, schema_name = s.name FROM sys.tables t INNER JOIN sys.schemas s ON t.schema_id = s.schema_id;")
    tables = cursor.fetchall()
    
    db_schema = {}
    
    for table in tables:
        table_name = table.table_name
        schema_name = table.schema_name
        
        # Query to get column details for each table
        cursor.execute(f"SELECT column_name = c.name, data_type = t.name FROM sys.columns c INNER JOIN sys.types t ON c.user_type_id = t.user_type_id WHERE c.object_id = OBJECT_ID('{schema_name}.{table_name}');")
        columns = cursor.fetchall()
        
        column_details = {}
        for column in columns:
            column_name = column.column_name
            column_type = column.data_type
            column_details[column_name] = column_type
        
        db_schema[f"{schema_name}.{table_name}"] = column_details
    
    conn.close()
    return db_schema

if __name__ == "__main__":
    connection = create_connection()

    if connection is not None:
        # Querying the database
        query = "SELECT top (3) * FROM [smartresearchR].[ACL_List_Companies_Jsons]"
        df = query_database(connection, query)
        if df is not None:
            print(df)

        # Get the database schema
        schema = get_schema_representation()
        print("Schemas:", schema)

        # Close the database connection
        connection.close()
