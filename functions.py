import pymongo
from config import *


def get_collection(collection_name: str):
    client = pymongo.MongoClient(DB_HOST, DB_PORT)
    db = client[DB_NAME]
    collection = db[collection_name]
    return collection


def get_next_sequence_value(sequence_name: str) -> int:
    counter = get_collection("counter")
    querry = counter.find_one({"_id": sequence_name})
    sequence_value = int(querry.get("sequence_value")) + 1
    counter.update({'_id': sequence_name}, {"sequence_value": sequence_value})
    return sequence_value


def validate_user(user_data: dict) -> bool:
    if len(user_data) == 3:
        if "username" in user_data and type(user_data.get("username")) is str and\
                "password" in user_data and type(user_data.get("password")) is str and\
                "created_at" in user_data and type(user_data.get("created_at")) is int:
            return True
        else:
            return False
    else:
        return False


def validate_auth(auth_data: dict) -> bool:
    if len(auth_data) == 2:
        if "username" in auth_data and type(auth_data.get("username")) is str and\
                "password" in auth_data and type(auth_data.get("password")) is str:
            return True
        else:
            return False
    else:
        return False


def does_user_exist(username: str) -> bool:
    username = str(username)
    users = get_collection("users")
    querry = users.find_one({"username": username})
    if querry is None:
        return False
    else:
        return True


def cursor_to_dict(cursor_) -> dict:
    dict_ = dict()
    i = 0
    for elem in cursor_:
        dict_.update({i: elem})
        i += 1
    return dict_


def validate_offer(offer_dictionary: dict) -> bool:
    if len(offer_dictionary) == 4:
        if "user_id" in offer_dictionary and type(offer_dictionary.get("user_id")) is int and\
                "title" in offer_dictionary and type(offer_dictionary.get("title")) is str and\
                "text" in offer_dictionary and type(offer_dictionary.get("text")) is str and\
                "created_at" in offer_dictionary and type(offer_dictionary.get("created_at")) is int:
            return True
        else:
            return False
    else:
        return False
