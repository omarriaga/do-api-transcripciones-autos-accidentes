from pydantic import BaseModel, field_validator
from typing import Optional, Any
from datetime import date, datetime, time

ERROR_FECHA_INVALIDA = "Fecha inválida. Debe ser en formato DD/MM/YYYY o YYYY-MM-DD"

class Transcripcion(BaseModel):
    id_conversacion: Optional[str]
    dnis: Optional[str]
    id_cola: Optional[str]
    nombre_cola: Optional[str]
    id_usuario: Optional[str]
    nombre_usuario: Optional[str]
    username: Optional[str]
    emisor: Optional[str]
    fecha_inicio_participante: Optional[datetime]
    fecha_fin_participante: Optional[datetime]
    equipo: Optional[str]
    sentimiento: Optional[float]
    tendencia_sentimiento: Optional[float]
    transcripcion: Optional[str]
    confianza: Optional[float]
    tipo_direccion: Optional[str]
    hora_transcripciones_mil: Optional[datetime]
    fecha_cargue: Optional[str]

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
