from fastapi import APIRouter
from database.connection import client
from queries.disease_queries import *

router = APIRouter()

@router.get("/trends/monthly-disease-trends")
async def get_monthly_disease_trends():
    results = client.query(MONTHLY_DISEASE_TRENDS)
    return [{"month": str(row[0]), "disease_name": row[1], "cases": row[2]} for row in results.result_rows]

@router.get("/heatmap/seasonal-disease-occurrence")
async def get_seasonal_disease_occurrence():
    results = client.query(SEASONAL_DISEASE_OCCURRENCE)
    return [{"month": row[0], "disease_name": row[1], "cases": row[2]} for row in results.result_rows]

@router.get("/distribution/disease-distribution")
async def get_disease_distribution():
    results = client.query(DISEASE_DISTRIBUTION)
    return [{"disease_name": row[0], "cases": row[1], "percentage": row[2]} for row in results.result_rows]

@router.get("/severity/disease-severity-distribution")
async def get_disease_severity_distribution():
    results = client.query(DISEASE_SEVERITY_DISTRIBUTION)
    return [{"disease_name": row[0], "severity": row[1], "cases": row[2]} for row in results.result_rows]

@router.get("/boxplot/age-by-disease")
async def get_age_by_disease():
    results = client.query(AGE_BY_DISEASE)
    return [
        {
            "disease_name": row[0], 
            "age_quantiles": row[1], 
            "min_age": row[2], 
            "max_age": row[3]
        } for row in results.result_rows
    ] 