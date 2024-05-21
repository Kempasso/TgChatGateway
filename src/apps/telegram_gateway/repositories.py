from src.core.mixins.query_mixins import CreateMixin
from src.apps.telegram_gateway.models import Chat, Message


class ChatRepository(CreateMixin):

    def __init__(self, session):
        self.session = session
        self.table = Chat


class MessageRepository(CreateMixin):

    def __init__(self, session):
        self.session = session
        self.table = Message
