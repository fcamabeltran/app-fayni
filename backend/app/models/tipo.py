from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Tipo(Base):
    __tablename__ = "tipos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, nullable=False)  # INGRESO, EGRESO, DONACIÓN

    movimientos = relationship("Movimiento", back_populates="tipo")
