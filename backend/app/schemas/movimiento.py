from pydantic import BaseModel
from typing import Optional
from datetime import date


class MovimientoCreate(BaseModel):
    fecha: date
    descripcion: str
    monto_ingreso: float = 0.0
    monto_egreso: float = 0.0
    grupo_id: int
    tipo_id: int


class MovimientoUpdate(BaseModel):
    fecha: Optional[date] = None
    descripcion: Optional[str] = None
    monto_ingreso: Optional[float] = None
    monto_egreso: Optional[float] = None
    grupo_id: Optional[int] = None
    tipo_id: Optional[int] = None


class GrupoInfo(BaseModel):
    id: int
    nombre: str
    icono: Optional[str] = None
    color: Optional[str] = None

    class Config:
        from_attributes = True


class TipoInfo(BaseModel):
    id: int
    nombre: str

    class Config:
        from_attributes = True


class MovimientoOut(BaseModel):
    id: int
    fecha: date
    descripcion: str
    monto_ingreso: float
    monto_egreso: float
    saldo: Optional[float]
    grupo: GrupoInfo
    tipo: TipoInfo

    class Config:
        from_attributes = True


class GrupoCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    icono: Optional[str] = None
    color: Optional[str] = None


class GrupoOut(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    icono: Optional[str] = None
    color: Optional[str] = None

    class Config:
        from_attributes = True


class TipoCreate(BaseModel):
    nombre: str


class TipoOut(BaseModel):
    id: int
    nombre: str

    class Config:
        from_attributes = True
