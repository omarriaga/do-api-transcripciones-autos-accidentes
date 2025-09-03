from pydantic import BaseModel, field_validator
from typing import Optional, Any
from datetime import date, datetime, time

ERROR_FECHA_INVALIDA = "Fecha inválida. Debe ser en formato DD/MM/YYYY o YYYY-MM-DD"

class Transcripcion(BaseModel):
    id_conversacion: Optional[str]
    dnis: str
    id_cola: str
    nombre_cola: str
    id_usuario: str
    nombre_usuario: str
    username: str
    emisor: str
    fecha_inicio_participante: datetime
    fecha_fin_participante: datetime
    equipo: str
    sentimiento: float
    tendencia_sentimiento: str
    transcripcion: str
    confianza: float
    tipo_direccion: str
    hora_transcripciones_mil: int
    fecha_cargue: datetime

class DataResponse(BaseModel):
    data: list[Transcripcion]

class DataRequest(BaseModel):
    dni: Optional[str] = None
    fecha: Optional[datetime] = None
    gestor: Optional[str] = None

    @field_validator('fecha', mode='before')
    @classmethod
    def parse_fecha(cls, value: Any) -> datetime:
        if isinstance(value, datetime):
            dt = value
        elif isinstance(value, date):
            dt = datetime.combine(value, time.min)
        elif isinstance(value, str):
            # Intenta formato DD/MM/YYYY
            try:
                dt = datetime.strptime(value, "%d/%m/%Y")
            except ValueError:            
                try:
                    dt = datetime.strptime(value, "%Y-%m-%d")
                except ValueError:
                    raise ValueError(ERROR_FECHA_INVALIDA)
        else:
            raise ValueError(ERROR_FECHA_INVALIDA)
        # Siempre a la primera hora del día
        return dt.replace(hour=0, minute=0, second=0, microsecond=0)
