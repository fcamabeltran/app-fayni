from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from typing import Optional
from datetime import date
from app.database import get_db
from app.models.movimiento import Movimiento
from app.models.grupo import Grupo
from app.models.tipo import Tipo
from app.auth.jwt import get_current_user

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/resumen")
def resumen(
    fecha_desde: Optional[date] = None,
    fecha_hasta: Optional[date] = None,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    q = db.query(Movimiento)
    if fecha_desde:
        q = q.filter(Movimiento.fecha >= fecha_desde)
    if fecha_hasta:
        q = q.filter(Movimiento.fecha <= fecha_hasta)

    movs = q.all()
    total_ingreso  = sum(m.monto_ingreso for m in movs)
    total_egreso   = sum(m.monto_egreso  for m in movs)
    total_donacion = sum(m.monto_ingreso for m in movs if m.tipo.nombre == "DONACIÓN")

    # Saldo actual = último registro por ID (orden de ingreso, no por fecha)
    ultimo = db.query(Movimiento).order_by(Movimiento.id.desc()).first()

    return {
        "total_ingreso":    round(total_ingreso, 2),
        "total_egreso":     round(total_egreso, 2),
        "total_donacion":   round(total_donacion, 2),
        "saldo_actual":     round(ultimo.saldo, 2) if ultimo and ultimo.saldo else 0,
        "total_movimientos": len(movs),
    }


@router.get("/por-grupo")
def por_grupo(
    fecha_desde: Optional[date] = None,
    fecha_hasta: Optional[date] = None,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    q = db.query(
        Grupo.nombre,
        Grupo.color,
        Grupo.icono,
        func.sum(Movimiento.monto_ingreso).label("ingreso"),
        func.sum(Movimiento.monto_egreso).label("egreso"),
    ).join(Movimiento, Movimiento.grupo_id == Grupo.id)

    if fecha_desde:
        q = q.filter(Movimiento.fecha >= fecha_desde)
    if fecha_hasta:
        q = q.filter(Movimiento.fecha <= fecha_hasta)

    rows = q.group_by(Grupo.nombre, Grupo.color, Grupo.icono).all()
    return [
        {
            "grupo": r.nombre,
            "color": r.color,
            "icono": r.icono,
            "ingreso": round(r.ingreso or 0, 2),
            "egreso": round(r.egreso or 0, 2),
        }
        for r in rows
    ]


@router.get("/evolucion-mensual")
def evolucion_mensual(
    anio: Optional[int] = None,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    q = db.query(
        extract("year", Movimiento.fecha).label("anio"),
        extract("month", Movimiento.fecha).label("mes"),
        func.sum(Movimiento.monto_ingreso).label("ingreso"),
        func.sum(Movimiento.monto_egreso).label("egreso"),
    )
    if anio:
        q = q.filter(extract("year", Movimiento.fecha) == anio)

    rows = q.group_by("anio", "mes").order_by("anio", "mes").all()
    meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
    return [
        {
            "periodo": f"{meses[int(r.mes)-1]} {int(r.anio)}",
            "anio": int(r.anio),
            "mes": int(r.mes),
            "ingreso": round(r.ingreso or 0, 2),
            "egreso": round(r.egreso or 0, 2),
            "balance": round((r.ingreso or 0) - (r.egreso or 0), 2),
        }
        for r in rows
    ]


@router.get("/servicios-casa")
def servicios_casa(
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    """Gastos de luz y agua de la casa (ServicioCasa)"""
    rows = db.query(
        extract("year", Movimiento.fecha).label("anio"),
        extract("month", Movimiento.fecha).label("mes"),
        func.sum(Movimiento.monto_egreso).label("total"),
    ).join(Grupo, Movimiento.grupo_id == Grupo.id)\
     .filter(Grupo.nombre == "ServicioCasa")\
     .group_by("anio", "mes")\
     .order_by("anio", "mes").all()

    meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
    return [
        {
            "periodo": f"{meses[int(r.mes)-1]} {int(r.anio)}",
            "total": round(r.total or 0, 2),
        }
        for r in rows
    ]


@router.get("/top-egresos")
def top_egresos(
    limit: int = 5,
    fecha_desde: Optional[date] = None,
    fecha_hasta: Optional[date] = None,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    q = db.query(
        Grupo.nombre,
        func.sum(Movimiento.monto_egreso).label("total"),
    ).join(Movimiento, Movimiento.grupo_id == Grupo.id)
    if fecha_desde:
        q = q.filter(Movimiento.fecha >= fecha_desde)
    if fecha_hasta:
        q = q.filter(Movimiento.fecha <= fecha_hasta)

    rows = q.filter(Movimiento.monto_egreso > 0)\
            .group_by(Grupo.nombre)\
            .order_by(func.sum(Movimiento.monto_egreso).desc())\
            .limit(limit).all()
    return [{"grupo": r.nombre, "total": round(r.total or 0, 2)} for r in rows]
