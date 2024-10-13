
from __future__ import annotations

from dataclasses import dataclass, field
from dataclasses import fields as list_fields
from datetime import datetime
from enum import Enum
import logging

from bson import ObjectId
from pymongo.collection import Collection

from utils import only
from typing import Any, Type, TypeVar

T = TypeVar('T', bound='Model')


class NonAdminRoles(str, Enum):
    neutralizer = "neutralizer"
    reviewer = "reviewer"
    hybrid = "hybrid"
    
class Roles(str, Enum):
    admin = "admin"
    neutralizer = "neutralizer"
    reviewer = "reviewer"
    hybrid = "hybrid"

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
        
    @classmethod
    def from_record(cls: Type[T], record:dict, ignore_extra: bool = True) -> T:
        """Exists to allow control of extra arguments from the DB"""
        if ignore_extra:
            record = only(record, keys=cls.list_fields())
        return cls(**record)
    
    def refresh(self) -> Model:
        return self.from_id(self.oid)
    
    @classmethod
    def _from(cls: Type[T], key: str, value: Any) -> T|None:
        obj = cls.coll.find_one({key: value})
        if not obj:
            return None
        return cls.from_record(obj, ignore_extra=True)
    
    @classmethod
    def from_id(cls: Type[T], id: ObjectId|str) -> T:
        return cls._from(key='_id', value=ObjectId(id))