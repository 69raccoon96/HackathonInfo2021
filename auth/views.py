import json

from aiohttp import web

from aiohttp_security import (
    remember, forget, authorized_userid,
    check_permission, check_authorized,
)

from auth.db_auth import check_credentials


class Auth(object):
    async def login(self, request):
        json_data = await request.json()
        username = json_data['login']
        password = json_data['password']
        user_repo = request.app.user_repo
        if await check_credentials(user_repo, username, password):
            user = await user_repo.get_user_by_username(username)
            user_dto = vars(user)
            user_dto.pop('password', None)
            user_dto['id'] = user_dto.pop('_id')
            response = web.Response(text=json.dumps(user_dto, ensure_ascii=False))
            await remember(request, response, username)
            return response
        else:
            raise web.HTTPUnauthorized()

    async def logout(self, request):
        await check_authorized(request)
        response = web.Response()
        await forget(request, response)
        return response

    async def update_session(self, request):
        await check_authorized(request)
        response = web.Response()
        user_id = authorized_userid(request)
        await forget(request, response)
        await remember(request, response, user_id)
        return response

    def configure(self, app):
        router = app.router
        router.add_route('POST', '/login', self.login, name='login')
        router.add_route('POST', '/logout', self.logout, name='logout')
        router.add_route('PATCH', '/session', self.update_session, name='update_session')