CASES_BY_CITY = """
    SELECT city, 
           COUNT(*) AS cases 
    FROM Patients 
    GROUP BY city 
    ORDER BY cases DESC
"""