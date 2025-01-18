from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import clickhouse_connect

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize ClickHouse Client
client = clickhouse_connect.get_client(
            host='localhost',
            port=8123,
            username='default',
            password='',
            database='default'
        )

@app.get("/trends/monthly-disease-trends")
async def get_monthly_disease_trends():
    query = "SELECT toStartOfMonth(diagnosis_date) AS month, disease_name, COUNT(*) AS cases FROM Patients GROUP BY month, disease_name ORDER BY month, disease_name"
    results = client.query(query)
    return [{"month": str(row[0]), "disease_name": row[1], "cases": row[2]} for row in results.result_rows]

@app.get("/heatmap/seasonal-disease-occurrence")
async def get_seasonal_disease_occurrence():
    query = "SELECT toMonth(diagnosis_date) AS month, disease_name, COUNT(*) AS cases FROM Patients GROUP BY month, disease_name ORDER BY month ASC, disease_name ASC"
    results = client.query(query)
    return [{"month": row[0], "disease_name": row[1], "cases": row[2]} for row in results.result_rows]

@app.get("/distribution/cases-by-city")
async def get_cases_by_city():
    query = "SELECT city, COUNT(*) AS cases FROM Patients GROUP BY city ORDER BY cases DESC"
    results = client.query(query)
    return [{"city": row[0], "cases": row[1]} for row in results.result_rows]

@app.get("/heatmap/city-severity-distribution")
async def get_city_severity_distribution():
    query = "SELECT city, severity, COUNT(*) AS cases FROM Patients GROUP BY city, severity ORDER BY city, severity"
    results = client.query(query)
    return [{"city": row[0], "severity": row[1], "cases": row[2]} for row in results.result_rows]

@app.get("/distribution/disease-distribution")
async def get_disease_distribution():
    query = "WITH (SELECT COUNT(*) FROM Patients) AS total_cases SELECT disease_name, COUNT(*) AS cases, (COUNT(*) * 100.0 / total_cases) AS percentage FROM Patients GROUP BY disease_name ORDER BY cases DESC"
    results = client.query(query)
    return [{"disease_name": row[0], "cases": row[1], "percentage": row[2]} for row in results.result_rows]

@app.get("/severity/disease-severity-distribution")
async def get_disease_severity_distribution():
    query = "SELECT disease_name, severity, COUNT(*) AS cases FROM Patients GROUP BY disease_name, severity ORDER BY disease_name, severity"
    results = client.query(query)
    return [{"disease_name": row[0], "severity": row[1], "cases": row[2]} for row in results.result_rows]

@app.get("/distribution/age-distribution")
async def get_age_distribution():
    query = "SELECT intDiv(age, 10) * 10 AS age_group, COUNT(*) AS cases FROM Patients GROUP BY age_group ORDER BY age_group"
    results = client.query(query)
    return [{"age_group": f"{row[0]}-{row[0] + 9}", "cases": row[1]} for row in results.result_rows]

@app.get("/boxplot/age-by-disease")
async def get_age_by_disease():
    query = "SELECT disease_name, quantiles(0.25, 0.5, 0.75)(age) AS age_quantiles, min(age) AS min_age, max(age) AS max_age FROM Patients GROUP BY disease_name"
    results = client.query(query)
    return [
        {
            "disease_name": row[0], 
            "age_quantiles": row[1], 
            "min_age": row[2], 
            "max_age": row[3]
        } for row in results.result_rows
    ]

@app.get("/distribution/severity-distribution")
async def get_severity_distribution():
    query = "SELECT severity, COUNT(*) AS cases FROM Patients GROUP BY severity ORDER BY cases DESC"
    results = client.query(query)
    return [{"severity": row[0], "cases": row[1]} for row in results.result_rows]

