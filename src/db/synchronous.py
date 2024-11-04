from pymongo import MongoClient
from pymongo.collection import Collection

from db.main import CollectionName, settings, URI

client = MongoClient(URI)
DB = client[settings.DB_NAME]
collections: dict[CollectionName, Collection] = {c.value:DB[c.value] for c in CollectionName}