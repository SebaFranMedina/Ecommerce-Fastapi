from pydantic import BaseModel

class ProductoSchema(BaseModel):
    id: int
    valor: str
    fecha_creacion: str

    model_config = {"from_attributes": True}
