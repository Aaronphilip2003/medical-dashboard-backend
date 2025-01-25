from fastapi import APIRouter,HTTPException
from database.connection import client
from queries.disease_queries import *


router = APIRouter()

@router.get("/trends/monthly-disease-trends")
async def get_monthly_disease_trends(month: str):
    try:
        year, month_num = map(int, month.split('-'))
        # Use f-string for parameter substitution in ClickHouse
        query = f"""
            SELECT 
                disease_name,
                COUNT(*) AS cases 
            FROM Patients 
            WHERE toYear(diagnosis_date) = {year}
            AND toMonth(diagnosis_date) = {month_num}
            GROUP BY disease_name 
            ORDER BY disease_name
        """
        results = client.query(query)
        return [{
            "disease_name": row[0],
            "cases": row[1]
        } for row in results.result_rows]
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/heatmap/seasonal-disease-occurrence") #Used
async def get_seasonal_disease_occurrence():
    results = client.query(SEASONAL_DISEASE_OCCURRENCE)
    return [{"month": row[0], "disease_name": row[1], "cases": row[2]} for row in results.result_rows]
