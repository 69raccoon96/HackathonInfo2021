import json

from aiohttp import web
from aiohttp_security import (
    remember, forget, authorized_userid,
    check_permission, check_authorized,
)


class Admin(object):
    def __init__(self, user_repo, course_repo, subject_repo):
        self.user_repo = user_repo
        self.course_repo = course_repo
        self.subject_repo = subject_repo

    async def get_users(self, request):
        await check_permission(request, 'admin')
        request_data = dict(request.query)
        amount = request_data['amount'] if 'amount' in request_data else 100
        page = request_data['page'] if 'page' in request_data else 0
        lst = await self.user_repo.get_list(amount, page)
        for ls in lst['users']:
            ls['id'] = str(ls['_id'])
            ls.pop('_id', None)
        return web.Response(text=json.dumps(lst, ensure_ascii=False))

    async def get_courses(self, request):
        await check_permission(request, 'admin')
        request_data = dict(request.query)
        amount = request_data['amount'] if 'amount' in request_data else 100
        page = request_data['page'] if 'page' in request_data else 0
        lst = await self.course_repo.get_list(amount, page)
        for ls in lst['courses']:
            ls['id'] = str(ls['_id'])
            ls.pop('_id', None)
        return web.Response(text=json.dumps(lst, ensure_ascii=False))

    async def get_subjects(self, request):
        await check_permission(request, 'admin')
        request_data = dict(request.query)
        amount = request_data['amount'] if 'amount' in request_data else 100
        page = request_data['page'] if 'page' in request_data else 0
        lst = await self.subject_repo.get_list(amount, page)
        for ls in lst['subjects']:
            ls['id'] = str(ls['_id'])
            ls.pop('_id', None)
        return web.Response(text=json.dumps(lst, ensure_ascii=False))

    async def add_user(self, request):
        await check_permission(request, 'admin')
        json_obj = await request.json()
        await self.user_repo.add(json_obj)
        return web.HTTPCreated()

    async def add_course(self, request):
        await check_permission(request, 'admin')
        json_obj = await request.json()
        await self.course_repo.add(json_obj)
        return web.HTTPCreated()

    async def add_subject(self, request):
        await check_permission(request, 'admin')
        json_obj = await request.json()
        await self.subject_repo.add(json_obj)
        return web.HTTPCreated()

    async def delete_user(self, request):
        await check_permission(request, 'admin')
        json_obj = await request.json()
        await self.user_repo.remove(json_obj['id'])
        return web.HTTPNoContent()

    async def delete_course(self, request):
        await check_permission(request, 'admin')
        json_obj = await request.json()
        await self.course_repo.remove(json_obj['id'])
        return web.HTTPNoContent()

    async def delete_subject(self, request):
        await check_permission(request, 'admin')
        json_obj = await request.json()
        await self.subject_repo.remove(json_obj['id'])
        return web.HTTPNoContent()

    async def update_user(self, request):
        await check_permission(request, 'admin')
        json_obj = await request.json()
        idx = json_obj['id']
        json_obj.pop('id', None)
        await self.user_repo.update(idx, json_obj)
        return web.HTTPNoContent()

    async def update_course(self, request):
        await check_permission(request, 'admin')
        json_obj = await request.json()
        idx = json_obj['id']
        json_obj.pop('id', None)
        await self.course_repo.update(idx, json_obj)
        return web.HTTPNoContent()

    async def update_subject(self, request):
        await check_permission(request, 'admin')
        json_obj = await request.json()
        idx = json_obj['id']
        json_obj.pop('id', None)
        await self.subject_repo.update(idx, json_obj)
        return web.HTTPNoContent()

    def configure(self, app):
        router = app.router
        router.add_route('GET', '/api/admin/user', self.get_users, name='admin_get_user')
        router.add_route('GET', '/api/admin/course', self.get_courses, name='admin_get_course')
        router.add_route('GET', '/api/admin/subject', self.get_subjects, name='admin_get_subject')
        router.add_route('PUT', '/api/admin/user', self.add_user, name='admin_add_user')
        router.add_route('PUT', '/api/admin/course', self.add_course, name='admin_add_course')
        router.add_route('PUT', '/api/admin/subject', self.add_subject, name='admin_add_subject')
        router.add_route('DELETE', '/api/admin/user', self.delete_user, name='admin_delete_user')
        router.add_route('DELETE', '/api/admin/course', self.delete_course, name='admin_delete_course')
        router.add_route('DELETE', '/api/admin/subject', self.delete_subject, name='admin_delete_subject')
        router.add_route('PATCH', '/api/admin/user', self.update_user, name='admin_update_user')
        router.add_route('PATCH', '/api/admin/course', self.update_course, name='admin_update_course')
        router.add_route('PATCH', '/api/admin/subject', self.update_subject, name='admin_update_subject')
