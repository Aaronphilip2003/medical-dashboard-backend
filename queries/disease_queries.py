SEASONAL_DISEASE_OCCURRENCE = """
    SELECT toMonth(diagnosis_date) AS month, 
           disease_name, 
           COUNT(*) AS cases 
    FROM Patients 
    GROUP BY month, disease_name 
    ORDER BY month ASC, disease_name ASC
"""