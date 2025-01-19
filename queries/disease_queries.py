MONTHLY_DISEASE_TRENDS = """
    SELECT toStartOfMonth(diagnosis_date) AS month, 
           disease_name, 
           COUNT(*) AS cases 
    FROM Patients 
    GROUP BY month, disease_name 
    ORDER BY month, disease_name
"""

SEASONAL_DISEASE_OCCURRENCE = """
    SELECT toMonth(diagnosis_date) AS month, 
           disease_name, 
           COUNT(*) AS cases 
    FROM Patients 
    GROUP BY month, disease_name 
    ORDER BY month ASC, disease_name ASC
"""

DISEASE_DISTRIBUTION = """
    WITH (SELECT COUNT(*) FROM Patients) AS total_cases 
    SELECT disease_name, 
           COUNT(*) AS cases, 
           (COUNT(*) * 100.0 / total_cases) AS percentage 
    FROM Patients 
    GROUP BY disease_name 
    ORDER BY cases DESC
"""

DISEASE_SEVERITY_DISTRIBUTION = """
    SELECT disease_name, 
           severity, 
           COUNT(*) AS cases 
    FROM Patients 
    GROUP BY disease_name, severity 
    ORDER BY disease_name, severity
"""

AGE_BY_DISEASE = """
    SELECT disease_name, 
           quantiles(0.25, 0.5, 0.75)(age) AS age_quantiles, 
           min(age) AS min_age, 
           max(age) AS max_age 
    FROM Patients 
    GROUP BY disease_name
""" 