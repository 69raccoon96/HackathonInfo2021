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

log = logging.getLogger(__name__)


async def init_mongo(loop):
    url = "mongodb+srv://admin:RTF4empion@cluster0.p8umr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    conn = aiomotor.AsyncIOMotorClient(
        url, maxPoolSize=2, io_loop=loop)
    db = 'IOT'
    return conn[db]


async def setup_mongo(loop):
    db = await init_mongo(loop)
    return db


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

    return app


if __name__ == '__main__':
    web.run_app(make_app())