import db
from locales import Token

tokens = {
    'fr': Token.FRENCH,
    'en': Token.ENGLISH
}

DEFAULT_GAME = db.SYNC.games.find_one({'name':'default'})
DEFAULT_GAME = DEFAULT_GAME['_id'] # type: ignore

WORKING_LANGUAGES = [tokens[lang['code']] for lang in db.SYNC.languages.find({'active':True})]

DEFAULT_WORKING_LANGUAGE = 'fr'



