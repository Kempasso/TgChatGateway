from sqlalchemy.future import select

from src.core.mixins.query_mixins import GetMixin, CreateMixin
from src.apps.authentication.models import User


class UserRepository(GetMixin, CreateMixin):
    def __init__(self, session):
        self.table = User
        self.session = session
