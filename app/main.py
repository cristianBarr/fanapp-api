# app/main.py

from fastapi import FastAPI
from app.api.v1.api import api_router  # <-- NUEVO: Importamos nuestro enrutador

# Creamos la instancia principal de la aplicación.
# Los parámetros title, description y version son opcionales, 
# pero hacen que la documentación automática se vea profesional.
app = FastAPI(
    title="FanApp API",
    description="Backend oficial para la app móvil del Ciclón. ¡Vamos San Lorenzo!",
    version="0.1.0"
)

# <-- NUEVO: Conectamos las rutas de la versión 1 con el prefijo /api/v1
app.include_router(api_router, prefix="/api/v1")

# Este es nuestro primer Endpoint (Ruta)
# El decorador @app.get("/") indica que si alguien hace una petición GET a la raíz de la API,
# se ejecutará la función 'read_root'.
@app.get("/")
def read_root():
    return {"message": "¡Hola Cuervo! Bienvenido a FanApp API"}

# Endpoint de "Health Check" (Chequeo de Salud)
# Es una buena práctica tener una ruta que solo diga "estoy vivo". 
# GCP (Cloud Run) usa esto para saber si el servidor está sano.
@app.get("/health")
def health_check():
    return {"status": "ok"}