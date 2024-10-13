from __future__ import annotations

from dataclasses import dataclass
from datetime import  datetime

from pymongo.collection import Collection

import db
from models.main import Model

@dataclass(kw_only=True)
class Segment(Model):

    coll: Collection = db.collections[db.CollectionName.SEGMENTS]

    active: bool
    created_at: datetime
    lang: str
    last_updated: datetime = None
    source: str