from pydantic import BaseModel, Field

class AuthRequestModel(BaseModel):
    username: str = Field(...)
    password: str = Field(...)

class AuthResponse(BaseModel):
    key: str