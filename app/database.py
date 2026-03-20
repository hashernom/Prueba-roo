"""
Configuración de la base de datos SQLite usando SQLAlchemy.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de conexión a SQLite (archivo en el directorio raíz)
SQLALCHEMY_DATABASE_URL = "sqlite:///./biotica_nexus.db"

# Motor de la base de datos
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}  # Necesario para SQLite
)

# Sesión local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()

# Dependencia para obtener sesión de base de datos
def get_db():
    """
    Provee una sesión de base de datos para cada request.
    Cierra la sesión automáticamente al final.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()