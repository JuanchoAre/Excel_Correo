import os
from typing import List, Optional
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Body, Query
from pymongo import MongoClient
from loguru import logger
from api.scheme.basemodel import EmailBase, EmailFilterAge, EmailFilterStatus

from src.class_handler import Email_Handler

# Cargar variables de entorno
load_dotenv()

router = APIRouter()

# Configuración de MongoDB
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_USER_COLLECTION = os.getenv("MONGO_USER_COLLECTION")
MONGO_SENT_COLLECTION = os.getenv("MONGO_SENT_COLLECTION")

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client[MONGO_DB]
    user_collection = db[MONGO_USER_COLLECTION]
    sent_collection = db[MONGO_SENT_COLLECTION]
    
    # Forzar verificación de conexión
    client.admin.command('ping')
    logger.info("Conexión a MongoDB establecida y verificada exitosamente")
except Exception as e:
    logger.error(f"FALLO CRÍTICO al conectar con MongoDB: {e}")
    # Opcional: Podríamos no levantar la app si la DB falla, 
    # pero por ahora solo logueamos el error grave.



def send_emails_to_docs(documents: List[dict], credentials: EmailBase):
    """Función auxiliar para iterar documentos y enviar correos."""
    email_handler = Email_Handler(
        email=credentials.email, 
        password=credentials.password
    )
    
    count = 0
    for doc in documents:
        user_email = doc.get("correo")
        
        if user_email:
            # send_email espera: to_email, subject, message
            if email_handler.send_email(user_email, credentials.subject, credentials.message):
                count += 1
                logger.info(f"Correo enviado a {user_email}")
                sent_collection.insert_one({
                    "email": user_email,
                    "message": credentials.message,
                    })
            else:
                logger.warning(f"Fallo al enviar a {user_email}")
        else:
            logger.warning("Correo no encontrado en el documento.")
    return count

@router.post("/database-operation")
async def database_operation(payload: dict = Body(...)):
    """
    Endpoint dedicado a operaciones de base de datos.
    """
    try:
        # =================================================================
        # ESPACIO PARA TU CÓDIGO (LÓGICA PERSONALIZADA)
        # Aquí puedes procesar los datos recibidos, leer archivos, etc.
        # =================================================================
        
        # Ejemplo de operación (puedes borrar o modificar esto):
        logger.info(f"Procesando datos: {payload}")
        return {"message": "Operación de base de datos realizada con éxito"}

    except Exception as e:
        logger.error(f"Error en la operación de base de datos: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/send-emails/all", tags=["Emails"])
async def send_emails_all(request: EmailBase):
    """Envia correos a TODOS los usuarios en la base de datos."""
    try:
        cursor = user_collection.find({})
        docs = list(cursor)
        sent_count = send_emails_to_docs(docs, request)
        return {"message": f"Se enviaron {sent_count} correos exitosamente."}
    except Exception as e:
        logger.error(f"Error en send-emails/all: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/send-emails/by-age")
async def send_emails_by_age(request: EmailFilterAge):
    """Envia correos a usuarios dentro de un rango de edad."""
        
    try:
        query = {"edad": {"$gte": request.min_age, "$lte": request.max_age}}
        cursor = user_collection.find(query)
        docs = list(cursor)
        sent_count = send_emails_to_docs(docs, request)
        return {"message": f"Se enviaron {sent_count} correos a usuarios entre {request.min_age} y {request.max_age} años."}
    except Exception as e:
        logger.error(f"Error en send-emails/by-age: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/send-emails/by-status")
async def send_emails_by_status(request: EmailFilterStatus):
    """Envia correos filtrando por si el usuario está activo o no."""
        
    try:
        query = {"activo": request.is_active}
        cursor = user_collection.find(query)
        docs = list(cursor)
        sent_count = send_emails_to_docs(docs, request)
        status_str = "activos" if request.is_active else "inactivos"
        return {"message": f"Se enviaron {sent_count} correos a usuarios {status_str}."}
    except Exception as e:
        logger.error(f"Error en send-emails/by-status: {e}")
        raise HTTPException(status_code=500, detail=str(e))