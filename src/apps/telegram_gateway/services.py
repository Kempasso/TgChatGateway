import json

from src.apps.telegram_gateway.repositories import ChatRepository, MessageRepository
from src.apps.telegram_gateway.serializers import CreateChatSerializer
from src.core import redis_service
from fastapi import BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from src.providers import gpt_provider, tg_provider
from src.providers.chat_gpt_api.prompts import prompts


class TelegramGatewayService:

    async def process_message(self, message_data: dict, session: AsyncSession, text: str,
                              background_tasks: BackgroundTasks):
        message = message_data["message"]
        message_from = message.get('from', None)
        chat = CreateChatSerializer(**message_from)
        chat_repo = ChatRepository(session=session)
        message_repo = MessageRepository(session=session)
        chat_instance = await chat_repo.get_or_create(**chat.model_dump())
        message_instance = await message_repo.create(text=text, chat=chat_instance)
        operator_needed = await redis_service.check_set_element('operator_needed', chat_instance.chat_id)
        operator_processing = await redis_service.check_set_element('operator_processing', chat_instance.chat_id)
        if operator_processing or operator_needed:
            if operator_processing:
                await redis_service.publish_to_channel(channel=f"chat_{chat_instance.chat_id}_messages",
                                                       message={"text": text})
            return
        background_tasks.add_task(analyze_message_text_task, text=text, chat_id=chat_instance.chat_id)


async def analyze_message_text_task(text, chat_id):
    current_prompt = prompts['analyze_message_text']
    summary_prompt = f"#### Requirements\n{current_prompt}\n##### User input\n{text}"
    gpt_response = await gpt_provider.send_request(prompt=summary_prompt)
    gpt_response = json.loads(gpt_response)
    answer = gpt_response.get('answer')
    if gpt_response.get('operator'):
        await redis_service.add_element_to_set(channel='operator_needed', value=chat_id)
    await tg_provider.send_message(chat_id=chat_id, text=answer)
