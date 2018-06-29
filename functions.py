import pymongo
from config import *


def get_collection(collection_name: str):
    client = pymongo.MongoClient(DB_HOST, DB_PORT)
    db = client[DB_NAME]
    collection = db[collection_name]
    return collection


def validate_user(user_data):
    # TODO сделать проверку на значения
    if len(user_data) == 3:
        if "username" in user_data and "password" in user_data and "created_at" in user_data:
            return True
    else:
        return False


def validate_auth(auth_data: dict):
    # TODO сделать проверку на значения
    if len(auth_data) == 2:
        if "username" in auth_data and "password" in auth_data:
            return True
    else:
        return False


def does_user_exist(username: str):
    username = str(username)
    users = get_collection("users")
    querry = users.find_one({"username": username})
    if querry is None:
        return False
    else:
        return True

def cursor_to_dict(cursor):
    dict_ = {}
    i = 0
    for elem in cursor:
        dict_.update({i: elem})
        i += 1
    return dict_


def validate_offer(offer_dictionary):
    if len(offer_dictionary) == 4:
        if "user_id" in offer_dictionary and "title" in offer_dictionary and\
                "text" in offer_dictionary and "created_at" in offer_dictionary:
            return True
        else:
            return False
    else:
        return False
