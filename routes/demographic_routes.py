from fastapi import APIRouter
from database.connection import client
from queries.demographic_queries import *

router = APIRouter()

@router.get("/distribution/cases-by-city") # Used
async def get_cases_by_city():
    results = client.query(CASES_BY_CITY)
    return [{"city": row[0], "cases": row[1]} for row in results.result_rows]

@router.get("/distribution/cases-by-age")  # New
async def get_cases_by_age():
    results = client.query("""
        SELECT age, COUNT(*) AS cases
        FROM Patients
        GROUP BY age
        ORDER BY age
    """)
    return [{"age": row[0], "cases": row[1]} for row in results.result_rows]

@router.get("/distribution/severity-count")  # New
async def get_severity_distribution():
    results = client.query("""
        SELECT severity, COUNT(*) AS cases
        FROM Patients
        GROUP BY severity
        ORDER BY cases DESC
    """)
    return [{"severity": row[0], "cases": row[1]} for row in results.result_rows]
