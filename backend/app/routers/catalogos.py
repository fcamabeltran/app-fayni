from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.grupo import Grupo
from app.models.tipo import Tipo
from app.schemas.movimiento import GrupoCreate, GrupoOut, TipoCreate, TipoOut
from app.auth.jwt import get_current_user, require_admin

router = APIRouter(prefix="/api/catalogos", tags=["catalogos"])


@router.get("/grupos", response_model=List[GrupoOut])
def listar_grupos(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(Grupo).all()


@router.post("/grupos", response_model=GrupoOut, status_code=201)
def crear_grupo(data: GrupoCreate, db: Session = Depends(get_db), _=Depends(require_admin)):
    if db.query(Grupo).filter(Grupo.nombre == data.nombre).first():
        raise HTTPException(status_code=400, detail="Grupo ya existe")
    g = Grupo(**data.model_dump())
    db.add(g)
    db.commit()
    db.refresh(g)
    return g


@router.put("/grupos/{grupo_id}", response_model=GrupoOut)
def actualizar_grupo(grupo_id: int, data: GrupoCreate, db: Session = Depends(get_db), _=Depends(require_admin)):
    g = db.query(Grupo).filter(Grupo.id == grupo_id).first()
    if not g:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")
    for field, val in data.model_dump(exclude_unset=True).items():
        setattr(g, field, val)
    db.commit()
    db.refresh(g)
    return g


@router.delete("/grupos/{grupo_id}")
def eliminar_grupo(grupo_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    g = db.query(Grupo).filter(Grupo.id == grupo_id).first()
    if not g:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")
    db.delete(g)
    db.commit()
    return {"detail": "Eliminado"}


@router.get("/tipos", response_model=List[TipoOut])
def listar_tipos(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(Tipo).all()


@router.post("/tipos", response_model=TipoOut, status_code=201)
def crear_tipo(data: TipoCreate, db: Session = Depends(get_db), _=Depends(require_admin)):
    if db.query(Tipo).filter(Tipo.nombre == data.nombre).first():
        raise HTTPException(status_code=400, detail="Tipo ya existe")
    t = Tipo(**data.model_dump())
    db.add(t)
    db.commit()
    db.refresh(t)
    return t
