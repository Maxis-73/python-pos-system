from pydantic import BaseModel

class User(BaseModel):
    id: str
    email: str
    full_name: str
    is_active: bool
    created_at: str
    updated_at: str

class RegisterRequest(BaseModel):
    email: str
    full_name: str
    password: str
    confirm_password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    message: str