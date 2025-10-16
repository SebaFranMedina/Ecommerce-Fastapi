import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Carpeta donde está core.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ruta absoluta a productos.db
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'productos.db')}"

# Engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # necesario para SQLite
)

# Sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos
Base = declarative_base()

# Función para usar en Depends()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
