"""
Script para insertar datos de prueba en la base de datos Biotica Nexus.
Ejecutar con: python test_data.py
"""
import sys
import random
from datetime import datetime, timedelta

# Agregar el directorio actual al path para importar módulos de app
sys.path.insert(0, '.')

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models, crud, schemas

# Crear tablas si no existen
models.Base.metadata.create_all(bind=engine)


def crear_datos_prueba():
    """
    Crea 3 sensores y 10 lecturas de prueba.
    """
    db = SessionLocal()
    
    try:
        # Limpiar tablas existentes (opcional, comentar si no se desea)
        print("Limpiando tablas existentes...")
        db.query(models.Lectura).delete()
        db.query(models.Sensor).delete()
        db.commit()
        
        # 1. Crear 3 sensores de prueba
        sensores_data = [
            {"tipo": "temperatura", "ubicacion": "Invernadero A", "estado": "activo"},
            {"tipo": "humedad", "ubicacion": "Invernadero B", "estado": "activo"},
            {"tipo": "presion", "ubicacion": "Laboratorio Central", "estado": "mantenimiento"},
        ]
        
        sensores = []
        print("Creando sensores de prueba...")
        for data in sensores_data:
            sensor = schemas.SensorCreate(**data)
            db_sensor = crud.create_sensor(db, sensor)
            sensores.append(db_sensor)
            print(f"  Sensor creado: ID={db_sensor.id}, {db_sensor.tipo} en {db_sensor.ubicacion}")
        
        # 2. Crear 10 lecturas de prueba distribuidas entre los sensores
        print("\nCreando lecturas de prueba...")
        
        # Valores típicos por tipo de sensor
        rangos = {
            "temperatura": (15.0, 35.0),
            "humedad": (40.0, 90.0),
            "presion": (980.0, 1020.0)
        }
        
        lecturas_creadas = 0
        for i in range(10):
            # Seleccionar sensor aleatorio
            sensor = random.choice(sensores)
            rango = rangos.get(sensor.tipo, (0.0, 100.0))
            
            # Generar valor aleatorio dentro del rango
            valor = round(random.uniform(rango[0], rango[1]), 2)
            
            # Crear lectura
            lectura_data = schemas.LecturaCreate(
                sensor_id=sensor.id,
                valor=valor
            )
            
            try:
                db_lectura = crud.create_lectura(db, lectura_data)
                lecturas_creadas += 1
                print(f"  Lectura {i+1}: Sensor {sensor.id} ({sensor.tipo}) = {valor}")
            except Exception as e:
                print(f"  Error creando lectura: {e}")
        
        # 3. Mostrar resumen
        print("\n" + "="*50)
        print("RESUMEN DE DATOS DE PRUEBA")
        print("="*50)
        
        # Contar sensores y lecturas
        total_sensores = db.query(models.Sensor).count()
        total_lecturas = db.query(models.Lectura).count()
        
        print(f"Sensores creados: {total_sensores}")
        print(f"Lecturas creadas: {total_lecturas}")
        
        # Mostrar estadísticas por sensor
        for sensor in sensores:
            lecturas_sensor = crud.get_lecturas_by_sensor(db, sensor.id)
            print(f"\nSensor {sensor.id} ({sensor.tipo}):")
            print(f"  Ubicación: {sensor.ubicacion}")
            print(f"  Estado: {sensor.estado}")
            print(f"  Lecturas: {len(lecturas_sensor)}")
            
            if lecturas_sensor:
                valores = [l.valor for l in lecturas_sensor]
                print(f"  Rango: {min(valores):.2f} - {max(valores):.2f}")
                print(f"  Promedio: {sum(valores)/len(valores):.2f}")
        
        print("\n¡Datos de prueba insertados exitosamente!")
        print("\nPara probar la API:")
        print("1. Ejecuta el servidor: uvicorn app.main:app --reload")
        print("2. Visita http://localhost:8000/docs para la documentación interactiva")
        
    except Exception as e:
        print(f"Error durante la creación de datos de prueba: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("Iniciando inserción de datos de prueba para Biotica Nexus...")
    crear_datos_prueba()