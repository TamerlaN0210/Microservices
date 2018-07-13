from support_files.functions import *
from sanic import Sanic
from sanic.response import json
from support_files.User import *


users = get_collection(USER_COLLECTION)


app = Sanic(__name__)


@app.route("/user/registry/", methods=["POST"])
async def registry(request):
    user = User(request.json)
    if not does_user_exist(user.username, users):
        if user.is_valid_for_registry():
            querry = users.insert_one({"username": user.username,
                                       "password": user.get_hashed_password(),
                                       "created_at": user.created_at,
                                       "id": get_next_sequence_value("user_id")})
            if querry:
                return json({}, status=201)
            else:
                return json({"Error": "Error while writing in data base"})
        else:
            return json({"Error": "JSON must have only this keys: username, password, created_at"})
    else:
        return json({"Error": "Sorry, user with \"{}\" nickname already exist.".format(user.username)})


@app.route("/user/auth/", methods=["POST"])
async def authorization(request):
    user = User(request.json)
    if user.is_valid_for_auth():
        querry = users.find_one({"username": user.username, "password": user.get_hashed_password()})
        if querry is not None:
            return json({"id": int(querry.get("id"))}, status=201)
        else:
            return json({None}, status=401)
    else:
        return json({"Error": "JSON must only have this keys: username, password."}, status=401)


@app.route("/user/<user_id>", methods=["GET"])
async def get_user(request, user_id):
    querry = users.find_one({"id": int(user_id)}, {"_id": 0, "password": 0})
    if querry is not None:
        return json(querry)
    else:
        return json({None}, status=401)


app.run(host=SANIC_HOST, port=SANIC_PORT)
