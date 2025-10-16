from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.core import Base, engine
from app.api import endpoints

app = FastAPI(title="Proyecto de Ejemplo")

# Crear todas las tablas
Base.metadata.create_all(bind=engine)

# Carpeta estática y templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Rutas
app.include_router(endpoints.router)


#  uvicorn app.main:app --reload

