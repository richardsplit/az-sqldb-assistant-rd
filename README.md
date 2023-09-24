# SQL Query Assistant with GPT-4 + Streamlit

This project showcases the capabilities of combining OpenAI's GPT-4 with Streamlit to generate SQL queries based on natural language input. Users can enter a message describing the data they want to query from an SQLite database, and the application will display the generated SQL query as well as the results from the database.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Natural Language to SQL**: Uses GPT-4 to transform user's natural language input into an SQL Server specific query.
- **Streamlit Interface**: Provides a simple and intuitive interface for users to input their queries.
- **Azure SQL DB Backend**: Uses Azure SQL DB as the database backend to store and query the data. SQL User is used for authentication
- **Plugins/ Apss**: 
  
## Prerequisites

- Python 3.6 or above
- Virtual Environment (recommended)

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/richardsplit/az-sqldb-assistant-rd.git
    ```

2. **Set up a Virtual Environment** (optional but recommended):
    ```bash
    python -m venv .venv
    source .venv/bin/activate 
    .venv\Scripts\activate # For Windows 
    ```

3. **Install the Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up Environment Variables**:
   
   If you're using any external services like Azure or APIs, make sure you have the credentials set up as environment variables or stored safely.

## Usage

1. **Run the Streamlit App**:
    ```bash
    streamlit run main_app.py
    ```

2. Open the displayed URL in your browser, usually `http://localhost:8501`.

3. Type in your natural language query into the input box, like "Show me all transactions for this month".

4. View the generated SQL query and the results from the database.

## How It Works

1. **Azure SQL Database**:

   The app uses SQL Server to create a table representing a company's data. It holds fields like revenue, expenses, and profit.

2. **Schema Retrieval**:

   Before generating a query, the system retrieves the schema of the table from SQL Server to understand its structure. 
   Uses SQL User to Authenticate

3. **GPT-4 Model**:

   The main functionality relies on the GPT-4 model to convert a user's natural language input into an SQL query. The app sends a formatted message containing the table's schema to GPT-4, which then returns an appropriate SQL query specifically  SQL Server.

4. **Query Execution**:

   The app then executes the generated SQL query on the SQLite database and retrieves the results.

## License

This project is open source, under the MIT license.
