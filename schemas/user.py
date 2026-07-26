from datetime import datetime
from pydantic import BaseModel, Field, field_validator, ConfigDict, EmailStr

class UserCreate(BaseModel):
    username: str = Field(min_length=2, max_length=70, description="User name")
    email: EmailStr = Field(min_length=10, max_length=100, description="User email")
    password: str = Field(min_length=5, max_length=50, description="User password")

class UserLogin(BaseModel):
    username: str = Field(min_length=2, max_length=70, description="User name")
    password: str = Field(min_length=5, max_length=50, description="User password")

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    role: str
    created_at: datetime