from fastapi import APIRouter, HTTPException, Depends, Query
from schemas.prediction import NewsArticle, PredictionResponse, PredictionHistory, PredictionDetail, Prediction_Apdate
from dependencies.model import get_model
from services.prediction_service import PredictionService
from sqlalchemy.orm import Session
from dependencies.database import get_db
from typing import Optional
from dependencies.security import verify_api_key
from core.security import get_current_user, requires_role
from models.user import User

router = APIRouter(prefix="/predict", tags=["Prediction"])

@router.post("/", response_model=PredictionResponse)
def predict(article: NewsArticle, model = Depends(get_model), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        service = PredictionService(model, db=db)
        return service.predict(article, current_user)
        
    except Exception as e:
        print(e)

        raise HTTPException(
            status_code=500,
            detail="Prediction failed"
        )

@router.get("/history", response_model=list[PredictionHistory])
def get_history(limit: int = Query(default=20, ge=1, le=100), 
                offset : int = Query(default=0, ge=0),
                condition: Optional[str] = Query(default=None, description="Prediction type"),
                current_user: User = Depends(get_current_user),
                db: Session = Depends(get_db)
    ):
    
    service = PredictionService(model=None, db=db)
    return service.get_history(limit, offset, condition, current_user)

@router.get("/history/{id}", response_model=PredictionDetail)
def get_prediction(id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = PredictionService(model=None, db=db)
    prediction = service.get_prediction(id, current_user)
    
    return prediction

@router.delete("/delete/{id}")
def delete_prediction(id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = PredictionService(model=None, db=db)

    deleted = service.delete_prediction(id, current_user)


    return {"message": "Prediction deleted successfully"}

@router.patch("/update/{id}")
def update_prediction(id: int, update: Prediction_Apdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = PredictionService(None, db)

    updated = service.update_prediction(id, update, current_user)

    
    return {"message": "Note has been successfully updated."}

