from src.core.mixins.model_mixins import AbstractBase
from sqlalchemy import Column, String, ForeignKey


class User(AbstractBase):
    __tablename__ = "user"
    username = Column(String, unique=True)
    password = Column(String)
    chat_id = Column(ForeignKey("chat.id", ondelete="CASCADE"))