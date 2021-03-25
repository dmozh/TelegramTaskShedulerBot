from aiohttp import web
import json
from network import send_request, TypeRequest
import settings as crs
from app import redis_connector
import logger

pool = {}


async def action(request):
    msg_object = await request.json()
    logger.info_logger.info(logger.generate_message(f"Action is start", f"{json.dumps(msg_object)}"))
    response_msg = {'msg': 'Action is start', 'method': 'post-action'}

    if 'edited_message' in msg_object:
        await __edited_message(msg_object)
    elif 'callback_query' in msg_object:
        await __callback_query(msg_object)
    else:
        await __message(msg_object)
    # return web.Response(text='dd')
    return web.json_response(response_msg)


async def __message(msg_object):
    _msg_action = msg_object['message']
    # print(_msg_action)
    chat_id = _msg_action['chat']['id']
    inner_msg_text = _msg_action['text']
    if inner_msg_text == '/start':
        params = {'chat_id': chat_id, 'text': 'Hello guest'}
    elif inner_msg_text == '/newtask':
        logger.info_logger.info(logger.generate_message(f"New task command is start", f"{json.dumps(_msg_action)}"))
        pool[chat_id] = {"chat_id": chat_id, "action": "newtask"}
        params = {'chat_id': chat_id, 'text': f'If you would like add new notify, '
                                              f'you need point out cron expression for schedule and notify msg\n'
                                              f'Rules for cron expression:\n'
                                              f"*    *    *      *     *      *\n"
                                              f"sec  min  hours  days  month  years\n"
                                              f"* - every time, every second, every day, etc\n"
                                              f"0 - specific time\n"
                                              f"0/15 - every any time from start example every 15 minute from start 0\n"
                                              f"MON,TUE,WED,THU,FRI,SAT,SUN - specific week days\n"
                                              f"For example: 0 0 14 MON,TUE,WED * * - for every month in "
                                              f"monday, tuesday and wednesday in 14:00am you get notify",
                  'reply_markup': {
                      'inline_keyboard': [
                          [{'text': 'Ok', "callback_data": 'OK'}]
                      ]}
                  }
    elif '/deletetask' in inner_msg_text:
        logger.info_logger.info(logger.generate_message(f"Delete task command is start", f"{json.dumps(_msg_action)}"))
        try:
            tid = inner_msg_text.split(' ')[1]
            redis_connector.delete_task(tid)
            text = f'Deleted {tid}'
        except Exception:
            text = "123"
        params = {'chat_id': chat_id, 'text': text}
    elif '/pausetask' in inner_msg_text:
        logger.info_logger.info(logger.generate_message(f"Pause task command is start", f"{json.dumps(_msg_action)}"))
        try:
            tid = inner_msg_text.split(' ')[1]
            redis_connector.pause_task(tid)
            text = f'Paused {tid}'
        except Exception:
            text = "123"
        params = {'chat_id': chat_id, 'text': text}
    elif inner_msg_text == '/changetask':
        logger.info_logger.info(logger.generate_message(f"Change task command is start", f"{json.dumps(_msg_action)}"))
        params = {'chat_id': chat_id, 'text': '123'}
    elif inner_msg_text == '/taskslist':
        logger.info_logger.info(logger.generate_message(f"Task list command is start", f"{json.dumps(_msg_action)}"))
        tasks = redis_connector.get_task_list(chat_id)
        text = "Your tasks:\n"
        for task in tasks:
            text += f"job_id: {task['job_id']}, cron expression: {task['cronexpr']}, notify: {task['notify']}\n"
        params = {'chat_id': chat_id, 'text': text}
    elif inner_msg_text == '/commands':
        logger.info_logger.info(logger.generate_message(f"Commands list command is start", f"{json.dumps(_msg_action)}"))
        text = "Commands list:\n" \
               "/newtask - add new notify task\n" \
               "/taskslist - show all your tasks\n" \
               "/deletetask - delete entered your task\n" \
               "/changetask - change entered your task\n" \
               "/pausetask - chanfe entered your task\n"
        params = {'chat_id': chat_id, 'text': text}
    else:
        logger.info_logger.info(logger.generate_message(f"Send commands list", f"{json.dumps(_msg_action)}"))
        text = '/commands'
        params = {'chat_id': chat_id, 'text': text}
        if chat_id in pool:
            if not pool[chat_id]['have_notify']:
                pool[chat_id]['notify'] = inner_msg_text
                pool[chat_id]['have_notify'] = True
                text = 'Enter schedule use cron expression'
            elif not pool[chat_id]['have_cron']:
                pool[chat_id]['cron'] = inner_msg_text
                pool[chat_id]['have_cron'] = True
            if pool[chat_id]['have_cron'] and pool[chat_id]['have_notify']:
                text = f"Your notify msg: {pool[chat_id]['notify']}\n" \
                       f"Your schedule: {pool[chat_id]['cron']}\n" \
                       f"All right?"
                params['reply_markup'] = {
                    'inline_keyboard': [
                        [{'text': 'Yes =)', "callback_data": 'allright|yes'},
                         {'text': 'No ;(', "callback_data": 'allright|no'}]
                    ]}
            params['text'] = text

    await __send_msg(params)


async def __edited_message(msg_object):
    msg_action = msg_object['edited_message']
    # print(msg_action)
    pass


async def __callback_query(msg_object):
    _msg_action = msg_object['callback_query']
    # print(_msg_action)
    chat_id = _msg_action['message']['chat']['id']
    params = {'chat_id': chat_id}
    if _msg_action['data'] == "OK":
        params['text'] = 'Great! Then we starting\n' \
                         'Please enter what you would like notify to myself'
        pool[chat_id]['have_notify'] = False
        pool[chat_id]['have_cron'] = False
    elif 'allright' in _msg_action['data']:
        if _msg_action['data'].split('|')[1].lower() == 'yes':
            params['text'] = 'Success! You add new notify task\n'
            redis_connector.publish_task(chat_id=chat_id,
                                         notify=pool[chat_id]['notify'],
                                         cronexpr=pool[chat_id]['cron'])
            del pool[chat_id]
        else:
            params['text'] = 'Ok, would you like start over?\n'
            params['reply_markup'] = {
                'inline_keyboard': [
                    [{'text': 'Yes', "callback_data": 'startover|yes'},
                     {'text': 'No', "callback_data": 'startover|no'}]
                ]}
    elif 'startover' in _msg_action['data']:
        if _msg_action['data'].split('|')[1].lower() == 'yes':
            params['text'] = 'Nice^^\nPlease enter what you would like notify to myself'
            pool[chat_id]['have_notify'] = False
            pool[chat_id]['have_cron'] = False
        else:
            params['text'] = 'Ok, i hope we see you soon ;)\n'
            del pool[chat_id]
    else:
        params = {'chat_id': chat_id, 'text': '/commands'}

    await __send_msg(params)


async def __send_msg(params):
    logger.info_logger.info(logger.generate_message(f"Send msg", f"{json.dumps(params)}"))
    send_request(host=f"{crs.BASE_URL}{crs.API_TOKEN}",
                 api_url="/sendMessage",
                 request_type=TypeRequest.POST,
                 body=params)
