import redis
import settings
import json
from datetime import datetime

__redis_client = redis.Redis(host=settings.REDIS_IP, port=settings.REDIS_PORT)


def get_task_list(pattern):
    # tasks = []
    for key in __redis_client.keys(f"{pattern}*"):
        yield json.loads(__redis_client.get(key).decode())
        # print(key.decode())
        # tasks.append(__redis_client.get(key).decode())
    # return tasks


def publish_task(chat_id, notify, cronexpr):
    channel = 'add-channel'
    tmstmp = datetime.today().timestamp()
    job_id = f'{chat_id}-{tmstmp}'
    data = json.dumps({'chat_id': chat_id,
                       'job_id': job_id,
                       'notify': notify,
                       'work': 1,
                       'cronexpr': cronexpr,
                       'datetime': tmstmp})

    result = __redis_client.publish(channel, data)
    print(result)


def delete_task(job_id):
    channel = 'delete-channel'
    data = json.dumps({'job_id': job_id})
    __redis_client.publish(channel, data)


def change_task():
    channel = 'change-channel'
    pass


def pause_task(job_id):
    channel = 'change-channel'
    data = json.dumps({'job_id': job_id, 'work': 0})
    __redis_client.publish(channel, data)