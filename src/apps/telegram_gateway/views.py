import asyncio
import json

from fastapi import APIRouter, Request, Depends, WebSocket, BackgroundTasks
from fastapi.routing import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from src.apps.telegram_gateway.models import Chat, Message
from src.apps.telegram_gateway.services import TelegramGatewayService
from src.core import redis_service
from src.core.database import get_session

telegram_gateway_router = APIRouter()


@telegram_gateway_router.post("/receive_messages/")
async def receive_messages(request: Request, background_tasks: BackgroundTasks = BackgroundTasks(),
                           session: AsyncSession = Depends(get_session)):
    message_data = await request.json()
    if not (text := message_data.get('message', {}).get('text')):
        return JSONResponse(content='Please provide text message', status_code=400)
    tg_gateway_service = TelegramGatewayService()
    await tg_gateway_service.process_message(message_data=message_data, session=session, text=text,
                                             background_tasks=background_tasks)
    return JSONResponse({"status": f"Message was accepted"})


@telegram_gateway_router.websocket("/ws/help_operator")
async def websocket_chat(websocket: WebSocket, session: AsyncSession = Depends(get_session)):
    await websocket.accept()
    chat_id = None
    closed_by_operator = False
    try:
        chat_id = await redis_service.pop_one_set_element('operator_needed')
        if chat_id:
            chat_id = int(chat_id.decode('utf-8'))
            await redis_service.add_element_to_set('operator_processing', chat_id)
            pubsub = await redis_service.subscribe_to_channel(f"chat_{chat_id}_messages")
            result = await session.execute(
                select(Chat).where(Chat.chat_id == chat_id).options(joinedload(Chat.messages)))
            chat = result.scalars().first()

            if chat:
                await websocket.send_json({
                    "chat_id": chat.id,
                    "messages": [{"text": message.text} for message in chat.messages]
                })

                while True:
                    if closed_by_operator:
                        break
                    done, pending = await asyncio.wait(
                        [pubsub.get_message(ignore_subscribe_messages=True, timeout=1), websocket.receive_text()],
                        return_when=asyncio.FIRST_COMPLETED,
                        timeout=1
                    )
                    for task in done:
                        if event := task.result():
                            if isinstance(event, dict):
                                data_json = json.loads(event.get('data'))
                            elif isinstance(event, str):
                                data_json = json.loads(event)
                                if data_json.get('action') == 'close':
                                    closed_by_operator = True
                                    break
                            new_message = Message(text=data_json['text'], chat_id=chat.id)
                            session.add(new_message)
                            await session.commit()
                            await websocket.send_json({
                                "text": data_json.get('text'),
                                "chat_id": chat.id
                            })
                    for task in pending:
                        task.cancel()
    except Exception:
        print(f"WebSocket disconnected")
    finally:
        if chat_id:
            if closed_by_operator:
                await redis_service.remove_element_from_set('operator_processing', chat_id)
            else:
                await redis_service.remove_element_from_set('operator_processing', chat_id)
                await redis_service.add_element_to_set('operator_needed', chat_id)
            await redis_service.unsubscribe_from_channel(pubsub=pubsub, channel=f"chat_{chat_id}_messages")
            await redis_service.close_connection()
        await websocket.close()
