CASES_BY_CITY = """
    SELECT city, 
           COUNT(*) AS cases 
    FROM Patients 
    GROUP BY city 
    ORDER BY cases DESC
"""

CITY_SEVERITY_DISTRIBUTION = """
    SELECT city, 
           severity, 
           COUNT(*) AS cases 
    FROM Patients 
    GROUP BY city, severity 
    ORDER BY city, severity
"""

AGE_DISTRIBUTION = """
    SELECT intDiv(age, 10) * 10 AS age_group, 
           COUNT(*) AS cases 
    FROM Patients 
    GROUP BY age_group 
    ORDER BY age_group
"""

SEVERITY_DISTRIBUTION = """
    SELECT severity, 
           COUNT(*) AS cases 
    FROM Patients 
    GROUP BY severity 
    ORDER BY cases DESC
""" 