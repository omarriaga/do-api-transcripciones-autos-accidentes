import sys
sys.path.append('.')

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse
import os


from utils.request_postgres import consultar_conversacion
from utils.connect_sql import create_db_engine_async
from contextlib import asynccontextmanager
from typing import Optional
from models.models import DataResponse

# Parametros básicos y clases
from fastapi.middleware.gzip import GZipMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    engine, connector = await create_db_engine_async()
    app.state.db_engine = engine
    app.state.db_connector = connector
    yield
    await app.state.db_engine.dispose()
    await app.state.db_connector.close_async()

app = FastAPI(lifespan=lifespan)
app.add_middleware(GZipMiddleware, minimum_size=1000)
puerto = os.environ.get("PORT", 8080)

# Configuración de CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#* Definición de un endpoint
descripcion_path = 'aqui se describe el endpoint de consulta'
summary_path = 'un resumen del endpoint de consulta'
endpoint_end = '/api/transcripciones/autos-accidentes'


@app.get(endpoint_end, summary=summary_path, description=descripcion_path, response_model=Optional[DataResponse])
async def api_consulta_sabana_facilities(conversaciones: Optional[DataResponse] = Depends(consultar_conversacion)):
    if conversaciones is None:
        return JSONResponse(status_code=404, content={"error": "No hay conversaciones para mostrar"})
    return conversaciones


@app.get("/", response_class=RedirectResponse)
async def redirect_to_docs():
    return "/docs"


