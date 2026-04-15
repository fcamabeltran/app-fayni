from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Movimiento(Base):
    __tablename__ = "movimientos"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, nullable=False, index=True)
    descripcion = Column(Text, nullable=False)
    monto_ingreso = Column(Float, default=0.0)
    monto_egreso = Column(Float, default=0.0)
    saldo = Column(Float, nullable=True)

    grupo_id = Column(Integer, ForeignKey("grupos.id"), nullable=False)
    tipo_id = Column(Integer, ForeignKey("tipos.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    grupo = relationship("Grupo", back_populates="movimientos")
    tipo = relationship("Tipo", back_populates="movimientos")
    usuario = relationship("Usuario", back_populates="movimientos")
