import logging

import httpx
from fastapi import FastAPI

from src.apps.telegram_gateway.views import telegram_gateway_router
from src.apps.authentication.views import auth_router
from src.core.database import Base, engine
from src.core.settings import telegram_bot_key, hostname
from src.apps.telegram_gateway.models import Chat, Message
from src.apps.authentication.models import User

app = FastAPI()
app.include_router(auth_router, prefix='/auth')
app.include_router(telegram_gateway_router)
logging.getLogger('logger').setLevel(logging.DEBUG)
logging.FileHandler(filename='log.log')


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def set_telegram_webhook():
    url = f"https://api.telegram.org/bot{telegram_bot_key}/setWebhook?url={hostname}/receive_messages/"
    async with httpx.AsyncClient() as client:
        response = await client.post(url)
        if response.status_code == 200:
            logging.debug('Telegram webhook is set')
        else:
            logging.debug('Failed')

#
@app.on_event("startup")
async def startup_event():
    # await create_tables()
    await set_telegram_webhook()
