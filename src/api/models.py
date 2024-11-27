
from __future__ import annotations

from dataclasses import dataclass, field
from dataclasses import fields as list_fields
from datetime import datetime
from enum import Enum
import logging
from typing import Any, Type, TypeVar

from bson import ObjectId
import telegram
from telegram.ext import CallbackContext

from api.enums import Roles, NonAdminRoles
import db
from static import DEFAULT_GAME
from utils import only


T = TypeVar('T', bound='Model')




@dataclass
class _Custom:
    
    def __bool__(self) -> bool:
        return True
    
    def __iter__(self):
        yield from self.__dict__.items()


    def get(self, k: str, default: Any=None) -> Any:
        if k not in self.__dict__:
            raise AttributeError(f'Unknown attribute `{k}`')
        return getattr(self, k, default)
    
    @classmethod
    def list_fields(cls) -> list[str]:
        return [f.name for f in list_fields(cls)]

@dataclass(kw_only=True)
class Model(_Custom):
    _id: ObjectId
    
    sx_coll: db.Collection
    ax_coll: db.AsyncCollection

    oid: ObjectId = field(init=False)
    uid: str = field(init=False)

    def __post_init__(self):
        self.oid = ObjectId(self._id)
        self.uid = str(self._id)

    
    def __hash__(self):
        return hash((self._id, ))

    def __eq__(self, other):
        return self._id == other._id

    def __gt__(self, other):
        return self._id > other._id

    def _update(self, d: dict=None, force: dict = None, **kw): # type: ignore
        """Updates the user entry in self.coll with mappings in 'd' and 'kw'
        `force` can be used to pass the whole update operation directly"""
        if force:
            update = force
        else:
            r = d or {}
            r = force or dict(**r, **kw)
            update = {'$set':r}

        update.setdefault('$set', {})
        update['$set']['last_updated'] = datetime.now()
        filter =  {'_id': self.oid}
        return filter, update
        
    def update(self, d: dict=None, force: dict = None, **kw) -> bool:
        filter, update = self._update(d, force, **kw)
        try:
            self.sx_coll.update_one(filter, update)
            return True
        except Exception as e:
            logging.error('Update failed', exc_info=e)
            return False
        
    async def async_update(self, d: dict=None, force: dict = None, **kw) -> bool:
        filter, update = self._update(d, force, **kw)
        try:
            await self.ax_coll.update_one(filter, update)
            return True
        except Exception as e:
            logging.error('Update failed', exc_info=e)
            return False
        
    @classmethod
    def from_record(cls: Type[T], record:dict, ignore_extra: bool = True) -> T:
        """Exists to allow control of extra arguments from the DB"""
        if ignore_extra:
            record = only(record, keys=cls.list_fields())
        return cls(**record)
    
    def refresh(self) -> Model:
        return self.from_oid(self.oid)
    
    @classmethod
    def _from(cls: Type[T], key: str, value: Any) -> T|None:
        obj = cls.sx_coll.find_one({key: value})
        if not obj:
            return None
        return cls.from_record(obj, ignore_extra=True)
    
    @classmethod
    def from_oid(cls: Type[T], id: ObjectId|str) -> T:
        return cls._from(key='_id', value=ObjectId(id))



@dataclass(kw_only=True)
class Segment(Model):

    sx_coll: db.Collection = db.SYNC.segments
    ax_coll: db.AsyncCollection = db.ASYNC.segments

    active: bool
    created_at: datetime
    lang: str
    last_updated: datetime = None
    source: str




@dataclass(kw_only=True)
class Team(Model):

    sx_coll: db.Collection = db.SYNC.teams
    ax_coll: db.AsyncCollection = db.ASYNC.teams

@dataclass(kw_only=True)
class User(Model):

    sx_coll: db.Collection = db.SYNC.users
    ax_coll: db.AsyncCollection = db.ASYNC.users

    active: bool
    chat_id:str
    created_at: datetime
    first_name: str = ''
    id: int
    is_bot: bool
    working_language: str
    last_updated: datetime = None
    roles: list[Roles] = field(default_factory=list)

    @classmethod
    def exists(cls, user:telegram.User):
        if cls.sx_coll.find_one({'id':user.id}, {'_id':1}):
            return True
        return False

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
            'last_updated':now,
            'roles':[],
            'working_language':user.language_code,  # default, can change during onboarding
        }
        cls.sx_coll.insert_one(record)
        return cls.from_record(record)

    @classmethod
    def from_id(cls, id:int):
        record = cls.sx_coll.find_one({'id':id})
        if record:
            return cls.from_record(record)
        
    def set_role(self, role:Roles):
        roles = {role, *self.roles}
        roles = list(roles)
        self.update(force={'roles': roles})
        
    
    def set_working_language(self, lang:str):
        self.update(working_language=lang)
        
    def register_in_team(self, team: ObjectId, game: ObjectId=DEFAULT_GAME):
        record = {
            "team": team,
            "game": game
        }
        db.SYNC.team_members.update_one(record, {'$set': record}, upsert=True)

    def remove_from_team(self, team: ObjectId, game: ObjectId=DEFAULT_GAME):
        record = {
            "player": self.id,
            "team": team,
            "game": game
        }
        db.SYNC.team_members.delete_one(record)


def get_existing_users_ids():
    return User.sx_coll.distinct('id')

async def active_user(update: telegram.Update, context: CallbackContext) -> User:
    user = context.user_data['user'] # type: ignore
    return User.from_id(user.id)