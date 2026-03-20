"""
Modelos de SQLAlchemy para la base de datos.
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Sensor(Base):
    """
    Modelo de tabla Sensores.
    Campos: id, tipo, ubicacion, estado
    """
    __tablename__ = "sensores"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String(50), nullable=False, index=True)
    ubicacion = Column(String(200), nullable=False)
    estado = Column(String(20), default="activo")  # activo, inactivo, mantenimiento

    # Relación uno a muchos con Lecturas
    lecturas = relationship("Lectura", back_populates="sensor", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Sensor(id={self.id}, tipo={self.tipo}, ubicacion={self.ubicacion})>"


class Lectura(Base):
    """
    Modelo de tabla Lecturas.
    Campos: id, sensor_id, valor, timestamp
    """
    __tablename__ = "lecturas"

    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(Integer, ForeignKey("sensores.id"), nullable=False, index=True)
    valor = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relación muchos a uno con Sensor
    sensor = relationship("Sensor", back_populates="lecturas")

    def __repr__(self):
        return f"<Lectura(id={self.id}, sensor_id={self.sensor_id}, valor={self.valor})>"