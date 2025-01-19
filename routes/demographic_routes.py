from fastapi import APIRouter
from database.connection import client
from queries.demographic_queries import *

router = APIRouter()

@router.get("/distribution/cases-by-city")
async def get_cases_by_city():
    results = client.query(CASES_BY_CITY)
    return [{"city": row[0], "cases": row[1]} for row in results.result_rows]

@router.get("/heatmap/city-severity-distribution")
async def get_city_severity_distribution():
    results = client.query(CITY_SEVERITY_DISTRIBUTION)
    return [{"city": row[0], "severity": row[1], "cases": row[2]} for row in results.result_rows]

@router.get("/distribution/age-distribution")
async def get_age_distribution():
    results = client.query(AGE_DISTRIBUTION)
    return [{"age_group": f"{row[0]}-{row[0] + 9}", "cases": row[1]} for row in results.result_rows]

@router.get("/distribution/severity-distribution")
async def get_severity_distribution():
    results = client.query(SEVERITY_DISTRIBUTION)
    return [{"severity": row[0], "cases": row[1]} for row in results.result_rows] 