from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import datetime


class NewsArticle(BaseModel):
    title: str = Field(
        min_length=10,
        max_length=1000,
        description="Enter the title of the article"
    )

    text: str = Field(
        min_length=20,
        max_length=5000,
        description="Enter the full text of the article"
    )

    note: str | None = Field(
        default=None,
        max_length=150,
        description="Optional note to save with the prediction"
    )

    @field_validator("title", "text")
    @classmethod
    def strip_whitespace(cls, value: str):
        return value.strip()
    
    model_config = ConfigDict(
    json_schema_extra={
        "example": {
            "title": "NASA launches new Mars rover",
            "text": "NASA successfully launched a new rover to explore ancient riverbeds on Mars.",
            "note": "Example request"
        }
    }
)


class PredictionResponse(BaseModel):
    prediction: str
    probability: float

class PredictionHistory(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    prediction: str
    probability: float
    created_at: datetime
    note: str | None = None

class PredictionDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    text: str
    prediction: str
    probability: float
    created_at: datetime
    note: str | None = None

class Prediction_Apdate(BaseModel):
    note: str | None = Field(default=None, max_length=150)

