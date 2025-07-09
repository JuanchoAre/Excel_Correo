from pydantic import BaseModel, Field
from typing import Optional

class EmailData(BaseModel):
    """
    email and password for the email handler
    """

    username: str = Field(..., description="Email address to send from")
    password: str = Field(..., description="Password or application password for the email account")