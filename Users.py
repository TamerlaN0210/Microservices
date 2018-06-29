import pymongo
from test import *
from sanic import Sanic
from sanic.response import json, text
from bson.objectid import ObjectId



client = pymongo.MongoClient()
db = client.test
users = db.users
print()

def validate_user(data_dictionary):
    # TODO сделать проверку на значения
    if len(data_dictionary) == 3:
        if "username" in data_dictionary and "password" in data_dictionary and "created_at" in data_dictionary:
            return True
    else:
        return False


def validate_auth(data_dictionary):
    # TODO сделать проверку на значения
    if len(data_dictionary) == 2:
        if "username" in data_dictionary and "password" in data_dictionary:
            return True
    else:
        return False


def does_user_exist(username):
    username = str(username)
    querry = users.find_one({"username": username})
    if querry is None:
        return False
    else:
        return True


app = Sanic(__name__)


@app.route("/user/registry/", methods=["POST"])
async def registry(request):
    if validate_user(request.json):
        username = request.json.get("username")
        if not does_user_exist(username):

            # копирую объект, т.к. при выполнении запроса к бд меняется request.json и сервер не работает
            querry = db.users.insert_one(copy.copy(request.json))
            if querry:
                return text(None, status=201)
            else:
                return text("Error while writing in data base")
        else:
            return text("Sorry, user with \"{}\" nickname already exist.".format(username))
    else:
        return text("JSON must have only this keys: username, password, created_at")


@app.route("/user/auth/", methods=["POST"])
async def authorization(request):
    if validate_auth(copy.copy(request.json)):
        querry = users.find_one(request.json)
        if querry is not None:
            return json({"id": str(querry.get("_id"))})
        else:
            return text(None, status=401)
    else:
        return text("JSON must only have this keys: username, password.", status=401)


@app.route("/user/<user_id>", methods=["GET"])
async def get_user(request, user_id):
    querry = users.find_one({"_id": ObjectId(user_id)}, {"password": 0})
    if querry is not None:
        querry["_id"] = str(querry["_id"])
        return json(querry)
    else:
        return text(None, status=401)


app.run(host="0.0.0.0", port=8000)
