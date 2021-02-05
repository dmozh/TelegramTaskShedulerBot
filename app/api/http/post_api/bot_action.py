from app.sql.sql_handler import sql_exec as handle
from aiohttp import web
import json
from network import send_request, TypeRequest
import credentials as crs
import requests


async def action(request):
    msg_object = await request.json()
    print(json.dumps(msg_object))
    # print(**msg_object)
    if 'message' in msg_object:
        msg_action = msg_object['message']
    elif 'edited_message' in msg_object:
        msg_action = msg_object['edited_message']
    elif 'callback_query' in msg_object:
        msg_action = msg_object['callback_query']
        print('fff')
    else:
        msg_action = msg_object['message']
    print(msg_action)
    chat_id = msg_action['chat']['id']
    print(chat_id)
    params = {'chat_id': chat_id, 'text': f'Hello guest',
              'reply_markup': {
                  'inline_keyboard': [
                      [{'text': 'test', "callback_data": 'test'}]
                  ]
              }}

    r = send_request(host=f"{crs.BASE_URL}{crs.API_TOKEN}",
                     api_url="/sendMessage",
                     request_type=TypeRequest.POST,
                     body=params)
    # print(r)
    # requests.post(url, headers=None, json=params)
    return web.Response(text='dd')


async def __message():
    pass


async def __edited_message():
    pass


async def __callback_query():
    pass
