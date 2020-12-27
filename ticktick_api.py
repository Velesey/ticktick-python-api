from client import Client
from service.task_service import TaskService


class TickTickAPI:
    _user_name: str
    _password: str
    _client: Client
    _tasks: TaskService

    def __init__(self, user_name: str, password: str):
        self._user_name = user_name
        self._password = password
        self._client = Client(user_name, password)
        self._tasks = TaskService(self._client)

    def connect(self) -> bool:
        return self._client.connect(self._user_name, self._password)

    def tasks(self):
        return self._tasks;
