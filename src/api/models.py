
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from dataclasses import fields as list_fields
from datetime import datetime
import logging
import random
from typing import Any, Iterable, Type, TypeVar

from bson import ObjectId
import telegram

from api.enums import Roles
import db
import settings
from static import DEFAULT_GAME, DEFAULT_WORKING_LANGUAGE
from utils import only, today, find_streaks


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

    game: ObjectId
    source: str
    target: str
    to_neutralize: str
    source_lang: str
    target_lang: str
    to_neutralize_lang: str
    last_updated: datetime = None
    origin: str
    

    @classmethod
    def pick_next_for(cls, user: User, game: ObjectId=DEFAULT_GAME) -> dict:
        """Returns the next segment for the user"""
        neutralizations = user.get_neutralizations()
        done = [n.segment for n in neutralizations]
        segment = cls.sx_coll.find({
            '_id':{'$nin':done},
            'to_neutralize_lang':user.working_language
        }).sort('_id', 1)
        segment = next(segment, None)
        segment_id = None
        if segment:
            segment = cls.from_record(segment)
            segment_id = segment.oid
        return {
            'segment': segment_id,
            'task':'neutralization',
            'data':getattr(segment, segment.to_neutralize)
        }


@dataclass(kw_only=True)
class Neutralization(Model):

    sx_coll: db.Collection = db.SYNC.neutralizations
    ax_coll: db.AsyncCollection = db.ASYNC.neutralizations

    created_at: datetime
    segment: ObjectId
    text: str
    lang: str
    user: ObjectId

    @classmethod
    def insert(cls, segment: ObjectId, by: User, text:str, ) -> Neutralization:
        original = Segment.from_oid(segment)
        if not original:
            return
        record = {
            'created_at': datetime.now(),
            'segment': segment,
            'text': text,
            'user': by.oid,
            'lang': original.to_neutralize_lang            
        }
        # If a record matching on 'segment' and 'user' already exists, update it
        record = cls.sx_coll.find_one_and_update(
            filter={'segment':segment, 'user':by.oid},
            update={'$set':record},
            upsert=True,
            return_document=True  # Return the updated document
        )
        # print(record)
        # print(cls.from_record(record))
        return cls.from_record(record)

    @classmethod
    def pick_next_for(cls, user: User, game: ObjectId=DEFAULT_GAME) -> dict:
        """Returns the next neutralization to review for the user"""
        team_mates = [user]
        # A user cannot review a neutralization from a team mate
        team = user.get_team(game)
        if team:
            team_mates += team.get_members(game)
        forbidden = [m.oid for m in team_mates]

        done = list({r.segment for r in user.get_reviews()})   # done = Review.sx_coll.distinct('segment', {'user':user.oid})

        pipeline = [
            {
                '$match': {
                    'segment':{'$nin':done},
                    'user': {'$nin': forbidden},
                    'created_at': {'$lt': today()},
                    'lang': user.working_language
                }
            },
            {
                '$group': {
                    '_id': '$segment',
                    'neutralizations': {'$push': '$$ROOT'},
                    'count': {'$sum': 1}
                }
            },
            # Sort by the number of neutralizations (most first)
            {
                '$sort': {'count': -1, '_id': -1}
            },
        ]
        neutralizations = list(cls.sx_coll.aggregate(pipeline))
        segment_id = None
        data = []
        if neutralizations:
            first = neutralizations[0]
            neutralizations = first['neutralizations']
            segment_id = first['_id']
            data = [cls.from_record(n) for n in neutralizations]
            data = [d.text for d in data]
            data = list(set(data))  # Remove duplicates
        return {
            'segment':segment_id,
            'task':'review',
            'data': data
        }

@dataclass(kw_only=True)
class Review(Model):
    
    sx_coll: db.Collection = db.SYNC.reviews
    ax_coll: db.AsyncCollection = db.ASYNC.reviews

    segment: ObjectId
    user: ObjectId
    created_at: datetime
    text: str

    @classmethod
    def insert(cls, segment: ObjectId, by: User, text:str) -> Review:
        record = {
            'segment': segment,
            'user': by.oid,
            'created_at': datetime.now(),
            'text': text,
        }
        print(record)
        cls.sx_coll.insert_one(record)
        return cls.from_record(record)

