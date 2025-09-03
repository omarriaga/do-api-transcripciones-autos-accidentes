
import sqlalchemy


from utils.connect_sql import get_raw_connection
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncConnection
from typing import Optional
from models.models import DataRequest, DataResponse, Transcripcion
from datetime import timedelta

SIETE_DIAS = timedelta(days=7)

async def consultar_conversacion(
    request: DataRequest,
    db: AsyncConnection = Depends(get_raw_connection)
) -> Optional[DataResponse]:

    sql = """
        SELECT  id_conversacion, dnis, id_cola, nombre_cola, id_usuario, nombre_usuario, username, emisor, 
                fecha_inicio_participante, fecha_fin_participante, equipo, sentimiento, tendencia_sentimiento, 
                transcripcion, confianza, tipo_direccion, hora_transcripciones_mil, fecha_cargue
        FROM api_backend.t_transcripciones_autos_accidentes
        WHERE 1 = 1        
    """

    params = {}

    if request.dni:
        params["dnis"] = request.dni
        sql += " AND dnis like '%:dnis%' "
    if request.fecha:
        params["fecha_inicio"] = request.fecha - SIETE_DIAS
        params["fecha_fin"] = request.fecha + SIETE_DIAS
        sql += " AND hora_transcripciones_mil between :fecha_inicio and :fecha_fin "
    if request.gestor:
        params["gestor"] = request.gestor
        sql += " AND name like '%:gestor%' "

    query = sqlalchemy.text(sql)
        
    results = await db.execute(query, params)

    rows = results.mappings().all()
    if rows:
        return DataResponse(data=[Transcripcion(**row) for row in rows])

    return None

