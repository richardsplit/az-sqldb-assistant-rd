# SQL Query Generator with GPT-4 and Streamlit

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

- **Natural Language to SQL**: Uses GPT-4 to transform user's natural language input into an SQL query.
- **Streamlit Interface**: Provides a simple and intuitive interface for users to input their queries.
- **SQLite Backend**: Uses SQLite as the database backend to store and query the financial data.
  
## Prerequisites

- Python 3.6 or above
- Virtual Environment (recommended)
- wkhtmltopdf installed on your machine for hosting the app

## Installation

1. **Clone the Repository**:
    ```bash
   git clone https://github.com/richardsplit/az-sqldb-assistant-rd.git
    ```

2. **Set up a Virtual Environment** (optional but recommended):
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
    ```

3. **Install the Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up Environment Variables**:
   
   If you're using any external services like Azure or APIs, make sure you have proper rights/permissions .
   - Apps is using SQL User with Access to DB as owner

   If you are going to host the project version app on streamlit .
    - Make sure to have the ip of the streamlit provisioned machine to your Azure SQL DB   

## Usage

1. **Run the Streamlit App**:
    ```bash
    streamlit run main_app.py
    ```

2. Open the displayed URL in your browser, usually `http://localhost:8501`.

3. Type in your natural language query into the input box, like "Show me all transactions and transaction timestamp for this month".

4. View the generated SQL Server specific query and the results from the database.

## How It Works

1. **SQLite Database**:

   The app uses SQLite to create a table representing a company's finances. It holds fields like revenue, expenses, and profit.

2. **Schema Retrieval**:

   Before generating a query, the system retrieves the schema of the table from SQL Server DB to understand its structure.

3. **GPT-4 Model**:

   The main functionality relies on the GPT-4 model to convert a user's natural language input into an SQL query. The app sends a formatted message containing the table's schema to GPT-4, which then returns an appropriate SQL query.

4. **Query Execution**:

   The app then executes the generated SQL query on the SQL Server database and retrieves the results.

## License

This project is open source, under the MIT license.
