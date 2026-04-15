from pydantic import BaseModel, EmailStr
from typing import Optional


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario_id: int
    nombre: str
    email: str
    rol: str


class UsuarioCreate(BaseModel):
    nombre: str
    email: EmailStr
    password: str
    rol: str = "familia"


class UsuarioOut(BaseModel):
    id: int
    nombre: str
    email: str
    rol: str
    activo: bool

    class Config:
        from_attributes = True
