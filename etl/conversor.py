import sys
import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import logging
import re

# 🔹 Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 🔹 Agregar la carpeta raíz al path para importar app
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

try:
    from app.models import (
        Base,
        PapelHigienicoCocina,
        BolsasEnvases,
        LimpiezaHogar,
        LimpiezaQuimica,
        Insecticidas,
        CuidadoPersonal,
        UtensiliosPlastico,
        Otros
    )
except ImportError as e:
    logger.error(f"Error importando modelos: {e}")
    sys.exit(1)

def extraer_precio(nombre):
    """
    Extrae el precio del formato: 'PRODUCTO ($precio)'
    """
    try:
        # Buscar patrones de precio: ($número) o ($número.decimal)
        match = re.search(r'\(\$([\d,.]+)\)', str(nombre))
        if match:
            precio_str = match.group(1).replace(',', '')  # Remover comas
            return float(precio_str)
        return 0.0
    except:
        return 0.0

def limpiar_nombre(nombre):
    """
    Remueve el precio del nombre para tener solo el nombre del producto
    """
    try:
        # Remover la parte del precio: ($número)
        nombre_limpio = re.sub(r'\(\$[\d,.]*\)', '', str(nombre)).strip()
        return nombre_limpio
    except:
        return str(nombre)

def clasificar_producto(nombre):
    """
    Clasificación EXACTA basada en la distribución real de la base de datos
    """
    if not nombre or pd.isna(nombre):
        return "otros"
    
    nombre_lower = str(nombre).lower().strip()
    
    # EXCLUIR PRODUCTOS QUE NO DEBEN SER INSERTADOS
    if any(x in nombre_lower for x in ["envio lejano", "envio medio", "envio cercano", "ajuste"]):
        return "excluir"
    
    # CLASIFICACIÓN EXACTA BASADA EN LOS PRODUCTOS REALES
    # Orden de prioridad basado en especificidad
    
    # 1. PRODUCTOS QUE DEBEN IR EN "OTROS" (corrección)
    if any(x in nombre_lower for x in [
        "film cocina", "r. aluminio", "r. pap. manteca", "rollo papel manteca",
        "aluminio profesional", "aluminio super", "film stretch", "rollo film polietileno",
        "marcador negro indeleble", "cubiertos multiusos", "separadores freezer",
        "espuma limpia hornos", "espuma limpia parrilla"
    ]):
        return "otros"
    
    if any(x in nombre_lower for x in ["t. humeda", "toalla humeda"]):
        return "cuidado_personal"
    
    # 2. CUIDADO PERSONAL (muy específico)
    if any(x in nombre_lower for x in [
        "colgate", "desodorante", "toallas femen", "protector diario", "algodón", 
        "femenino", "lovely", "deluxe", "mac gregor", "hisopo", "discos desmaquillantes",
        "tanga", "anatómico", "nocturnas", "afeitar", "antitranspirante", "unisex",
        "doncella", "q-soft", "premium", "pre-cortado"
    ]):
        return "cuidado_personal"
    
    # 3. INSECTICIDAS (muy específico)
    if any(x in nombre_lower for x in [
        "insecticida", "repelente", "espiral", "moscas", "mosquitos", 
        "cucarachas", "hormigas", "pulgas", "garrapatas", "polillas", 
        "pirisa", "mata"
    ]):
        return "insecticidas"
    
    # 4. BOLSAS Y ENVASES
    if any(x in nombre_lower for x in [
        "bolsa", "bolsas", "camiseta", "zip", "rollo", "arranque", 
        "freezer", "horno", "lavarropa", "residuos", "escombros",
        "empaque", "envase", "negro", "verde", "roja", "blanca",
        "pack", "contenedor", "combo"
    ]):
        return "bolsas_envases"
    
    # 5. LIMPIEZA QUÍMICA
    if any(x in nombre_lower for x in [
        "deterg", "alcohol", "suavizante", "jabon liq", "limpiador", 
        "cloro", "lavandina", "desinfectante", "desengrasante", 
        "lavavajillas", "lustramueble", "silicona", "lubricante", 
        "aromatizante", "espuma", "limpiatapizados", "smell fresh", 
        "val", "s.f.", "escudo", "piso", "ambient", "textil",
        "concentrado", "arranca motores", "apresto", "danubio",
        "espuma limpia hornos", "espuma limpia parrilla"
    ]):
        return "limpieza_quimica"
    
    # 6. LIMPIEZA HOGAR
    if any(x in nombre_lower for x in [
        "escoba", "esponja", "microfibra", "paño", "franela", "rejilla", 
        "cepillo", "valerina", "trapo", "t. piso", "barrendero", "repasador", 
        "cabo", "aljofifa", "bayeta", "guante", "secador", "charango", 
        "tehuelche", "irizar", "sauce", "pabilo", "americana", "multiuso",
        "consorcio", "abeja", "pino", "escobilla", "pala", "barrehojas"
    ]):
        return "limpieza_hogar"
    
    # 7. UTENSILIOS PLÁSTICOS
    if any(x in nombre_lower for x in [
        "compotera", "cazuela", "lunchera", "vaso", "balde", "cubetera", 
        "cubierto", "fuenton", "cesto", "palangana", "barrehojas", 
        "escobilla", "pala", "secador", "basura", "resistent", 
        "alta calidad", "extraduro", "vasitos de nenes"
    ]):
        return "utensilios_plasticos"
    
    # 8. PAPEL HIGIÉNICO/COCINA (SOLO productos de papel higiénico y servilletas)
    if any(x in nombre_lower for x in [
        "calipso", "family", "grand family", "mega family", "papel higiénico", 
        "toalla", "rollo", "higiénico", "servilleta", "pañuelo", 
        "pañuelitos", "kitchen", "cocina", "perfumado", "eco", "esp."
    ]):
        return "papel_higienico_cocina"
    
    # 9. OTROS (todo lo demás)
    return "otros"

