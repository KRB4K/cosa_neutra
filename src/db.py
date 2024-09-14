from argparse import Namespace
from pymongo import MongoClient
from pymongo.collection import Collection
import warnings

# TODO: refactor mongo variable as environment variables
# TODO: define roles in a JSON files for bootstrapping

ROLES = 'roles'
SEGMENTS = 'segments'
TEAMS = 'teams'
USERS = 'users'

client = MongoClient('mongodb://127.0.0.1:27017')

database_name = 'cosa_neutra'
database = client[database_name]

collections: dict[str, Collection ] = {
    ROLES: database[ROLES],
    SEGMENTS: database[SEGMENTS],
    TEAMS: database[TEAMS],
    USERS: database[USERS],
}

def _init(key:str, data: list[dict]|None):
    if not data:
        return True
    collection = collections[key]
    result = collection.insert_many(data)
    if len(result.inserted_ids) == len(data):
        return True
    else:
        return False


def bootstrap(
    roles: list|None = None,
    segments: list|None = None,
    teams: list|None = None,
    users: list|None = None,

) -> None:
    existing = database.list_collection_names()
    for name, data in (
        (ROLES, roles),
        (SEGMENTS, segments),
        (TEAMS, teams),
        (USERS, users)
    ):
        if name not in existing:
            if not _init(name, data):
                warnings.warn(f'Could not bootstrap {name}')
