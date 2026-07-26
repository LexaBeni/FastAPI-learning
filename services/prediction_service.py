from functions.preprocessing import prepare_df
from models.prediction import Prediction
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from core.exception import PredictionNotFound
from roles import UserRole

ADMIN_ROLES = ("admin")

class PredictionService:

    def __init__(self, model, db):
        self.model = model
        self.db = db

    def predict(self, article, user):
        if self.model is None:
            raise ValueError("Model is not available")

        df = prepare_df(article.title, article.text)

        prediction = int(self.model.predict(df)[0])
        probability = float(self.model.predict_proba(df)[0, 1])

        label = "FAKE" if prediction == 1 else "REAL"

        confidence = probability if prediction == 1 else 1 - probability

        prediction_db = Prediction(

        title=article.title,

        text=article.text,

        prediction=label,

        probability=confidence,

        note=article.note,

        user_id = user.id
        )

        self.db.add(prediction_db)
        self.db.commit()
        self.db.refresh(prediction_db)
        
        return{
            "prediction" : label,
            "probability": round(confidence, 2)
        }
    def get_history(self, limit, offset, condition, user):

        stmt = select(Prediction)
        if condition:
            stmt = stmt.where(Prediction.prediction == condition)
        if user.role not in ADMIN_ROLES:
            stmt = stmt.where(Prediction.user_id == user.id)
        stmt = stmt.order_by(Prediction.created_at.desc()).limit(limit).offset(offset)

        result = self.db.execute(stmt)

        predictions = result.scalars().all()

        return predictions
    
    def get_prediction(self, prediction_id: int, user):
        stmt = select(Prediction).where(Prediction.id == prediction_id)
        if user.role not in ADMIN_ROLES:
            stmt = stmt.where(Prediction.user_id == user.id)
        result = self.db.execute(stmt)
        outcome = result.scalar_one_or_none()

        if outcome is None:
            raise PredictionNotFound(prediction_id)
        return outcome
    
    def delete_prediction(self, prediction_id: int, user):
        prediction = self.get_prediction(prediction_id, user)
        self.db.delete(prediction)

        self.db.commit()

    
    def update_prediction(self, prediction_id: int, update, user):
        prediction = self.get_prediction(prediction_id, user)
        
        prediction.note = update.note

        self.db.commit()
        self.db.refresh(prediction)

