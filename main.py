import requests
from aiohttp import web

routes = web.RouteTableDef()

@routes.get('/')
async def hello(request):
    name = request.query['name']
    txt = "Hello, {}".format(name)
    return web.Response(text=txt)

app = web.Application()
app.add_routes(routes)
web.run_app(app)