import asyncio
import io
from time import sleep

import pandas as pd
from loguru import logger
from fastapi import APIRouter, HTTPException, UploadFile, File, Form

from src.class_handler import Excel_Handler, Email_Handler
from api.scheme.basemodel import EmailData

xlsx = Excel_Handler()

router = APIRouter()
@router.post("/send-email")
async def send_email(file: UploadFile = File(...), 
                    username: str = Form(...), 
                    password: str = Form(...)):
    """endpoint para enviar un correo desde una lista de excel"""
    email = Email_Handler(
    smtp_server='smtp.gmail.com',
    smtp_port=587,
    username=username,
    password=password
)

    try:
        content = await file.read()
        buffer = io.BytesIO(content)
        new_list = xlsx.excel_to_list(buffer)
        logger.success(new_list)
    except Exception as e:
        logger.error(f"Error al leer el archivo de Excel: {e}")
        raise HTTPException(status_code=500, detail="Error al leer el archivo de Excel")
    sleep(2)

    for email_list in new_list:
        email.send_email(email_list)

    logger.success("Correos enviados exitosamente")
    return {"message": "Correos enviados exitosamente"}