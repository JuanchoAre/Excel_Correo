from pydantic import BaseModel, Field
from typing import Optional

class EmailBase(BaseModel):
    """
    Modelo base con credenciales y contenido del correo.
    Usado para enviar correos a todos sin filtros adicionales.
    """
    email: str = Field(..., description="Email address to send from")
    password: str = Field(..., description="Password or application password for the email account")
    subject: str = Field("Notificación Importante", description="Subject of the email")
    message: str = Field("Hola, este es un mensaje automático.", description="Body of the email")

class EmailFilterAge(EmailBase):
    """
    Modelo extendido para filtrar usuarios por rango de edad.
    """
    min_age: int = Field(..., description="Minimum age (inclusive)")
    max_age: int = Field(..., description="Maximum age (inclusive)")

class EmailFilterStatus(EmailBase):
    """
    Modelo extendido para filtrar usuarios por estado (activo/inactivo).
    """
    is_active: bool = Field(..., description="Status of the user (true for active, false for inactive)")