@dataclass(kw_only=True)
class Game(Model):
    active: bool
    description: str
    lang: str  # currently unused and incompatible with the current design where languages are mixed
    name: str

    @staticmethod
    def get_segments(game: ObjectId) -> Iterable[Segment]:
        segments = db.SYNC.segments.find({'game':game})
        yield from (Segment.from_record(s) for s in segments)


@dataclass(kw_only=True)
class Team(Model):

    sx_coll: db.Collection = db.SYNC.teams
    ax_coll: db.AsyncCollection = db.ASYNC.teams

    name: str
    active: bool
    games: list[ObjectId]

    @classmethod
    def from_name(cls, name:str, game: ObjectId=DEFAULT_GAME) -> Team:
        record = cls.sx_coll.find_one({'name':name, 'games':game})
        if record:
            return cls.from_record(record)
        
    def get_members(self, game: ObjectId=DEFAULT_GAME) -> list[User]:
        members = db.SYNC.team_members.find({'team':self.oid, 'game':game})
        return [User.from_id(m['player']) for m in members]
        

@dataclass(kw_only=True)
class User(Model):

    sx_coll: db.Collection = db.SYNC.users
    ax_coll: db.AsyncCollection = db.ASYNC.users

    active: bool
    chat_id:str
    created_at: datetime
    first_name: str = ''
    game: ObjectId = DEFAULT_GAME
    id: int
    is_admin: bool = False
    is_bot: bool
    working_language: str = DEFAULT_WORKING_LANGUAGE
    last_updated: datetime = None
    role: Roles = None

    @classmethod
    def create_user(cls, user:telegram.User, chat_id:str):
        now = datetime.now()
        record = {
            'active': False,
            'chat_id':chat_id,
            'created_at':now,
            'first_name': user.first_name,
            'game':DEFAULT_GAME,
            'id':user.id,
            'is_admin':False,
            'is_bot':user.is_bot,
            'last_updated':now,
            'role':None,
            'working_language':user.language_code,  # default, can change during onboarding
        }
        cls.sx_coll.insert_one(record)
        return cls.from_record(record)

    @classmethod
    def from_id(cls, id:int):
        record = cls.sx_coll.find_one({'id':id})
        if record:
            return cls.from_record(record)
        

    def register_in_team(self, team_name: str, game: ObjectId=DEFAULT_GAME):
        existing = {
            'player': self.id,
            'game': game
        }
        db.SYNC.team_members.delete_many(existing) # already in a team
        team = Team.from_name(team_name, game=game)
        if not team:
            raise ValueError(f'Team {team_name} not found')
        new = {
            "team": team.oid,
            **existing
        }
        db.SYNC.team_members.insert_one(new)

    def remove_from_team(self, team: ObjectId, game: ObjectId=DEFAULT_GAME):
        record = {
            "player": self.id,
            "team": team,
            "game": game
        }
        db.SYNC.team_members.delete_one(record)

    def get_team(self, game: ObjectId=DEFAULT_GAME):
        membership = db.SYNC.team_members.find_one({'player':self.id, 'game':game})
        if not membership:
            return None
        return Team.from_oid(membership['team'])
    
    def get_neutralizations(self, game: ObjectId=DEFAULT_GAME, filters:dict=None) -> list[Neutralization]:
        filters = filters or {}
        filters.update({'user':self.oid})
        records =  Neutralization.sx_coll.find({'user':self.oid})  # , 'game':game
        return [Neutralization.from_record(r) for r in records]
    
    def get_reviews(self, game: ObjectId=DEFAULT_GAME, filters:dict=None) -> list[Review]:
        filters = filters or {}
        filters.update({'user':self.oid})
        records =  Review.sx_coll.find(filters)  # , 'game':game
        return [Review.from_record(r) for r in records]
    
    

        
