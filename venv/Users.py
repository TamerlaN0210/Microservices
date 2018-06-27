import pymongo
import copy
from sanic import Sanic
from sanic.response import json, text
from json import dumps as jdumps
from json import  loads as jloads

client = pymongo.MongoClient()
db = client.test
users = db.users


def user_validation(data_dictionary):
    # TODO сделать проверку на значения
    if len(data_dictionary) == 3:
        if "username" in data_dictionary and "password" in data_dictionary and "created_at" in data_dictionary:
            return True
    return False


def does_user_exist(username):
    username = str(username)
    querry_result = users.find_one({"username": username})
    if querry_result is None:
        return False
    else:
        return True


app = Sanic(__name__)


@app.route("/user/registry/", methods=["POST"])
async def registry(request):
    if user_validation(request.json):
        username = request.json.get("username")
        if not does_user_exist(username):
            # копирую объект, т.к. при выполнении запроса к бд меняется request.json и сервер не работает
            query_result = db.users.insert_one(copy.copy(request.json))
            if query_result:
                return json({"Verification": user_validation(request.json), "json_queue": request.json}, status=201)
            else:
                return text("Error while writing in data base")
        else:
            return text("Sorry, user with \"{}\" nickname already exist.".format(username))
    else:
        return text("JSON must have only this keys: username, password, created_at")


@app.route("/user/<name>", methods=['POST'])
async def test(request, name):
    # data = users.find_one({"name": "{}".format(name)})
    return text('POST request - {}'.format(request.json))


@app.route("/user/<name>", methods=['GET'])
async def test(request, name):
    data = users.find_one({"name": "{}".format(request.json)})
    return text(str(data))

app.run(host="0.0.0.0", port=8000)
