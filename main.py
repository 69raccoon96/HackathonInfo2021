import requests
from aiohttp import web
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
import json
import asyncio

import motor.motor_asyncio as aiomotor
from aiohttp_session_mongo import MongoStorage
from aiohttp import web
from aiohttp_session import setup, get_session, session_middleware, SimpleCookieStorage
from aiohttp_security import setup as setup_security, SessionIdentityPolicy

import logging

from auth.db import MongoUserRepository
from auth.db_auth import DBAuthorizationPolicy
from auth.views import Auth
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

async def init_mongo(loop):
    url = "mongodb+srv://admin:RTF4empion@cluster0.p8umr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    conn = aiomotor.AsyncIOMotorClient(
        url, maxPoolSize=2, io_loop=loop)
    db = 'IOT'
    return conn[db]

async def setup_mongo(loop):
    db = await init_mongo(loop)
    return db

@routes.get('/')
async def hello(request):
    return web.Response(text="true")

async def make_app():
    max_age = 3600 * 24 * 365
    loop = asyncio.get_event_loop()
    db = await setup_mongo(loop)
    session_collection = db['sessions']
    middleware = session_middleware(MongoStorage(session_collection, max_age=max_age))

    app = web.Application(middlewares=[middleware])

    async def close_mongo():
        db.client.close()
    app.on_cleanup.append(close_mongo)

    app.user_repo = MongoUserRepository(db)
    policy = SessionIdentityPolicy()
    setup_security(app, policy, DBAuthorizationPolicy(app.user_repo))
    auth_handlers = Auth()
    auth_handlers.configure(app)
    app.add_routes(routes)
    return app
web.run_app(make_app())