class UserWithRole(User, ABC):

    @abstractmethod
    def next_to_do(self, *args, **kwargs) -> dict:
        raise NotImplementedError()
    
    @abstractmethod
    def get_available_task_type(self, *args, **kwargs) -> list[str]:
        raise NotImplementedError()
    

    @abstractmethod
    def get_score(self, *args, **kwargs) -> dict[str, int]:
        raise NotImplementedError()
    
    @classmethod
    def get_all_active_users(cls) -> list[UserWithRole]:
        records = cls.sx_coll.find({'active':True})
        users = []
        for r in records:
            role = r.get('role')
            match role:
                case 'neutralizer':
                    cls = Neutralizer
                case 'reviewer':
                    cls = Reviewer
                case 'hybrid':
                    cls = Hybrid
            users.append(cls.from_record(r))
        return users


class Neutralizer(UserWithRole):

    def next_to_do(self, *args, **kwargs):
        return Segment.pick_next_for(self)
    
    def get_available_task_type(self) -> list[str]:
        filters = {'created_at':today()}
        print(self.get_neutralizations(filters=filters), settings.DAILY_NEUTRALIZATIONS)
        if len(self.get_neutralizations(filters=filters)) >= settings.DAILY_NEUTRALIZATIONS:
            return ['neutralization']
        return []
    
    def get_score(self) -> dict[str, int]:
        total = 0
        neutralizations = self.get_neutralizations()
        total += len(neutralizations)

        # streaks = find_streaks(neutralizations)
        # streaks_3 = [s for s in streaks if s['streak'] == 3]
        # streaks_4 = [s for s in streaks if s['streak'] == 4]
        # streak_n = [s for s in streaks if s['streak'] > 4]
        # total += len(streaks)
        
        return {'neutralization': total}
    
    def get_streaks(self) -> list[dict]:
        neutralizations = self.get_neutralizations()
        streaks = find_streaks(neutralizations)
        return streaks


class Reviewer(UserWithRole):

    def next_to_do(self, *args, **kwargs):
        return Neutralization.pick_next_for(self)
    
    def get_available_task_type(self) -> list[str]:
        filters = {'created_at':today()}
        print(self.get_reviews(filters=filters), settings.DAILY_REVIEWS)
        if len(self.get_reviews(filters=filters)) >= settings.DAILY_REVIEWS:
            return ['review']
        return []
    
    def get_score(self) -> dict[str, int]:
        total = 0
        reviews = self.get_reviews()
        total += len(reviews)
        return {'review': total}

class Hybrid(UserWithRole):

    def next_to_do(self, only:list[str]=None) -> dict:
        """Returns the next item to review or neutralize at random"""
        only = only or ['neutralization', 'review']
        if not only:
            raise ValueError('You must specify the type of task to do')

        choices = []
        for task in only:
            if task == 'neutralization':
                choices.append(Segment)
            elif task == 'review':
                choices.append(Neutralization)

        cls = random.choice(choices)
        item = cls.pick_next_for(self)
        if item['data']:
            return item
        else:
            other_cls = Neutralization if cls == Segment else Segment
            item = other_cls.pick_next_for(self)
            return item

    def get_available_task_type(self) -> list[str]:
        filters = {'created_at':{'$gte':today()}}
        neutralizations = len(self.get_neutralizations(filters=filters))
        reviews = len(self.get_reviews(filters=filters))
        available = []
        if neutralizations < settings.DAILY_NEUTRALIZATIONS:
            available.append('neutralization')
        if reviews < settings.DAILY_REVIEWS:
            available.append('review')
        print(neutralizations, reviews, settings.DAILY_NEUTRALIZATIONS, settings.DAILY_REVIEWS)
        return available
    
    def get_score(self) -> dict[str, int]:
        neutralizations = self.get_neutralizations()
        reviews = self.get_reviews()
        return {'neutralization': len(neutralizations), 'review': len(reviews)}

    
