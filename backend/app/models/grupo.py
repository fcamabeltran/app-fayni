from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.database import Base


class Grupo(Base):
    __tablename__ = "grupos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, nullable=False)
    descripcion = Column(Text, nullable=True)
    icono = Column(String(50), nullable=True)   # emoji o nombre de icono
    color = Column(String(20), nullable=True)   # color hex para dashboard

    movimientos = relationship("Movimiento", back_populates="grupo")
