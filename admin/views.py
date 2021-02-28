import json

from aiohttp import web
import aiohttp_cors
from aiohttp_security import (
    remember, forget, authorized_userid,
    check_permission, check_authorized,
)

routes = web.RouteTableDef()


@routes.view('/api/admin/user')
class AdminUserView(web.View, aiohttp_cors.CorsViewMixin):
    def __init__(self, request):
        super().__init__(request)
        self.user_repo = request.app.admin_user_repo

    async def put(self):
        await check_permission(self.request, 'admin')
        json_obj = await self.request.json()
        await self.user_repo.add(json_obj)
        return web.HTTPCreated()

    async def get(self):
        await check_permission(self.request, 'admin')
        request_data = dict(self.request.query)
        amount = request_data['amount'] if 'amount' in request_data else 100
        page = request_data['page'] if 'page' in request_data else 0
        lst = await self.user_repo.get_list(amount, page)
        for ls in lst['users']:
            ls['id'] = str(ls['_id'])
            ls.pop('_id', None)
        return web.Response(text=json.dumps(lst, ensure_ascii=False))

    async def delete(self):
        await check_permission(self.request, 'admin')
        json_obj = await self.request.json()
        await self.user_repo.remove(json_obj['id'])
        return web.HTTPNoContent()

    async def patch(self):
        await check_permission(self.request, 'admin')
        json_obj = await self.request.json()
        idx = json_obj['id']
        json_obj.pop('id', None)
        await self.user_repo.update(idx, json_obj)
        return web.HTTPNoContent()


@routes.view('/api/admin/subject')
class SubjectView(web.View, aiohttp_cors.CorsViewMixin):
    def __init__(self, request):
        super().__init__(request)
        self.subject_repo = request.app.admin_subject_repo

    async def put(self):
        await check_permission(self.request, 'admin')
        json_obj = await self.request.json()
        await self.subject_repo.add(json_obj)
        return web.HTTPCreated()

    async def get(self):
        await check_permission(self.request, 'admin')
        request_data = dict(self.request.query)
        amount = request_data['amount'] if 'amount' in request_data else 100
        page = request_data['page'] if 'page' in request_data else 0
        lst = await self.subject_repo.get_list(amount, page)
        for ls in lst['subjects']:
            ls['id'] = str(ls['_id'])
            ls.pop('_id', None)
        return web.Response(text=json.dumps(lst, ensure_ascii=False))

    async def delete(self):
        await check_permission(self.request, 'admin')
        json_obj = await self.request.json()
        await self.subject_repo.remove(json_obj['id'])
        return web.HTTPNoContent()

    async def patch(self):
        await check_permission(self.request, 'admin')
        json_obj = await self.request.json()
        idx = json_obj['id']
        json_obj.pop('id', None)
        await self.subject_repo.update(idx, json_obj)
        return web.HTTPNoContent()


@routes.view('/api/admin/course')
class CourseView(web.View, aiohttp_cors.CorsViewMixin):
    def __init__(self, request):
        super().__init__(request)
        self.course_repo = request.app.admin_course_repo

    async def put(self):
        await check_permission(self.request, 'admin')
        json_obj = await self.request.json()
        await self.course_repo.add(json_obj)
        return web.HTTPCreated()

    async def get(self):
        await check_permission(self.request, 'admin')
        request_data = dict(self.request.query)
        amount = request_data['amount'] if 'amount' in request_data else 100
        page = request_data['page'] if 'page' in request_data else 0
        lst = await self.course_repo.get_list(amount, page)
        for ls in lst['courses']:
            ls['id'] = str(ls['_id'])
            ls.pop('_id', None)
        return web.Response(text=json.dumps(lst, ensure_ascii=False))

    async def delete(self):
        await check_permission(self.request, 'admin')
        json_obj = await self.request.json()
        await self.course_repo.remove(json_obj['id'])
        return web.HTTPNoContent()

    async def patch(self):
        await check_permission(self.request, 'admin')
        json_obj = await self.request.json()
        idx = json_obj['id']
        json_obj.pop('id', None)
        await self.course_repo.update(idx, json_obj)
        return web.HTTPNoContent()


def get_admin_routes():
    return routes
