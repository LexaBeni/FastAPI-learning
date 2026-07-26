from fastapi import APIRouter, Query

router = APIRouter(tags=['Status'])

@router.get("/")
def root():
    return {"message": "Hello world!"}

@router.get("/status")
def get_status():
    return {
        "status": "online",
        "model": "XGBoost",
        "version": "1.0.0"
    }

@router.get("/articles")
def get_articles(limit: int = Query(default=10, ge=1, le=100), skip: int = Query(default=0, ge=0, le=100)):
    return{"message": f"Returning {limit} articles, skip {skip}."}
