from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.auth import LoginRequest, TokenResponse, UsuarioCreate, UsuarioOut
from app.auth.jwt import verify_password, hash_password, create_access_token, get_current_user, require_admin
from typing import List

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.email == data.email, Usuario.activo == True).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales incorrectas")

    token = create_access_token({"sub": user.email, "rol": user.rol})
    return TokenResponse(
        access_token=token,
        usuario_id=user.id,
        nombre=user.nombre,
        email=user.email,
        rol=user.rol,
    )


@router.get("/me", response_model=UsuarioOut)
def me(current_user=Depends(get_current_user)):
    return current_user


@router.post("/usuarios", response_model=UsuarioOut)
def crear_usuario(data: UsuarioCreate, db: Session = Depends(get_db), _=Depends(require_admin)):
    if db.query(Usuario).filter(Usuario.email == data.email).first():
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    user = Usuario(
        nombre=data.nombre,
        email=data.email,
        password_hash=hash_password(data.password),
        rol=data.rol,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/usuarios", response_model=List[UsuarioOut])
def listar_usuarios(db: Session = Depends(get_db), _=Depends(require_admin)):
    return db.query(Usuario).all()


@router.delete("/usuarios/{usuario_id}")
def desactivar_usuario(usuario_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    user = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    user.activo = False
    db.commit()
    return {"detail": "Usuario desactivado"}
