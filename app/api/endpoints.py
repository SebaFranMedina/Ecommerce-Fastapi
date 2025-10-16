from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.core import get_db
from app.models import (
    PapelHigienicoCocina, BolsasEnvases, LimpiezaHogar, LimpiezaQuimica,
    Insecticidas, CuidadoPersonal, UtensiliosPlastico, Otros
)
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# -----------------------------
# Landing page (index.html)
# -----------------------------
@router.get("/")
def landing(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# -----------------------------
# Panel de productos (/productos)
# -----------------------------
@router.get("/productos")
def productos(request: Request, db: Session = Depends(get_db)):
    data = {
        "papel_higienico_cocina": db.query(PapelHigienicoCocina).all(),
        "bolsas_envases": db.query(BolsasEnvases).all(),
        "limpieza_hogar": db.query(LimpiezaHogar).all(),
        "limpieza_quimica": db.query(LimpiezaQuimica).all(),
        "insecticidas": db.query(Insecticidas).all(),
        "cuidado_personal": db.query(CuidadoPersonal).all(),
        "utensilios_plasticos": db.query(UtensiliosPlastico).all(),
        "otros": db.query(Otros).all(),
    }
    return templates.TemplateResponse("productos.html", {"request": request, "data": data})

# -----------------------------
# Endpoint AJAX para cada tabla
# -----------------------------
@router.get("/tabla/{tabla_name}")
def get_tabla(tabla_name: str, db: Session = Depends(get_db)):
    tablas = {
        "papel_higienico_cocina": PapelHigienicoCocina,
        "bolsas_envases": BolsasEnvases,
        "limpieza_hogar": LimpiezaHogar,
        "limpieza_quimica": LimpiezaQuimica,
        "insecticidas": Insecticidas,
        "cuidado_personal": CuidadoPersonal,
        "utensilios_plasticos": UtensiliosPlastico,
        "otros": Otros,
    }
    Model = tablas.get(tabla_name)
    if not Model:
        return {"error": "Tabla no encontrada"}

    items = db.query(Model).all()
    return [{"id": i.id, "valor": i.valor} for i in items]

