from fastapi import APIRouter
from database.connection import client
from utils.query_processor import process_natural_query, process_patient_query

router = APIRouter()

@router.post("/query")
async def natural_language_query(body: dict):
    question = body["question"].lower()
    
    # Route to appropriate processor based on keywords
    patient_keywords = ["patient", "disease", "diagnosis", "medical history", 
                       "diagnosed", "sick", "treatment", "dengue", "covid",
                       "influenza", "typhoid", "pneumonia", "heat stroke"]
    
    is_patient_query = any(keyword in question.lower() for keyword in patient_keywords)
    
    if is_patient_query:
        result = process_patient_query(body["question"])
    else:
        result = process_natural_query(body["question"])
        
    if not result["success"]:
        return {"error": result["error"]}
        
    return {
        "success": True,
        "query": result["query"],
        "answer": result["answer"]
    }

# Tell me how many ICU beds were available in 2024 in Bangalore and tell me month by month
# Tell me about the different Diseases that Cedric Lin has had
# What disease did Richard Pfifer have in 2018? and what was his age then?
# When did Tommy Berndt have COVID-19?
# Give me all the patients with the name is like Cedric make sure they are unique and dates of diagnosis and give the disease they are diagnosed with and their age?
# Tell me how many Patients were there entirely in the year of 2024