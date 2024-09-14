from __future__ import annotations

from enum import Enum, auto
from dataclasses import dataclass, field
from dataclasses import fields as list_fields
from datetime import datetime
import logging
import re
from typing import Any

from bson import ObjectId
from pymongo.collection import Collection

import db

logging.getLogger().setLevel(logging.ERROR)


class NonAdminRoles(str, Enum):
    neutralizer = auto()
    reviewer = auto()
    hybrid = auto()
    
class Roles(str, Enum):
    admin = auto()
    neutralizer = auto()
    reviewer = auto()
    hybrid = auto()
    

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
    coll: Collection = None

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

    def update(self, d: dict=None, force: dict = None, **kw) -> bool: # type: ignore
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
        try:
            self.coll.update_one(
                filter = {'_id': self.oid},
                update = update
            )
            return True
        except Exception as e:
            logging.error('Update failed', exc_info=e)
            return False

@dataclass(kw_only=True)
class User(Model):

    coll: Collection = db.collections[db.USERS]

    active: bool
    alias: str = ''
    created_at: datetime
    last_updated: datetime = None
    locale: str = 'en'
    role: Roles

@dataclass(kw_only=True)
class Segment(Model):

    coll: Collection = db.collections[db.SEGMENTS]

    active: bool
    created_at: datetime
    lang: str
    last_updated: datetime = None
    source: str