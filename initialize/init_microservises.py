from support_files.functions import *
from initialize.validators import *


counters = get_collection(COUNTER_COLLECTION)
# создаем коллекцию для присваивания идентификаторов
counters.insert_many([{"name": "user_id", "sequence_value": 0}, {"name": "offer_id", "sequence_value": 0}])
users = get_collection(USER_COLLECTION)
offers = get_collection(OFFER_COLLECTION)
client = pymongo.MongoClient(DB_HOST, DB_PORT)
db = client[DB_NAME]
db.command({'collMod': 'users', 'validator': users_validator})
db.command({'collMod': 'offers', 'validator': offers_validator})
print("Done!")
