from functions import *
from sanic import Sanic
from sanic.response import json, text

app = Sanic(__name__)


@app.route("/offer/create/", methods=["POST"])
async def create_offer(request):
    if validate_offer(request.json):
        users = get_collection("users")
        offers = get_collection("offers")
        # если польователь с данным id существует, тогда проводим запись
        querry = users.find_one({"id": request.json.get("user_id")})
        if querry is not None:
            request.json.update({"id": get_next_sequence_value("offer_id")})
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
        if "offer_id" in request.json and type(request.json["offer_id"]) is int:
            offers = get_collection("offers")
            querry = offers.find_one({"id": request.json.get("offer_id")})
            if querry is not None:
                querry["_id"] = "ObjectID(" + str(querry["_id"]) + ")"
                querry["user_id"] = querry["user_id"]
                return json(querry, status=201)
            else:
                return json(None)
        elif "user_id" in request.json and type(request.json["user_id"]) is int:
            offers = get_collection("offers")
            querry = offers.find({"user_id": request.json.get("user_id")})
            querry = cursor_to_dict(querry)
            response = dict()
            if querry is not None:
                for key, elem in querry.items():
                    response.update({key: elem})
                    response[key]['_id'] = "ObjectId(" +str(elem['_id'])+ ")"
                return json(response, status=201)
            else:
                return json(None)
        else:
            return text("Uncorrect JSON key.")
    else:
        return text("JSON must have only one key, user_id or offer_id")

app.run(host=SANIC_HOST, port=SANIC_PORT)