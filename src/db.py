from enum import StrEnum

from motor.motor_asyncio import AsyncIOMotorClient
from motor.motor_asyncio import AsyncIOMotorCollection as AsyncCollection
from pymongo import MongoClient
from pymongo.collection import Collection

import settings


URI = settings.MONGO_URI

sync_client = MongoClient(URI, UuidRepresentation="standard")
async_client= AsyncIOMotorClient(URI, UuidRepresentation="standard")


class CollectionName(StrEnum):
    GAMES = 'games'
    LANGUAGES = 'languages'
    NEUTRALIZATIONS = 'neutralizations'
    REVIEWS = 'reviews'
    ROLES = 'roles'
    SEGMENTS = 'segments'
    TEAMS = 'teams'
    TEAM_MEMBERS = 'team_members'
    USERS = 'users'


class _Client:
    __client: MongoClient|AsyncIOMotorClient

    def __init__(self, client, db):
        self.__client = client
        self.__db = db

    def __getattribute__(self, name: str):
        value = object.__getattribute__(self, name)
        if name.startswith('_'):
            return value
        else:
            collection = self.__client[self.__db][value]
            return collection
        


class SyncClient(_Client):
    games: Collection = CollectionName.GAMES
    languages: Collection = CollectionName.LANGUAGES
    neutralizations: Collection = CollectionName.NEUTRALIZATIONS
    reviews: Collection = CollectionName.REVIEWS
    roles: Collection = CollectionName.ROLES
    segments: Collection = CollectionName.SEGMENTS
    teams: Collection = CollectionName.TEAMS
    team_members: Collection = CollectionName.TEAM_MEMBERS
    users: Collection = CollectionName.USERS

class AsyncClient(_Client):
    games: AsyncCollection = CollectionName.GAMES
    languages: AsyncCollection = CollectionName.LANGUAGES
    neutralizations: AsyncCollection = CollectionName.NEUTRALIZATIONS
    reviews: AsyncCollection = CollectionName.REVIEWS
    roles: AsyncCollection = CollectionName.ROLES
    segments: AsyncCollection = CollectionName.SEGMENTS
    teams: AsyncCollection = CollectionName.TEAMS
    team_members: AsyncCollection = CollectionName.TEAM_MEMBERS
    users: AsyncCollection = CollectionName.USERS



SYNC = SyncClient(sync_client, settings.DB_NAME)
ASYNC = AsyncClient(async_client, settings.DB_NAME)