from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from api.routers import send_email, login

description = "API para enviar un correo desde una lista de excel"
app = FastAPI(
    title="API enviar correo",
    description=description,)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "API para Enviar correos desde datos del excel"}

app.include_router(login.router)
app.include_router(send_email.router)
