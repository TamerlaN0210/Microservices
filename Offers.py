from functions import *
from sanic import Sanic
from sanic.response import json, text
from bson.objectid import ObjectId

app = Sanic(__name__)


@app.route("/offer/create/", methods=["POST"])
async def create_offer(request):
    if validate_offer(request.json):
        users = get_collection("users")
        offers = get_collection("offers")
        # если польователь с данным id существует, тогда проводим запись
        querry = users.find_one({"_id": ObjectId(request.json.get("user_id"))})
        if querry is not None:
            request.json['user_id'] = ObjectId(request.json['user_id'])
            querry = offers.insert_one(request.json)
            if querry:
                return text(None, status=201)
            else:
                return text("Error in data base.", status=500)
        else:
            return text("User with id: {} does not exist.".format(request.json.get("user_id")))
    else:
        return text("JSON must have only this keys: user_id, title, text, created_at.", status=401)


@app.route("/offer/", methods=["POST"])
async def get_offer(request):
    if len(request.json) == 1:
        if "offer_id" in request.json:
            offers = get_collection("offers")
            querry = offers.find_one({"_id": ObjectId(request.json.get("offer_id"))})
            if querry is not None:
                querry["_id"] = "ObjectID(" + str(querry["_id"]) + ")"
                querry["user_id"] = "ObjectID(" + str(querry["user_id"]) + ")"
                return json(querry, status=201)
            else:
                return json(None)
        elif "user_id" in request.json:
            offers = get_collection("offers")
            querry = offers.find({"user_id": ObjectId(request.json.get("user_id"))})
            print(cursor_to_dict(querry))
            if querry is not None:
                for elem in querry:
                    elem["_id"] = "ObjectID(" + str(elem["_id"]) + ")"
                    elem["user_id"] = "ObjectID(" + str(elem["user_id"]) + ")"
                return json(querry, status=201)
            else:
                return json(None)
    else:
        return text("JSON must have only one key, user_id or offer_id")

app.run(host="0.0.0.0", port=8000)