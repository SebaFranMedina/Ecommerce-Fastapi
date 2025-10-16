from sqlalchemy import Column, Integer, String, TIMESTAMP, text
from .core import Base

class PapelHigienicoCocina(Base):
    __tablename__ = "papel_higienico_cocina"
    id = Column(Integer, primary_key=True)
    valor = Column(String, nullable=False)
    fecha_creacion = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

class BolsasEnvases(Base):
    __tablename__ = "bolsas_envases"
    id = Column(Integer, primary_key=True)
    valor = Column(String, nullable=False)
    fecha_creacion = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

class LimpiezaHogar(Base):
    __tablename__ = "limpieza_hogar"
    id = Column(Integer, primary_key=True)
    valor = Column(String, nullable=False)
    fecha_creacion = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

class LimpiezaQuimica(Base):
    __tablename__ = "limpieza_quimica"
    id = Column(Integer, primary_key=True)
    valor = Column(String, nullable=False)
    fecha_creacion = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

class Insecticidas(Base):
    __tablename__ = "insecticidas"
    id = Column(Integer, primary_key=True)
    valor = Column(String, nullable=False)
    fecha_creacion = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

class CuidadoPersonal(Base):
    __tablename__ = "cuidado_personal"
    id = Column(Integer, primary_key=True)
    valor = Column(String, nullable=False)
    fecha_creacion = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

class UtensiliosPlastico(Base):
    __tablename__ = "utensilios_plasticos"  # <- CORRECTO: coincide con tu DB
    id = Column(Integer, primary_key=True)
    valor = Column(String, nullable=False)
    fecha_creacion = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

class Otros(Base):
    __tablename__ = "otros"
    id = Column(Integer, primary_key=True)
    valor = Column(String, nullable=False)
    fecha_creacion = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
