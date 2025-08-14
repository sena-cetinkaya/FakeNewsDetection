from sqlmodel import SQLModel, Field
from typing import Optional

# SQL Table
class News(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    news: str
    result: int

# Prediction Input
class PredictionInput(SQLModel):
    news: str

# Result
class PredictionOutput(SQLModel):
    result: str