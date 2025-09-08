
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

