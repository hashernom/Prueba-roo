"""
Esquemas Pydantic para validación y serialización de datos.
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


# Esquemas para Sensor
class SensorBase(BaseModel):
    """Esquema base para Sensor."""
    tipo: str = Field(..., min_length=1, max_length=50, example="temperatura")
    ubicacion: str = Field(..., min_length=1, max_length=200, example="Invernadero A")
    estado: Optional[str] = Field("activo", example="activo")


class SensorCreate(SensorBase):
    """Esquema para creación de Sensor."""
    pass


class SensorUpdate(BaseModel):
    """Esquema para actualización parcial de Sensor."""
    tipo: Optional[str] = Field(None, min_length=1, max_length=50)
    ubicacion: Optional[str] = Field(None, min_length=1, max_length=200)
    estado: Optional[str] = Field(None, min_length=1, max_length=20)


class Sensor(SensorBase):
    """Esquema para respuesta de Sensor (incluye ID)."""
    id: int
    lecturas_count: Optional[int] = 0

    class Config:
        from_attributes = True  # Permite la conversión desde ORM


# Esquemas para Lectura
class LecturaBase(BaseModel):
    """Esquema base para Lectura."""
    sensor_id: int = Field(..., gt=0, example=1)
    valor: float = Field(..., example=25.5)


class LecturaCreate(LecturaBase):
    """Esquema para creación de Lectura."""
    pass


class Lectura(LecturaBase):
    """Esquema para respuesta de Lectura (incluye ID y timestamp)."""
    id: int
    timestamp: datetime
    sensor: Optional[Sensor] = None

    class Config:
        from_attributes = True


# Esquemas para respuestas combinadas
class SensorWithLecturas(Sensor):
    """Sensor con lista de lecturas asociadas."""
    lecturas: list[Lectura] = []


# Esquema para estadísticas
class EstadisticasSensor(BaseModel):
    """Estadísticas de un sensor."""
    sensor_id: int
    total_lecturas: int
    valor_promedio: float
    valor_maximo: float
    valor_minimo: float
    ultima_lectura: Optional[datetime]