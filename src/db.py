from argparse import Namespace
from enum import StrEnum

from pymongo import MongoClient
from pymongo.collection import Collection

import settings

# TODO: refactor mongo variable as environment variables
# TODO: define roles in a JSON files for bootstrapping

client = MongoClient('mongodb://127.0.0.1:27017')
DB = client[settings.DB_NAME]

class CollectionName(StrEnum):
    NEUTRALIZATIONS = 'neutralizations'
    REVIEWS = 'reviews'
    ROLES = 'roles'
    SEGMENTS = 'segments'
    TEAMS = 'teams'
    USERS = 'users'

collections: dict[CollectionName, Collection] = {c.value:DB[c.value] for c in CollectionName}

def bootstrap():
    # Create needed collections
    existing = DB.list_collection_names()
    for coll in CollectionName:
        if coll.value in existing:
            continue
        DB.create_collection(coll.value, check_exists=False)

