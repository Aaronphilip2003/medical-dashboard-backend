from fastapi import APIRouter, HTTPException
from database.connection import client
# from queries.resource_queries import *
from datetime import datetime


router = APIRouter()



@router.get("/trends/resource-usage")
async def get_resource_usage_trends(city: str, month: str):
    try:
        # Parse the month parameter (format: YYYY-MM)
        year, month_num = map(int, month.split('-'))
        
        query = f"""
            SELECT 
                toDate(date) as date,
                city,
                SUM(currently_used) AS used_resources,
                SUM(total_resources - currently_used) AS available_resources
            FROM Resources
            WHERE city = '{city}'
            AND toYear(date) = {year}
            AND toMonth(date) = {month_num}
            GROUP BY date, city
            ORDER BY date
        """
        
        results = client.query(query)
        
        data = [{
            "date": row[0].strftime("%Y-%m-%d"),
            "city": row[1],
            "used_resources": float(row[2]),
            "available_resources": float(row[3])
        } for row in results.result_rows]
        
        return data
    except Exception as e:
        print(f"Full error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))