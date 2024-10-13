from dataclasses import dataclass
from datetime import  datetime

from pymongo.collection import Collection
import telegram

import db
from models.main import Model, Roles

@dataclass(kw_only=True)
class User(Model):

    coll: Collection = db.collections[db.CollectionName.USERS]

    active: bool
    alias: str = ''
    chat:str
    created_at: datetime
    last_updated: datetime = None
    locale: str
    roles: list[Roles]

    @classmethod
    def exists(cls, user:telegram.User):
        if cls.coll.find_one():
            ...

    @classmethod
    def create_user(cls, user:telegram.User, chat_id:str):
        now = datetime.now()
        record = {
            'active': True,
            'alias': user.first_name,
            'chat':chat_id,
            'created_at':now,
            'last_updated':now,
            'locale':user.language_code,
        }