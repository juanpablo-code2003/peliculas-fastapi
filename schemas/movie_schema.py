import time

from pydantic import BaseModel, Field

class MovieSchema(BaseModel):
  title: str = Field(min_length=2, max_length=50)
  overview: str = Field(min_length=2, max_length=50)
  year: int = Field(gt=1900, lt=time.localtime().tm_year)
  rating: float = Field(gt=0, le=10)
  category: str = Field(min_length=5, max_length=12)