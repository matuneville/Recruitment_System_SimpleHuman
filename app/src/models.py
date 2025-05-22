"""
models.py

Define el modelo de datos para representar a un candidato estudiante.
Pydantic es usado para la validación de datos y por su compatibilidad con FastAPI.
"""

from pydantic import BaseModel, Field, EmailStr
from typing import List

class StudentCandidate(BaseModel):
    full_name: str
    email: EmailStr
    college: str
    degree: str
    academic_average: float = Field(..., gt=3, le=10)
    skills: List[str] = []
    work_experience: str = '-'