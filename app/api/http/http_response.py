from app.sql.sql_handler import sql_exec as handle
from aiohttp import web
import json


async def test(request):
    # print(request.method)
    # print(request.headers['Origin'])
    # acao = request.headers['Origin'] if request.headers['Origin'] is not None else ''
    # headers = {'Access-Control-Allow-Credentials': 'true', 'Access-Control-Allow-Origin': acao}
    response = f'<div>test</div>'
    print('ddd')
    return web.Response(body=response)
