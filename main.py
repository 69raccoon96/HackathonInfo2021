import requests
from aiohttp import web
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
import json
#import dnspython


routes = web.RouteTableDef()
client = pymongo.MongoClient("mongodb+srv://admin:RTF4empion@cluster0.p8umr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
mydb = client["IOT"]
mycol = mydb["users"]

#mydict = { "name": "John", "address": "Highway 37" }
#myCursor = mycol.find({"name":"Ivan"})
#x = mycol.insert_one(mydict)

@routes.get('/percents')
async def procents(request):
    request_data = dict(request.query)
    user_id = request_data['id']
    user_info = mycol.find_one({"_id": ObjectId(user_id)})
    user_hard = user_info['hard']
    user_soft = user_info['soft']
    courses = list(mydb["courses"].find({}))
    procents_dict = {}
    for elem in courses:
        course_hard = elem['hard']
        dif = sum(1 for v in user_hard if v in course_hard)
        procents_dict[elem['name']] = round(dif / len(course_hard) * 100)
    result = []
    for elem in courses:
        dictionary = {'_id': elem['_id'], 'name': elem['name'], 'procent': procents_dict[elem['name']]}
        result.append(dictionary)
    return web.Response(text=str(result))



@routes.get('/')
async def hello(request):
    return web.Response(text="true")

app = web.Application()
app.add_routes(routes)

web.run_app(app)


