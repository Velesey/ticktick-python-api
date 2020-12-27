import json
import urllib
from datetime import datetime, timedelta

import httplib2
from pprint import pprint

import pytz

from task import Task, TaskStatus
from client import Client

from task_service import TaskService

USER = "velesey@gmail.com"
PASSWORD = "TickTickTock1!"

client = Client()
connected = client.connect(USER, PASSWORD)
if connected:
    tasks = TaskService(client)
    start = pytz.utc.localize(datetime.utcnow()) + timedelta(minutes=2)
    due = pytz.utc.localize(datetime.utcnow()) + timedelta(days=2)

    # tasks.add("5fe749928f08d95ef8a75b76", "some texfedf ofds f", 'Описание', start, due, 5)
    result = tasks.get_by_project('5fe749928f08d95ef8a75b76')
    # for r in result:
    #     print(r)
    # result[0].status = TaskStatus.ACTIVE
    # result[0].title = "new title"
    # result[0].priority = 5
    # result[0].start_date = start
    # result[0].due_date = due

    tasks.delete(result[0].id, result[0].project_id)
    # response, content = client.get(
    #     'https://api.ticktick.com/api/v2/project/5fe749928f08d95ef8a75b76/tasks')
