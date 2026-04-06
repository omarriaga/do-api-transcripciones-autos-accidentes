
import sqlalchemy


from utils.connect_sql import get_raw_connection
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncConnection
from typing import Optional
from models.models import DataRequest, DataResponse, Transcripcion, DataRequestWhatsapp, DataResponseWhatsapp, TranscripcionWhatsapp
from datetime import timedelta

SIETE_DIAS = timedelta(days=7)

async def consultar_conversacion(
    request: DataRequest,
    db: AsyncConnection = Depends(get_raw_connection)
) -> Optional[DataResponse]:

    sql = """
        SELECT id_conversacion, dialogo, "name" as nombre, username, fecha_llamada, address
        FROM api_backend.t_transcripciones_autos_accidentes
        WHERE 1 = 1        
    """

    params = {}

    if request.dni:
        params["address"] = f"%{request.dni}%"
        sql += " AND address like :address "
    if request.fecha:
        params["fecha_inicio"] = request.fecha - SIETE_DIAS
        params["fecha_fin"] = request.fecha + SIETE_DIAS
        sql += " AND fecha_llamada between :fecha_inicio and :fecha_fin "
    if request.gestor:
        params["gestor"] = f"%{request.gestor}%"
        sql += " AND username like :gestor "

    sql += " ORDER BY fecha_llamada ASC"

    query = sqlalchemy.text(sql)
        
    results = await db.execute(query, params)

    rows = results.mappings().all()
    if rows:
        return DataResponse(data=[Transcripcion(**row) for row in rows])

    return None


async def consultar_transcripcion_whatsapp(
    request: DataRequestWhatsapp,
    db: AsyncConnection = Depends(get_raw_connection)
) -> Optional[DataResponseWhatsapp]:

    sql = """
        SELECT conversationid, numero_telefono, topic, queueid, summary,
               dialogo_completo, inicio_conversacion, fin_conversacion
        FROM api_backend.t_transcripcion_whatsapp
        WHERE 1 = 1
    """

    params = {}

    if request.conversationid:
        params["conversationid"] = request.conversationid
        sql += " AND conversationid = :conversationid "
    if request.numero_telefono:
        params["numero_telefono"] = f"%{request.numero_telefono}"
        sql += " AND numero_telefono like :numero_telefono "
    if request.fecha_inicio:
        params["fecha_inicio"] = request.fecha_inicio
        sql += " AND inicio_conversacion >= :fecha_inicio "
    if request.fecha_fin:
        params["fecha_fin"] = request.fecha_fin + timedelta(days=1)
        sql += " AND inicio_conversacion < :fecha_fin "

    sql += " ORDER BY inicio_conversacion ASC"

    query = sqlalchemy.text(sql)

    results = await db.execute(query, params)

    rows = results.mappings().all()
    if rows:
        return DataResponseWhatsapp(data=[TranscripcionWhatsapp(**row) for row in rows])

    return None

