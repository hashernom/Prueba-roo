"""
Operaciones CRUD para Sensores y Lecturas.
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional
from app import models, schemas


# Operaciones CRUD para Sensor
def get_sensor(db: Session, sensor_id: int) -> Optional[models.Sensor]:
    """
    Obtiene un sensor por su ID.
    """
    return db.query(models.Sensor).filter(models.Sensor.id == sensor_id).first()


def get_sensor_by_ubicacion(db: Session, ubicacion: str) -> Optional[models.Sensor]:
    """
    Obtiene un sensor por su ubicación exacta.
    """
    return db.query(models.Sensor).filter(models.Sensor.ubicacion == ubicacion).first()


def get_sensores(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    tipo: Optional[str] = None,
    estado: Optional[str] = None
) -> List[models.Sensor]:
    """
    Obtiene lista de sensores con filtros opcionales.
    """
    query = db.query(models.Sensor)
    
    if tipo:
        query = query.filter(models.Sensor.tipo == tipo)
    if estado:
        query = query.filter(models.Sensor.estado == estado)
    
    return query.offset(skip).limit(limit).all()


def create_sensor(db: Session, sensor: schemas.SensorCreate) -> models.Sensor:
    """
    Crea un nuevo sensor en la base de datos.
    """
    db_sensor = models.Sensor(
        tipo=sensor.tipo,
        ubicacion=sensor.ubicacion,
        estado=sensor.estado
    )
    db.add(db_sensor)
    db.commit()
    db.refresh(db_sensor)
    return db_sensor


def update_sensor(
    db: Session, 
    sensor_id: int, 
    sensor_update: schemas.SensorUpdate
) -> Optional[models.Sensor]:
    """
    Actualiza un sensor existente.
    """
    db_sensor = get_sensor(db, sensor_id)
    if not db_sensor:
        return None
    
    update_data = sensor_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_sensor, field, value)
    
    db.commit()
    db.refresh(db_sensor)
    return db_sensor


def delete_sensor(db: Session, sensor_id: int) -> bool:
    """
    Elimina un sensor por su ID.
    Retorna True si se eliminó, False si no existía.
    """
    db_sensor = get_sensor(db, sensor_id)
    if not db_sensor:
        return False
    
    db.delete(db_sensor)
    db.commit()
    return True


# Operaciones CRUD para Lectura
def get_lectura(db: Session, lectura_id: int) -> Optional[models.Lectura]:
    """
    Obtiene una lectura por su ID.
    """
    return db.query(models.Lectura).filter(models.Lectura.id == lectura_id).first()


def get_lecturas_by_sensor(
    db: Session, 
    sensor_id: int,
    skip: int = 0, 
    limit: int = 100,
    orden_desc: bool = True
) -> List[models.Lectura]:
    """
    Obtiene lecturas de un sensor específico.
    """
    query = db.query(models.Lectura).filter(models.Lectura.sensor_id == sensor_id)
    
    if orden_desc:
        query = query.order_by(desc(models.Lectura.timestamp))
    else:
        query = query.order_by(models.Lectura.timestamp)
    
    return query.offset(skip).limit(limit).all()


def get_lecturas(
    db: Session, 
    skip: int = 0, 
    limit: int = 100
) -> List[models.Lectura]:
    """
    Obtiene todas las lecturas.
    """
    return db.query(models.Lectura).order_by(desc(models.Lectura.timestamp)).offset(skip).limit(limit).all()


def create_lectura(db: Session, lectura: schemas.LecturaCreate) -> models.Lectura:
    """
    Crea una nueva lectura en la base de datos.
    """
    # Verificar que el sensor exista
    sensor = get_sensor(db, lectura.sensor_id)
    if not sensor:
        raise ValueError(f"Sensor con ID {lectura.sensor_id} no existe")
    
    db_lectura = models.Lectura(
        sensor_id=lectura.sensor_id,
        valor=lectura.valor
    )
    db.add(db_lectura)
    db.commit()
    db.refresh(db_lectura)
    return db_lectura


def get_estadisticas_sensor(db: Session, sensor_id: int) -> Optional[dict]:
    """
    Calcula estadísticas de un sensor.
    """
    from sqlalchemy import func
    
    stats = db.query(
        func.count(models.Lectura.id).label("total_lecturas"),
        func.avg(models.Lectura.valor).label("valor_promedio"),
        func.max(models.Lectura.valor).label("valor_maximo"),
        func.min(models.Lectura.valor).label("valor_minimo"),
        func.max(models.Lectura.timestamp).label("ultima_lectura")
    ).filter(models.Lectura.sensor_id == sensor_id).first()
    
    if not stats or stats.total_lecturas == 0:
        return None
    
    return {
        "sensor_id": sensor_id,
        "total_lecturas": stats.total_lecturas,
        "valor_promedio": float(stats.valor_promedio) if stats.valor_promedio else 0.0,
        "valor_maximo": float(stats.valor_maximo) if stats.valor_maximo else 0.0,
        "valor_minimo": float(stats.valor_minimo) if stats.valor_minimo else 0.0,
        "ultima_lectura": stats.ultima_lectura
    }