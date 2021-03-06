import os
import json
import types

import aiohttp_cors

import pymongo
from aiohttp.web_middlewares import middleware
from aiohttp.web_urldispatcher import StaticResource
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from bson.objectid import ObjectId
import asyncio

import motor.motor_asyncio as aiomotor
from aiohttp_session_mongo import MongoStorage
from aiohttp import web
from aiohttp_session import setup, get_session, session_middleware, SimpleCookieStorage
from aiohttp_security import setup as setup_security, SessionIdentityPolicy, check_authorized

import logging

from admin.views import get_admin_routes
from auth.db import MongoUserRepository
from auth.db_auth import DBAuthorizationPolicy
from auth.views import Auth
#import dnspython
from infrastructure.session_storage.mymongostorage import MyMongoStorage

routes = web.RouteTableDef()
client = pymongo.MongoClient("mongodb+srv://admin:RTF4empion@cluster0.p8umr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
mydb = client["IOT"]
mycol = mydb["users"]

#mydict = { "name": "John", "address": "Highway 37" }
#myCursor = mycol.find({"name":"Ivan"})
#x = mycol.insert_one(mydict)


@middleware
async def cookie_header_middleware(request, handler):
    resp = await handler(request)
    return resp

@routes.get('/allcourses')
async def allcourses(request):
    all_courses = list(mydb['courses'].find({}))
    all_subjects = list(mydb['subjects'].find({}))
    res = {}
    for course in all_courses:
        needed_subjects = course['hard'] + course['soft']
        for sub in needed_subjects:
            for one_sub in all_subjects:
                print(sub)
                print(one_sub)
                if sub == one_sub['name']:
                    if course['name'] in res.keys():
                        res[course['name']].append([sub, one_sub['semesters']])
                    else:
                        res[course['name']] = [[sub, one_sub['semesters']]]
    return web.Response(text=json.dumps(res, ensure_ascii=False))

@routes.get('/percents')
async def percents(request):
    await check_authorized(request)
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
    await check_authorized(request)
    request_data = dict(request.query)
    course_data = list(mydb["subjects"].find({}))
    user_id = request_data['id']
    user_data = mydb["users"].find_one({"_id": ObjectId(user_id)})
    soft = []
    hard = []
    for element in user_data['soft']:
        for course in course_data:
            if element == course['name']:
                a = dict(course)
                a['id'] = str(a.pop('_id'))
                soft.append(a)
    for element in user_data['hard']:
        for course in course_data:
            if element == course['name']:
                a = dict(course)
                a['id'] = str(a.pop('_id'))
                hard.append(a)
    result = {}
    result['hard'] = hard
    result['soft'] = soft
    result['name'] = user_data['name']
    result['surname'] = user_data['surname']
    result['group'] = user_data['group']

    return web.Response(text=json.dumps(result, ensure_ascii=False))

@routes.get('/courseinfo')
async def courseinfo(request):
    await check_authorized(request)
    request_data = dict(request.query)
    course_id = request_data['id']
    course_data = mydb["courses"].find_one({"_id": ObjectId(course_id)})
    course_data['id'] = str(course_data.pop('_id'))
    return web.Response(text=json.dumps(course_data, ensure_ascii=False))

@routes.get('/addsubject')
async def addsubject(request):
    await check_authorized(request)
    request_data = dict(request.query)
    subject_id = request_data['idSubject']
    user_id = request_data['idUser']
    subject_data = mydb["subjects"].find_one({"_id": ObjectId(subject_id)})
    name = subject_data['name']
    t = subject_data['type']
    mydb["users"].update_one({'_id': ObjectId(user_id)}, {'$push': {t: name}}, upsert=True)
    return web.Response(text='completed')

def clean_up(courses):
    result = []
    for cuorse in courses:
        if cuorse not in result:
            result.append(cuorse)
    result2 = []
    for elem in result:
        if type(elem) != type("aaa"):
            for elem2 in elem:
                result2.append(elem2)
        else:
            result2.append(elem)
    return result2

@routes.get('/courseschoose')
async def courseschoose(request):
    user_percents = await get_percents(request)
    await check_authorized(request)
    course_data = list(mydb["subjects"].find({}))
    max = -1
    available_directions = []
    for elem in user_percents:
        if elem['percent'] > max:
            max = elem['percent']
    for elem in user_percents:
        if elem['percent'] == max:
            available_directions.append(elem['id'])
    colors = {}
    request_data = dict(request.query)
    user_id = request_data['id']
    user_data = mydb["users"].find_one({"_id": ObjectId(user_id)})
    print(user_data)
    user_semester: int = int(user_data['semester'])
    learned_courses = user_data['hard'] + user_data['soft']
    bad_courses = []
    good_courses_names = []
    for id in available_directions:
        bad_courses += mydb["courses"].find_one({"_id": ObjectId(id)})['bad']
        good_courses_names += mydb["courses"].find_one({"_id": ObjectId(id)})['hard'] + mydb["courses"].find_one({"_id": ObjectId(id)})['soft']
    bad_courses = clean_up(bad_courses)
    good_courses_names = clean_up(good_courses_names)
    normal_courses = []
    for subject in course_data:
        if subject['name'] not in good_courses_names and subject['name'] not in bad_courses:
            subject['id'] = str(subject.pop('_id'))
            if user_semester <= sorted(subject['semesters'])[-1]:
                normal_courses.append(subject)
    not_learned_coursed = []
    for course in good_courses_names:
        if course not in learned_courses:

            not_learned_coursed.append(course)
    good = []
    for gc in not_learned_coursed:
        for course in course_data:
            if gc == course['name']:
                if user_semester <= sorted(course['semesters'])[-1]:
                    course['id'] = str(course.pop('_id'))
                    good.append(course)
    colors['good'] = good
    colors['normal'] = normal_courses
    colors['semester'] = user_semester
    #print(bad_courses)
    #print(good_courses_names)
    #print([x['name'] for x in normal_courses])
    #print(not_learned_coursed)
    print(colors)
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
    storage = MyMongoStorage(session_collection, samesite='none', secure=True, max_age=max_age)
    app = web.Application(middlewares=[session_middleware(storage), cookie_header_middleware])
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",),
    })

    async def close_mongo():
        db.client.close()
    app.on_cleanup.append(close_mongo)
    app.user_repo = MongoUserRepository(db)
    policy = SessionIdentityPolicy()
    setup_security(app, policy, DBAuthorizationPolicy(app.user_repo))
    auth_handlers = Auth()
    auth_handlers.configure(app)
    app.add_routes(routes)
    app.add_routes(get_admin_routes())
    for route in list(app.router.routes()):
        if not isinstance(route.resource, StaticResource):
            cors.add(route)

    return app

port = os.getenv('PORT', 8081)
web.run_app(make_app(), port=port)


