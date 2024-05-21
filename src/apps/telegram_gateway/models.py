from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship

from src.core.mixins.model_mixins import AbstractBase


class Chat(AbstractBase):
    __tablename__ = "chat"
    chat_id = Column(Integer, unique=True)
    first_name = Column(String)
    language = Column(String)
    messages = relationship("Message", backref="chat")


class Message(AbstractBase):
    __tablename__ = "message"
    chat_id = Column(ForeignKey("chat.id", ondelete="CASCADE"))
    text = Column(String)