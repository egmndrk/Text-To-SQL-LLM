import os
from dotenv import load_dotenv
import sqlite3
import gradio as gr
import google.generativeai as genai
import pandas as pd

# Configure the Gemini API keys
load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_GEMINI_PRO_API_KEY'))
genai.configure(api_key=os.getenv('GOOGLE_GEMINI_FLASH_API_KEY'))

# Function to load Gemini Pro Model and provide SQL query
def get_gemini_pro_response(question, prompt):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content([prompt[0], question])
        if "Error" in response.text:
            return response.text.strip()
        else:
            return response.text.strip()
    except Exception as e:
        return f"Error generating SQL query: {e}"

# Function to load Gemini 1.5 Flash Model and provide natural language response
def get_gemini_flash_response(question, sql_query_response):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""Analyze the question and the response, and provide a concise, informative answer in a single sentence. 
        Also give your response as you are a search assistan. Question:{question}, Answer:{sql_query_response}"""
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating response: {e}"

# Function to retrieve Query from SQL database
def read_sql_query(sql, db):
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        conn.close()
        
        # Convert the rows to a string representation
        result_str = '\n'.join(str(row) for row in rows)
        return result_str
    except Exception as e:
        return f"Error executing SQL query: {e}"

# Function to save uploaded CSV file to SQLite database
def csv_to_sqlite(csv_file, db_name):
    try:
        df = pd.read_csv(csv_file)
        conn = sqlite3.connect(db_name)
        df.to_sql('UPLOADED_DATA', conn, if_exists='replace', index=False)
        conn.close()
        return df.columns.tolist()
    except Exception as e:
        return f"Error converting CSV to SQLite: {e}"

# Function to delete the SQLite database file
def delete_database(db_name):
    try:
        if os.path.exists(db_name):
            os.remove(db_name)
    except Exception as e:
        return f"Error deleting database: {e}"

# Function to handle the Gradio interface
def gradio_interface(question):
    db_name = 'EmployeesFromGithub.db'

    # Connect to the SQLite database and retrieve the schema
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table'")
    table_info = cursor.fetchall()
    conn.close()

    # Construct the database schema information
    schema_info = ""
    for table_name, create_table_sql in table_info:
        schema_info += f"Table Name: {table_name}\n"
        schema_info += f"Create Table SQL: {create_table_sql}\n\n"

    gemini_pro_prompt = [
        f"""
            You are an expert SQL translator specializing in converting English questions into precise SQL queries.
            The database schema is as follows:
            
            {schema_info}
            
            Task is to generate an SQL query based solely on the question provided, without using the word 'SQL' or backticks.
            Ensure your query retrieves relevant data based on the context of the question and the available tables/columns.
            
            If the question cannot be answered using the available data, please provide a detailed error message explaining why the query cannot be generated.
            Error message should include information about the issue, such as missing columns, invalid conditions, or unsupported operations.
            
            Examples:
            Question: "How many employees are there in the database?"
            Query: SELECT COUNT(*) FROM emp;
            
            Question: "List all employees who have a salary greater than 3000."
            Query: SELECT * FROM emp WHERE SAL > 3000;
            
            Question: "Show me the names of employees who work in the accounting department."
            Query: SELECT e.ENAME
                   FROM emp e
                   JOIN dept d ON e.DEPTNO = d.DEPTNO
                   WHERE d.DNAME = 'ACCOUNTING';
                   
            Question: "What is the average salary of employees in the research department?"
            Query: SELECT AVG(e.SAL) AS avg_salary
                   FROM emp e
                   JOIN dept d ON e.DEPTNO = d.DEPTNO
                   WHERE d.DNAME = 'RESEARCH';
                   
            Question: "List the names and job titles of all managers."
            Query: SELECT e.ENAME, e.JOB
                   FROM emp e
                   WHERE e.EMPNO IN (
                       SELECT DISTINCT MGR
                       FROM emp
                       WHERE MGR IS NOT NULL
                   );
                   
            Question: "Show me the employees who were hired in the last 6 months."
            Query: SELECT *
                   FROM emp
                   WHERE HIREDATE >= DATE('now', '-6 months');

            Question: "What is the average salary of employees in the database?"
            Query: SELECT AVG(SAL) AS avg_salary
                   FROM emp;
        """
    ]

    sql_query = get_gemini_pro_response(question, gemini_pro_prompt)

    if "Error" not in sql_query:
        data = read_sql_query(sql_query, db_name)
        if data:
            response = get_gemini_flash_response(question, data)
            return response
        else:
            return "No data found or an error occurred."
    else:
        return sql_query

# Define and launch the Gradio interface
iface = gr.Interface(
    fn=gradio_interface,
    inputs=[
        gr.Textbox(label="Enter your question", placeholder="What would you like to know?", lines=2)
    ],
    outputs=gr.Textbox(label="Response", lines=10),
    title="Gemini Pro + Gemini 1.5 Flash Text-to-SQL App",
    description="Ask a question and get an AI-generated natural language response based on the SQL query and result.",
    examples=[
        ["How many employees are there in the database?"],
        ["List all employees who have a salary greater than 3000."],
        ["Show me the names of employees who work in the accounting department."]
    ]
)

iface.launch()