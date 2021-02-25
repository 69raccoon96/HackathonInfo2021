import json

import pymongo
from bson.objectid import ObjectId
import asyncio

import motor.motor_asyncio as aiomotor
from aiohttp_session_mongo import MongoStorage
from aiohttp import web
from aiohttp_session import setup, get_session, session_middleware, SimpleCookieStorage
from aiohttp_security import setup as setup_security, SessionIdentityPolicy, check_authorized

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
async def percents(request):
    #await check_authorized(request)
    result = await get_percents(request)
    return web.Response(text=json.dumps(result, ensure_ascii=False))

async def get_percents(request):
    request_data = dict(request.query)
    user_id = request_data['id']
    user_info = mycol.find_one({"_id": ObjectId(user_id)})
    user_hard = user_info['hard']
    user_soft = user_info['soft']
    courses = list(mydb["courses"].find({}))
    procents_dict = {}
    for elem in courses:
        course_hard = elem['hard']
        course_soft = elem['soft']
        dif = sum(1 for v in user_hard if v in course_hard)
        dif2 = sum(1 for v in user_soft if v in course_hard)
        procents_dict[elem['name']] = round((dif + dif2) / (len(course_hard) + len(course_soft)) * 100)
    result = []
    for elem in courses:
        dictionary = {'id': str(elem['_id']), 'name': elem['name'], 'percent': procents_dict[elem['name']], "hard": elem["hard"], "soft": elem["soft"]}
        result.append(dictionary)
    return result


@routes.get('/profile')
async def profile(request):
    #await check_authorized(request)
    request_data = dict(request.query)

    user_id = request_data['id']
    user_data = mydb["users"].find_one({"_id": ObjectId(user_id)})
    result = {}
    result['hard'] = user_data['hard']
    result['soft'] = user_data['soft']
    result['name'] = user_data['name']
    result['surname'] = user_data['surname']
    result['group'] = user_data['group']
    return web.Response(text=json.dumps(result, ensure_ascii=False))

@routes.get('/courseinfo')
async def courseinfo(request):
    #await check_authorized(request)
    request_data = dict(request.query)
    course_id = request_data['id']
    course_data = mydb["courses"].find_one({"_id": ObjectId(course_id)})
    course_data['id'] = str(course_data.pop('_id'))
    return web.Response(text=json.dumps(course_data, ensure_ascii=False))

@routes.get('/courseschoose')
async def courseschoose(request):
    user_percents = await get_percents(request)
    #await check_authorized(request)
    course_data = list(mydb["subjects"].find({}))
    result = {}
    for i in range(1, 9):
        for course in course_data:
            if i in course['semesters']:
                if i in result.keys():
                    temp = dict(course)
                    temp.pop('semesters')
                    #temp.pop('_id')
                    result[i].append(temp)
                else:
                    result[i] = []
                    temp = dict(course)
                    temp.pop('semesters')
                    #temp.pop('_id')
                    result[i].append(temp)
    max = -1
    res = []
    for elem in user_percents:
        if elem['percent'] > max:
            max = elem['percent']
    for elem in user_percents:
        if elem['percent'] == max:
            res.append(elem)
    colors = {}
    request_data = dict(request.query)
    user_id = request_data['id']
    user_data = mydb["users"].find_one({"_id": ObjectId(user_id)})
    good_courses = []
    for elem in course_data:
        for elem2 in res:
            if elem['name'] in elem2['hard'] and elem not in good_courses and elem['name'] not in user_data['hard']:
                good_courses.append(elem)
    for course in good_courses:
        course['id'] = str(course.pop('_id'))
    colors['good'] = good_courses
    return web.Response(text=json.dumps(colors, ensure_ascii=False))

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


