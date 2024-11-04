from enum import StrEnum

import settings

URI = 'mongodb://127.0.0.1:27017'


class CollectionName(StrEnum):
    NEUTRALIZATIONS = 'neutralizations'
    REVIEWS = 'reviews'
    ROLES = 'roles'
    SEGMENTS = 'segments'
    TEAMS = 'teams'
    USERS = 'users'