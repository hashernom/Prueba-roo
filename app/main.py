"""
Punto de entrada de la aplicación FastAPI para Biotica Nexus.
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import os

from app import crud, models, schemas
from app.database import engine, get_db

# Crear tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

# Inicializar aplicación FastAPI
app = FastAPI(
    title="Biotica Nexus API",
    description="API para gestión de sensores ambientales en campo",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")


# Endpoints para Sensores
@app.post("/sensores/", response_model=schemas.Sensor, status_code=status.HTTP_201_CREATED)
def crear_sensor(
    sensor: schemas.SensorCreate,
    db: Session = Depends(get_db)
):
    """
    Crea un nuevo sensor en el sistema.
    
    - **tipo**: Tipo de sensor (temperatura, humedad, etc.)
    - **ubicacion**: Ubicación física del sensor
    - **estado**: Estado del sensor (activo, inactivo, mantenimiento)
    """
    # Verificar si ya existe un sensor en esa ubicación
    db_sensor = crud.get_sensor_by_ubicacion(db, ubicacion=sensor.ubicacion)
    if db_sensor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un sensor en la ubicación {sensor.ubicacion}"
        )
    
    return crud.create_sensor(db=db, sensor=sensor)


@app.get("/sensores/", response_model=List[schemas.Sensor])
def listar_sensores(
    skip: int = 0,
    limit: int = 100,
    tipo: Optional[str] = None,
    estado: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Obtiene lista de sensores con filtros opcionales.
    
    - **skip**: Número de registros a saltar (paginación)
    - **limit**: Límite de registros a retornar
    - **tipo**: Filtrar por tipo de sensor
    - **estado**: Filtrar por estado del sensor
    """
    sensores = crud.get_sensores(
        db, skip=skip, limit=limit, tipo=tipo, estado=estado
    )
    return sensores


@app.get("/sensores/{sensor_id}", response_model=schemas.SensorWithLecturas)
def obtener_sensor(
    sensor_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtiene un sensor específico por su ID, incluyendo sus lecturas.
    """
    db_sensor = crud.get_sensor(db, sensor_id=sensor_id)
    if db_sensor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sensor con ID {sensor_id} no encontrado"
        )
    
    # Obtener lecturas del sensor
    lecturas = crud.get_lecturas_by_sensor(db, sensor_id=sensor_id, limit=50)
    
    # Convertir a esquema con lecturas
    sensor_dict = schemas.Sensor.from_orm(db_sensor).model_dump()
    sensor_dict["lecturas"] = [
        schemas.Lectura.from_orm(lectura).model_dump() for lectura in lecturas
    ]
    sensor_dict["lecturas_count"] = len(lecturas)
    
    return schemas.SensorWithLecturas(**sensor_dict)


@app.put("/sensores/{sensor_id}", response_model=schemas.Sensor)
def actualizar_sensor(
    sensor_id: int,
    sensor_update: schemas.SensorUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualiza un sensor existente.
    """
    db_sensor = crud.update_sensor(db, sensor_id=sensor_id, sensor_update=sensor_update)
    if db_sensor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sensor con ID {sensor_id} no encontrado"
        )
    return db_sensor


@app.delete("/sensores/{sensor_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_sensor(
    sensor_id: int,
    db: Session = Depends(get_db)
):
    """
    Elimina un sensor por su ID.
    """
    success = crud.delete_sensor(db, sensor_id=sensor_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sensor con ID {sensor_id} no encontrado"
        )
    return None


# Endpoints para Lecturas
@app.post("/lecturas/", response_model=schemas.Lectura, status_code=status.HTTP_201_CREATED)
def crear_lectura(
    lectura: schemas.LecturaCreate,
    db: Session = Depends(get_db)
):
    """
    Registra una nueva lectura de sensor.
    
    - **sensor_id**: ID del sensor que generó la lectura
    - **valor**: Valor numérico de la lectura
    """
    try:
        return crud.create_lectura(db=db, lectura=lectura)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@app.get("/lecturas/", response_model=List[schemas.Lectura])
def listar_lecturas(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Obtiene todas las lecturas registradas, ordenadas por fecha descendente.
    """
    return crud.get_lecturas(db, skip=skip, limit=limit)


@app.get("/sensores/{sensor_id}/lecturas/", response_model=List[schemas.Lectura])
def listar_lecturas_sensor(
    sensor_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Obtiene las lecturas de un sensor específico.
    """
    # Verificar que el sensor exista
    sensor = crud.get_sensor(db, sensor_id=sensor_id)
    if sensor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sensor con ID {sensor_id} no encontrado"
        )
    
    return crud.get_lecturas_by_sensor(db, sensor_id=sensor_id, skip=skip, limit=limit)


@app.get("/sensores/{sensor_id}/estadisticas/", response_model=schemas.EstadisticasSensor)
def obtener_estadisticas_sensor(
    sensor_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtiene estadísticas de las lecturas de un sensor.
    """
    # Verificar que el sensor exista
    sensor = crud.get_sensor(db, sensor_id=sensor_id)
    if sensor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sensor con ID {sensor_id} no encontrado"
        )
    
    estadisticas = crud.get_estadisticas_sensor(db, sensor_id=sensor_id)
    if estadisticas is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No hay lecturas para el sensor con ID {sensor_id}"
        )
    
    return estadisticas


# Endpoint de salud
@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    """
    Endpoint para verificar el estado del servicio.
    """
    return {
        "status": "healthy",
        "service": "Biotica Nexus API",
        "version": "1.0.0"
    }


# Endpoint para el dashboard
@app.get("/dashboard")
def dashboard():
    """
    Endpoint para servir el dashboard interactivo.
    """
    return FileResponse("static/index.html")


# Endpoint raíz
@app.get("/")
def root():
    """
    Endpoint raíz con información básica de la API.
    """
    return {
        "message": "Bienvenido a Biotica Nexus API",
        "docs": "/docs",
        "redoc": "/redoc",
        "dashboard": "/dashboard",
        "endpoints": {
            "sensores": "/sensores/",
            "lecturas": "/lecturas/",
            "health": "/health"
        }
    }