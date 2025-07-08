import argparse
from argparse import ArgumentParser

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from playwright.async_api import async_playwright
from pydantic import BaseModel
from loguru import logger

from FastApi.routers import read_excel

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

app.include_router(read_excel.router)
@app.get("/")
def root():
    return {"message": "API para cambiar un dato dentro de una lista de excel"}