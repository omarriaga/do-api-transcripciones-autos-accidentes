from pydantic import BaseModel, field_validator
from typing import Optional, Any
from datetime import date, datetime, time

ERROR_FECHA_INVALIDA = "Fecha inválida. Debe ser en formato DD/MM/YYYY o YYYY-MM-DD"

class Transcripcion(BaseModel):
    id_conversacion: Optional[str]
    dialogo: Optional[str]
    nombre: Optional[str]
    username: Optional[str]
    fecha_llamada: Optional[datetime]
    address: Optional[str]
    
class DataResponse(BaseModel):
    data: list[Transcripcion]

class DataRequest(BaseModel):
    dni: Optional[str] = None
    fecha: Optional[datetime] = None
    gestor: Optional[str] = None
    id_conversacion: Optional[str] = None
    id_cola: Optional[str] = None
    codigo_conclusion: Optional[str] = None

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


ERROR_FECHA_PERIODO = "Fecha inválida para periodo. Debe ser en formato DD/MM/YYYY o YYYY-MM-DD"

def _parse_fecha_value(value: Any, error_msg: str) -> Optional[datetime]:
    if value is None:
        return None
    if isinstance(value, datetime):
        dt = value
    elif isinstance(value, date):
        dt = datetime.combine(value, time.min)
    elif isinstance(value, str):
        try:
            dt = datetime.strptime(value, "%d/%m/%Y")
        except ValueError:
            try:
                dt = datetime.strptime(value, "%Y-%m-%d")
            except ValueError:
                raise ValueError(error_msg)
    else:
        raise ValueError(error_msg)
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)


class TranscripcionWhatsapp(BaseModel):
    conversationid: Optional[str]
    numero_telefono: Optional[str]
    topic: Optional[str]
    queueid: Optional[str]
    summary: Optional[str]
    dialogo_completo: Optional[str]
    inicio_conversacion: Optional[datetime]
    fin_conversacion: Optional[datetime]

class DataResponseWhatsapp(BaseModel):
    data: list[TranscripcionWhatsapp]

class DataRequestWhatsapp(BaseModel):
    conversationid: Optional[str] = None
    numero_telefono: Optional[str] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None

    @field_validator('fecha_inicio', 'fecha_fin', mode='before')
    @classmethod
    def parse_fechas(cls, value: Any) -> datetime:
        return _parse_fecha_value(value, ERROR_FECHA_PERIODO)
