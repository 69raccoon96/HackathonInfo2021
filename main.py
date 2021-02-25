import requests
from aiohttp import web
import pymongo
#import dnspython

routes = web.RouteTableDef()
client = pymongo.MongoClient("mongodb+srv://admin:RTF4empion@cluster0.p8umr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.IOT
mydb = client["IOT"]
mycol = mydb["users"]

#mydict = { "name": "John", "address": "Highway 37" }
#myCursor = mycol.find({"name":"Ivan"})
#x = mycol.insert_one(mydict)

@routes.get('/auth')
async def hello(request):
    username = request.query['username']
    password = request.query['password']
    usernameDB = list(mycol.find({"username": username}))
    if len(usernameDB) == 0:
        return web.Response(text="Not found")
    first = usernameDB[0]
    if password == first["password"]:
        return web.Response(text="True")
    return web.Response(text="False")


@routes.get('/')
async def hello(request):
    return web.Response(text="true")

app = web.Application()
app.add_routes(routes)

web.run_app(app)


