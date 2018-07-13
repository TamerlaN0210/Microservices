from support_files.functions import *
from sanic import Sanic
from sanic.response import json
from support_files.Offer import *


users = get_collection(USER_COLLECTION)
offers = get_collection(OFFER_COLLECTION)


app = Sanic(__name__)


@app.route("/offer/create/", methods=["POST"])
async def create_offer(request):
    offer = Offer(request.json)
    if offer.is_valid():
        querry = users.find_one({"id": offer.user_id})
        if querry is not None:
            request.json.update({"id": get_next_sequence_value("offer_id")})
            querry = offers.insert_one({"id": get_next_sequence_value("offer_id"),
                                        "user_id": offer.user_id,
                                        "title": offer.title,
                                        "text": offer.text,
                                        "created_at": offer.created_at})
            if querry:
                return json({None}, status=201)
            else:
                return json({"Error": "Error in data base."}, status=500)
        else:
            return json({"Error": "User with id: {} does not exist.".format(request.json.get("user_id"))})
    else:
        return json({"Error": "JSON must have only this keys: user_id, title, text, created_at."}, status=401)


@app.route("/offer/", methods=["POST"])
async def get_offer(request):
    if len(request.json) == 1:
        if "offer_id" in request.json and type(request.json["offer_id"]) is int:
            querry = offers.find_one({"id": request.json.get("offer_id")}, {"_id": 0})
            if querry is not None:
                return json(querry, status=201)
            else:
                return json(None)
        elif "user_id" in request.json and type(request.json["user_id"]) is int:
            querry = offers.find({"user_id": request.json.get("user_id")}, {"_id": 0})
            querry = cursor_to_dict(querry)
            response = dict()
            if querry is not None:
                for key, elem in querry.items():
                    response.update({key: elem})
                return json(response, status=201)
            else:
                return json(None)
        else:
            return json({"Error": "Uncorrect JSON key."})
    else:
        return json({"Error": "JSON must have only one key, user_id or offer_id"})

app.run(host=SANIC_HOST, port=SANIC_PORT)
