import io
import pandas as pd
from fastapi import APIRouter, File, UploadFile, HTTPException
from app.services.ml_service import ml_service

router = APIRouter()

@router.post("/predict")
async def predict_file(file: UploadFile = File(...)):
    """
    Accepts a CSV file upload, runs data through the ML model,
    and returns traffic predictions and statistics.
    """
    if not file.filename.endswith(".csv"):
        return {
            "success": False,
            "error": "Invalid file type. Please upload a valid .csv file."
        }
        
    try:
        contents = await file.read()
        if not contents:
            return {
                "success": False,
                "error": "Uploaded file is empty."
            }
            
        df = pd.read_csv(io.BytesIO(contents))
        if df.empty:
            return {
                "success": False,
                "error": "CSV file contains no data rows."
            }
            
        results = ml_service.predict(df)
        return results
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to process CSV file: {str(e)}"
        }

@router.get("/model-info")
def get_model_info():
    """
    Returns metadata about the currently loaded NIDS machine learning model.
    """
    return {
        "model_type": "XGBoost Classifier",
        "features_used": len(ml_service.selected_features),
        "feature_names": ml_service.selected_features,
        "training_accuracy": 0.8980,
        "f1_score": 0.9007,
        "auc_score": 0.9860,
        "dataset": "UNSW-NB15"
    }

@router.get("/health")
def health_check():
    """
    Health check endpoint for the NIDS backend API.
    """
    return {
        "status": "healthy",
        "model_loaded": ml_service.binary_model is not None
    }