def main():
    try:
        # Ruta del Excel
        excel_path = os.path.join(os.path.dirname(__file__), "datos.xlsx")
        if not os.path.exists(excel_path):
            logger.error(f"Archivo Excel no encontrado: {excel_path}")
            return 1
        
        # Leer Excel
        logger.info("Leyendo archivo Excel...")
        df = pd.read_excel(excel_path)
        logger.info(f"Excel leído: {len(df)} productos encontrados")
        
        # Verificar columnas necesarias
        if 'Nombre' not in df.columns:
            logger.error("La columna 'Nombre' no existe en el Excel")
            return 1
            
        # Limpiar datos
        df_clean = df.dropna(subset=['Nombre']).copy()
        df_clean = df_clean[df_clean['Nombre'].astype(str).str.strip() != '']
        logger.info(f"Después de limpieza: {len(df_clean)} productos válidos")
        
        # Extraer precio y limpiar nombre
        logger.info("Procesando precios y nombres...")
        df_clean['precio_extraido'] = df_clean['Nombre'].apply(extraer_precio)
        df_clean['nombre_limpio'] = df_clean['Nombre'].apply(limpiar_nombre)
        
        # Clasificar productos
        logger.info("Clasificando productos...")
        df_clean['categoria'] = df_clean['nombre_limpio'].apply(clasificar_producto)
        
        # Filtrar productos excluidos
        df_final = df_clean[df_clean['categoria'] != 'excluir'].copy()
        logger.info(f"Productos después de excluir envíos: {len(df_final)}")
        
        # Mostrar distribución
        distribucion = df_final['categoria'].value_counts()
        logger.info("\nDistribución de categorías:")
        for cat, count in distribucion.items():
            logger.info(f"  {cat}: {count} productos")
        
        # Mostrar algunos ejemplos problemáticos para verificar
        logger.info("\nVerificando clasificación de productos específicos:")
        productos_verificar = [
            "DETERG. S.F. VERDE 600", "BOLSA P/HORNO HORNAL", "BOLSA P/FREEZER 25X35 HORNAL",
            "SEPARADORES FREEZER HORNAL", "ROLLO FILM POLIETILENO 45 CM X 500 MTS",
            "MARCADOR NEGRO INDELEBLE", "CUBIERTOS MULTIUSOS", "ESPUMA LIMPIA HORNOS Y PARRILLA",
            "T. PISO GRIS 48X58CM", "T. PISO CONSORCIO GRIS 60X70CM"
        ]
        
        for producto in productos_verificar:
            producto_limpio = limpiar_nombre(producto)
            categoria = clasificar_producto(producto_limpio)
            logger.info(f"  - {producto_limpio} → {categoria}")
        
        # Conexión a la base de datos
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "app", "productos.db")
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        engine = create_engine(f"sqlite:///{db_path}")
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Crear tablas
        Base.metadata.create_all(engine)
        logger.info("Tablas creadas/verificadas")
        
        # Mapear categoría a clase
        categoria_map = {
            "papel_higienico_cocina": PapelHigienicoCocina,
            "bolsas_envases": BolsasEnvases,
            "limpieza_hogar": LimpiezaHogar,
            "limpieza_quimica": LimpiezaQuimica,
            "insecticidas": Insecticidas,
            "cuidado_personal": CuidadoPersonal,
            "utensilios_plasticos": UtensiliosPlastico,
            "otros": Otros
        }
        
        # Insertar productos - SOLO NOMBRE POR AHORA
        logger.info("Insertando productos en la base de datos...")
        contadores = {categoria: 0 for categoria in categoria_map.keys()}
        
        for _, row in df_final.iterrows():
            try:
                cls = categoria_map[row['categoria']]
                # Por ahora solo insertamos el nombre hasta que confirmes el campo de precio
                producto = cls(valor=row['nombre_limpio'])
                session.add(producto)
                contadores[row['categoria']] += 1
            except Exception as e:
                logger.warning(f"Error insertando '{row['nombre_limpio']}': {e}")
        
        # Confirmar cambios
        session.commit()
        logger.info("Inserción completada")
        
        # Mostrar resumen final
        logger.info("\n" + "="*50)
        logger.info("RESUMEN FINAL DE CLASIFICACIÓN:")
        logger.info("="*50)
        for categoria, count in contadores.items():
            logger.info(f"  {categoria}: {count} productos")
        
        total_insertados = sum(contadores.values())
        logger.info(f"Total productos insertados: {total_insertados} de {len(df_final)}")
        
        # Comparación con distribución esperada
        logger.info("\nComparación con distribución esperada:")
        distribucion_esperada = {
            "papel_higienico_cocina": 34,
            "bolsas_envases": 76, 
            "limpieza_hogar": 48,
            "limpieza_quimica": 120,
            "insecticidas": 16,
            "cuidado_personal": 70,
            "utensilios_plasticos": 21,
            "otros": 59
        }
        
        for cat, esperado in distribucion_esperada.items():
            actual = contadores.get(cat, 0)
            diferencia = actual - esperado
            status = "✅" if abs(diferencia) <= 2 else "❌"
            logger.info(f"  {status} {cat}: {actual} (esperado: {esperado}) - diferencia: {diferencia:+d}")
        
        session.close()
        return 0
        
    except Exception as e:
        logger.error(f"Error en el proceso: {e}")
        if 'session' in locals():
            session.rollback()
            session.close()
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)