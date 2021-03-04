from aiohttp import web


async def test_json(request):
    # headers = {'Access-Control-Allow-Credentials': 'true', 'Access-Control-Allow-Origin': request.headers['Origin']}
    if request.method == 'POST':
        response_msg = {}

        response_msg['msg'] = 'test'
        response_msg['method'] = 'post'
        return web.json_response(response_msg)
