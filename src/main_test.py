# from bson import ObjectId
# from static import DEFAULT_GAME

import db

# # Update all segments with {'game':DEFAULT_GAME}
# x = db.SYNC.segments.update_many({}, {'$set': {'game': DEFAULT_GAME}})
# print(x)

import utils
print(utils.today())