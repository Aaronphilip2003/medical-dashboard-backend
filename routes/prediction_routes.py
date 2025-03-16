from fastapi import APIRouter, HTTPException
from utils.lstm_processor import LSTMPredictor
from typing import List
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class PredictionResponse(BaseModel):
    date: str
    predicted_cases: float
    confidence_lower: float
    confidence_upper: float

@router.get("/disease/{city}/{disease}", response_model=List[PredictionResponse])
async def get_disease_predictions(
    city: str, 
    disease: str, 
    days: int = 30
):
    """
    Get disease predictions for a specific city
    
    Parameters:
    - city: Name of the city
    - disease: Name of the disease
    - days: Number of days to predict (default: 30)
    
    Returns:
    - List of daily predictions with confidence intervals
    """
    try:
        predictor = LSTMPredictor()
        
        # Prepare and train model
        df = predictor.prepare_data(city, disease)
        predictor.train_model(df)
        
        # Make predictions with confidence intervals
        predictions = predictor.predict_future(df, days=days)
        
        # Format response
        return [
            PredictionResponse(
                date=date.strftime("%Y-%m-%d"),
                predicted_cases=float(pred),
                confidence_lower=float(lower),
                confidence_upper=float(upper)
            )
            for date, pred, lower, upper in predictions
        ]
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error making predictions: {str(e)}"
        ) 