import asyncio
from dataclasses import dataclass, field
from datetime import  datetime

import telegram

import db.main as db
import db.asynchronous as ax
import db.synchronous as sx
from models.main import Model, Roles

@dataclass(kw_only=True)
class User(Model):

    sx_coll: sx.Collection = sx.collections[db.CollectionName.USERS]
    ax_coll: ax.Collection = ax.collections[db.CollectionName.USERS]

    active: bool
    chat_id:str
    created_at: datetime
    first_name: str = ''
    id: int
    is_bot: bool
    language: str
    last_updated: datetime = None
    roles: list[Roles] = field(default_factory=list)

    @classmethod
    def exists(cls, user:telegram.User):
        if cls.coll.find_one():
            ...

    @classmethod
    def create_user(cls, user:telegram.User, chat_id:str):
        now = datetime.now()
        record = {
            'active': False,
            'chat_id':chat_id,
            'created_at':now,
            'first_name': user.first_name,
            'id':user.id,
            'is_bot':user.is_bot,
            'language':user.language_code,
            'last_updated':now,
        }
        cls.sx_coll.insert_one(record)
        return cls.from_record(record)

    @classmethod
    def from_id(cls, id:int):
        record = cls.coll.find_one({'id':id})
        if record:
            return cls.from_record(record)


def get_existing_users_ids():
    return User.sx_coll.distinct('id')

