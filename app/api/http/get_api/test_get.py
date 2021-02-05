from app.sql.sql_handler import sql_exec as handle
from aiohttp import web
import json
from network import send_request, TypeRequest


async def test_json(request):
    print(request)
    # headers = {'Access-Control-Allow-Credentials': 'true', 'Access-Control-Allow-Origin': request.headers['Origin']}
    if request.method == 'GET':
        response_msg = {'msg': 'test', 'method': 'get'}
        return web.json_response(response_msg)
