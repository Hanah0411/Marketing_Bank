# =============================================
# 📁 Archivo: /app/models/schemas.py
# =============================================
"""
Schemas de Pydantic para validación de datos
en endpoints de la API.
"""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, conint, confloat

class JobType(str, Enum):
    """Tipos de trabajo válidos."""
    ADMIN = "admin."
    BLUE_COLLAR = "blue-collar"
    ENTREPRENEUR = "entrepreneur"
    HOUSEMAID = "housemaid"
    MANAGEMENT = "management"
    RETIRED = "retired"
    SELF_EMPLOYED = "self-employed"
    SERVICES = "services"
    STUDENT = "student"
    TECHNICIAN = "technician"
    UNEMPLOYED = "unemployed"
    UNKNOWN = "unknown"

class MaritalStatus(str, Enum):
    """Estados civiles válidos."""
    DIVORCED = "divorced"
    MARRIED = "married"
    SINGLE = "single"
    UNKNOWN = "unknown"

class Education(str, Enum):
    """Niveles educativos válidos."""
    PRIMARY = "primary"
    SECONDARY = "secondary"
    TERTIARY = "tertiary"
    UNKNOWN = "unknown"

class YesNo(str, Enum):
    """Opciones Sí/No."""
    YES = "yes"
    NO = "no"
    UNKNOWN = "unknown"

class Contact(str, Enum):
    """Tipos de contacto válidos."""
    CELLULAR = "cellular"
    TELEPHONE = "telephone"
    UNKNOWN = "unknown"

class Month(str, Enum):
    """Meses válidos."""
    JAN = "jan"
    FEB = "feb"
    MAR = "mar"
    APR = "apr"
    MAY = "may"
    JUN = "jun"
    JUL = "jul"
    AUG = "aug"
    SEP = "sep"
    OCT = "oct"
    NOV = "nov"
    DEC = "dec"

class Outcome(str, Enum):
    """Resultados posibles de campaña previa."""
    SUCCESS = "success"
    FAILURE = "failure"
    OTHER = "other"
    UNKNOWN = "unknown"

class PredictionRequest(BaseModel):
    """
    Modelo de datos para solicitud de predicción.
    Incluye validaciones y valores por defecto.
    """
    age: conint(ge=18, le=100) = Field(..., description="Edad del cliente (18-100)")
    job: JobType = Field(..., description="Tipo de trabajo")
    marital: MaritalStatus = Field(..., description="Estado civil")
    education: Education = Field(..., description="Nivel educativo")
    default: YesNo = Field(YesNo.NO, description="¿Tiene crédito en incumplimiento?")
    balance: confloat(ge=-10000, le=1000000) = Field(..., description="Saldo promedio anual")
    housing: YesNo = Field(..., description="¿Tiene préstamo de vivienda?")
    loan: YesNo = Field(..., description="¿Tiene préstamo personal?")
    contact: Contact = Field(..., description="Tipo de contacto")
    day: conint(ge=1, le=31) = Field(..., description="Último día de contacto del mes")
    month: Month = Field(..., description="Último mes de contacto")
    duration: conint(ge=0, le=5000) = Field(..., description="Duración del último contacto (segundos)")
    campaign: conint(ge=1, le=50) = Field(..., description="Número de contactos para esta campaña")
    pdays: conint(ge=-1) = Field(..., description="Días desde último contacto (-1 si no contactado)")
    previous: conint(ge=0) = Field(..., description="Número de contactos previos")
    poutcome: Outcome = Field(Outcome.UNKNOWN, description="Resultado de campaña anterior")

    class Config:
        schema_extra = {
            "example": {
                "age": 45,
                "job": "management",
                "marital": "married",
                "education": "tertiary",
                "default": "no",
                "balance": 1200.0,
                "housing": "yes",
                "loan": "no",
                "contact": "cellular",
                "day": 12,
                "month": "may",
                "duration": 300,
                "campaign": 2,
                "pdays": -1,
                "previous": 0,
                "poutcome": "unknown"
            }
        }

class PredictionResponse(BaseModel):
    """Modelo de datos para respuesta de predicción."""
    prediction: str = Field(..., description="Predicción ('yes': acepta, 'no': no acepta)")
    message: str = Field(..., description="Mensaje explicativo de la predicción")
    linked_client_id: Optional[int] = Field(None, description="ID del cliente si existe en BD")
    probability: float = Field(..., description="Probabilidad de aceptación")