import json
from sqlalchemy.ext.asyncio import create_async_engine, AsyncConnection
from google.cloud import secretmanager
from google.cloud.sql.connector import Connector, IPTypes
from fastapi import Request
from helpers.credentials_helper import get_credentials


async def create_db_engine_async():
    creds_dict = get_credentials()
    INSTANCE_CONNECTION_NAME = creds_dict['host']
    DB_USER = creds_dict['user']
    DB_PASS = creds_dict['password']
    DB_NAME = creds_dict['database']

    connector = Connector()

    async def getconn():
        return await connector.connect_async(
            INSTANCE_CONNECTION_NAME,
            driver="asyncpg",
            user=DB_USER,
            password=DB_PASS,
            db=DB_NAME,
            ip_type=IPTypes.PUBLIC
        )

    engine = create_async_engine(
        "postgresql+asyncpg://",
        async_creator=getconn
    )
    # Test the connection to ensure async usage
    async with engine.begin():
        pass
    return engine, connector


async def get_raw_connection(request: Request):
    engine = request.app.state.db_engine
    async with engine.connect() as conn:
        yield conn





    