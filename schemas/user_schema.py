from pydantic import BaseModel, Field

class UserSchema(BaseModel):
  email: str
  password: str = Field(min_length=8)