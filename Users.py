from functions import *
import copy
from sanic import Sanic
from sanic.response import json, text
from bson.objectid import ObjectId


app = Sanic(__name__)


@app.route("/user/registry/", methods=["POST"])
async def registry(request):
    if validate_user(request.json):
        username = request.json.get("username")
        if not does_user_exist(username):
            users = get_collection("users")
            # copying request.json, because "insertOne" adding field "_id" to request.json. I don't need that.
            querry = users.insert_one(copy.copy(request.json))
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
        users = get_collection("users")
        querry = users.find_one(request.json)
        if querry is not None:
            return json({"id": str(querry.get("_id"))})
        else:
            return text(None, status=401)
    else:
        return text("JSON must only have this keys: username, password.", status=401)


@app.route("/user/<user_id>", methods=["GET"])
async def get_user(request, user_id):
    users = get_collection("users")
    querry = users.find_one({"_id": ObjectId(user_id)}, {"password": 0})
    if querry is not None:
        querry["_id"] = str(querry["_id"])
        return json(querry)
    else:
        return text(None, status=401)


app.run(host=SANIC_HOST, port=SANIC_PORT)
