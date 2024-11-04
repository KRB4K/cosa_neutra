from motor import motor_asyncio
from motor.motor_asyncio import AsyncIOMotorCollection as Collection
from db.main import CollectionName, settings, URI

client = motor_asyncio.AsyncIOMotorClient(URI)
DB = client[settings.DB_NAME]
collections: dict[CollectionName, Collection] = {c.value:DB[c.value] for c in CollectionName}