from pydantic import BaseModel

class CreateUserRequest(BaseModel):
    Email: str
    Password: str

class Token(BaseModel):
    access_token: str
    token_type: str
