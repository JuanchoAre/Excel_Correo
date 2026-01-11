import os
from typing import List, Optional
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Body, Query
from pymongo import MongoClient
from loguru import logger

# Cargar variables de entorno
load_dotenv()
router = APIRouter()

# Configuración de MongoDB
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")

try:
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    collection = db[MONGO_COLLECTION]
    logger.info("Conexión a MongoDB exitosa")
except Exception as e:
    logger.error(f"Error al conectar con MongoDB: {e}")

router.post("/login", tags=["Login"])
def login(email: str, password: str):
    try:
        cursor = collection.find({"correo": email, "contraseña": password})
        docs = list(cursor)
        if docs:
            return {"message": "Login exitoso"}
        else:
            return {"message": "Credenciales incorrectas"}
    except Exception as e:
        logger.error(f"Error en login: {e}")
        raise HTTPException(status_code=500, detail=str(e))

router.post("/register", tags=["Login"])
def register(user: str, email: str, password: str):
    try:
        cursor = collection.find({"correo": email})
        docs = list(cursor)
        if docs:
            return {"message": "Correo ya registrado"}
        else:
            collection.insert_one({"nombre": user, "correo": email, "contraseña": password})
            return {"message": "Registro exitoso"}
    except Exception as e:
        logger.error(f"Error en register: {e}")
        raise HTTPException(status_code=500, detail=str(e))