import requests
from aiohttp import web
import pymongo
#import dnspython

routes = web.RouteTableDef()
client = pymongo.MongoClient("mongodb+srv://admin:RTF4empion@cluster0.p8umr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.test
mydb = client["mydatabase"]
mycol = mydb["customers"]

mydict = { "name": "John", "address": "Highway 37" }

#x = mycol.insert_one(mydict)

@routes.get('/')
async def hello(request):
    name = request.query['name']
    txt = "Hello, {}".format(name)
    return web.Response(text=txt)

app = web.Application()
app.add_routes(routes)

web.run_app(app)