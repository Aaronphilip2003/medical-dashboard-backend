import google.generativeai as genai
from database.connection import client
import json
import datetime
from typing import Dict, Any

# Configure Gemini once with hardcoded API key
API_KEY = "AIzaSyD9SqGrU4fP54MPwc5KIL7bdUWNLgnzp24"
genai.configure(api_key=API_KEY)
models = genai.list_models()
for model in models:
    print(model.name, model.supported_generation_methods)
model = genai.GenerativeModel('gemini-1.5-flash-latest')


def process_natural_query(question: str) -> Dict[str, Any]:
    """
    Process natural language questions and return SQL query results with formatted answer
    
    Args:
        question: Natural language question
        
    Returns:
        Dictionary containing success status, SQL query, and formatted results
    """
    prompt = """
    You are a SQL query generator for a ClickHouse database. Convert the following natural language question to a SQL query.
    
    Resources_Query Table Schema:
    - city (String): Name of the city
    - date (Date): Date of the record
    - total_resources (UInt16): Total number of resources
    - currently_used (UInt16): Number of resources currently in use
    - available_icu_beds (UInt8): Number of available ICU beds
    - total_staff (UInt8): Total number of staff

    Important SQL Rules:
    1. When using GROUP BY:
       - Every column in the SELECT clause must either be in the GROUP BY clause OR be aggregated (using AVG, SUM, COUNT, etc.)
       - You cannot select raw columns that aren't either grouped or aggregated
    2. Always include appropriate date filters when needed
    3. Use proper ClickHouse SQL syntax
    4. For time-based queries, consider using appropriate date functions
    5. Return only the SQL query, no explanations

    Question: {question}
    """
    
    try:
        # Generate SQL query using global model
        response = model.generate_content(prompt.format(question=question))
        sql_query = response.text.strip()
        
        # Clean the query
        sql_query = sql_query.replace('```sql', '').replace('```', '').strip()
        
        # Execute the query using global client
        result = client.query(sql_query)
        
        # Get data
        rows = result.result_rows
        headers = result.column_names
        
        # Format the answer based on result structure
        if len(headers) == 1 and len(rows) == 1:
            # Single value result
            answer = rows[0][0]
        elif len(headers) == 1:
            # Single column, multiple rows
            answer = [row[0] for row in rows]
        else:
            # Multiple columns and rows
            answer = []
            for row in rows:
                row_dict = {}
                for header, value in zip(headers, row):
                    if isinstance(value, (datetime.date, datetime.datetime)):
                        row_dict[header] = value.isoformat()
                    else:
                        row_dict[header] = value
                answer.append(row_dict)
        
        return {
            "success": True,
            "query": sql_query,
            "answer": answer
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def process_patient_query(question: str):
    """
    Process patient-related natural language questions and return SQL query results
    """
    prompt = """
    You are a SQL query generator for a ClickHouse database. Convert the following natural language question to a SQL query.
    
    Patients_Query Table Schema:
    - patient_id (String): Unique identifier for each patient
    - patient_name (String): Full name of the patient
    - disease_name (String): Name of the diagnosed disease
    - diagnosis_date (Date): Date of diagnosis
    - age (UInt8): Patient's age at time of diagnosis

    Important SQL Rules:
    1. When using GROUP BY:
       - Every column in the SELECT clause must either be in the GROUP BY clause OR be aggregated (using AVG, SUM, COUNT, etc.)
       - You cannot select raw columns that aren't either grouped or aggregated
    2. Always include appropriate date filters when needed
    3. Use proper ClickHouse SQL syntax
    4. For time-based queries, consider using appropriate date functions
    5. Return only the SQL query, no explanations

    Example queries:
    1. "Show me all diseases for patient P100058":
       SELECT disease_name, diagnosis_date, age 
       FROM Patients_Query 
       WHERE patient_id = 'P100058' 
       ORDER BY diagnosis_date;

    2. "How many times has Richard Pfifer had Dengue?":
       SELECT COUNT(*) as dengue_count 
       FROM Patients_Query 
       WHERE patient_name = 'Richard Pfifer' 
       AND disease_name = 'Dengue';

    Question: {question}
    """
    
    try:
        # Generate SQL query using global model
        response = model.generate_content(prompt.format(question=question))
        sql_query = response.text.strip()
        
        # Clean the query
        sql_query = sql_query.replace('```sql', '').replace('```', '').strip()
        
        # Execute the query using global client
        result = client.query(sql_query)
        
        # Get data
        rows = result.result_rows
        headers = result.column_names
        
        # Format the answer based on result structure
        if len(headers) == 1 and len(rows) == 1:
            # Single value result
            answer = rows[0][0]
        elif len(headers) == 1:
            # Single column, multiple rows
            answer = [row[0] for row in rows]
        else:
            # Multiple columns and rows
            answer = []
            for row in rows:
                row_dict = {}
                for header, value in zip(headers, row):
                    if isinstance(value, (datetime.date, datetime.datetime)):
                        row_dict[header] = value.isoformat()
                    else:
                        row_dict[header] = value
                answer.append(row_dict)
        
        return {
            "success": True,
            "query": sql_query,
            "answer": answer
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }