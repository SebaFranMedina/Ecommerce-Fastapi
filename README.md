# Ecommerce-Fastapi
E-commerce con FastAPI + ETL desde Excel a SQLite + Interfaz web con HTML/CSS.

# 🛒 E-commerce FastAPI - Distribuidora El Alba

Proyecto web completo que combina un **proceso ETL (Extract, Transform, Load)** con una **aplicación web construida en FastAPI**.  
El objetivo fue tomar datos desde un archivo Excel, convertirlos en tablas organizadas dentro de una base de datos SQLite y exponerlos mediante una interfaz web dinámica.

---

## 🚀 Tecnologías utilizadas

- 🐍 **Python 3.11+**
- ⚡ **FastAPI** → Framework backend moderno y rápido.
- 🧱 **SQLAlchemy ORM** → Modelado de tablas y conexión con SQLite.
- 🧩 **Pydantic** → Validación y serialización de datos.
- 🖼️ **Jinja2 Templates** → Renderizado dinámico en HTML.
- 🎨 **HTML / CSS / JavaScript** → Interfaz web.
- 📊 **ETL (pandas, openpyxl)** → Conversión de datos desde Excel a base de datos.


---

## 📂 Estructura del proyecto
ecommerce/
│
├── etl/ # Proceso ETL
│ ├── conversor.py # Script que convierte datos desde Excel a la DB
│ └── datos.xlsx # Fuente de datos original
│
├── app/
│ ├── api/
│ │ └── endpoints.py # Endpoints FastAPI que exponen la información
│ ├── static/ # Recursos estáticos (CSS, JS, imágenes)
│ ├── templates/ # Plantillas HTML
│ ├── core.py # Configuración de base de datos y sesión
│ ├── models.py # Definición de modelos SQLAlchemy
│ ├── schemas.py # Modelos Pydantic (serialización)
│ ├── main.py # Punto de entrada principal (crea app y rutas)
│ └── productos.db # Base de datos resultante


## ⚙️ Instalación y ejecución

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/tuusuario/ecommerce.git
   cd ecommerce
  
2. **Crear entorno virtual**
python -m venv venv
source venv/bin/activate     # En Linux / Mac
venv\Scripts\activate        # En Windows


3. **Instalar dependencias**

pip install fastapi uvicorn sqlalchemy pydantic openpyxl pandas jinja2


4. **Ejecutar el proceso ETL**

python etl/conversor.py


Este script toma los datos desde datos.xlsx, los clasifica por categoría y los inserta en la base de datos productos.db.

5. **Iniciar la aplicación web**

uvicorn app.main:app --reload


6. **Abrir en el navegador**

http://127.0.0.1:8000


🧩 Flujo del proyecto

🔸 ETL
Lectura del Excel original (datos.xlsx).
Limpieza y transformación de los datos.
Carga final en tablas SQLite segmentadas por categoría.

🔸 Backend (FastAPI)
Endpoints para cada categoría de producto.
Tablas creadas automáticamente con SQLAlchemy.
Servidor de plantillas y archivos estáticos.

🔸 Frontend
Página principal con galería e introducción.
Panel dinámico de productos clasificados.
Diseño limpio y responsivo con styles.css.



✨ Funcionalidades:
✅ ETL automatizado desde Excel a base de datos.
✅ API REST con FastAPI para listar productos por categoría.
✅ Interfaz web con plantillas dinámicas.
✅ Enlace directo a contacto por WhatsApp.
✅ Estructura modular y escalable.

💡 Posibles mejoras futuras:
🚀 Conexión con PostgreSQL o MySQL.
🛠️ Panel de administración para agregar productos.
🔎 Filtros de búsqueda y paginación.
🌍 Despliegue en Render o Railway.

👨‍💻 Autor
Desarrollado por Sebastián Medina
📅 2025 — Todos los derechos reservados.

⚖️ Licencia
Este proyecto está bajo la licencia MIT.
Podés usarlo, modificarlo y distribuirlo libremente para tus propios fines.





