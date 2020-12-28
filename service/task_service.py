import json
from datetime import datetime, timezone
from typing import List, Optional
from client import Client
from service.service import Service
from model.task import TaskStatus, Task

DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%f%z'


class TaskService(Service):
    def __init__(self, client: Client):
        self.client = client

    def get_all(self) -> List[Task]:
        result = []
        url = f"https://api.ticktick.com/api/v2/project/all/tasks"
        response, content = self.client.get(url)
        if self.check_authorization_and_reconnect('get_all', response, content):
            jsn = json.loads(content)
            for c in jsn:
                result.append(self._build_task(c))

        return result

    def get_by_project(self, project_id: str) -> List[Task]:
        result = []
        url = f"https://api.ticktick.com/api/v2/project/{project_id}/tasks"
        response, content = self.client.get(url)
        if self.check_authorization_and_reconnect('get_by_project', response, content):
            jsn = json.loads(content)
            for c in jsn:
                result.append(self._build_task(c))

        return result

    def add(self, project_id: str, title: str, content: str, start_date: Optional[datetime],
            due_date: Optional[datetime], all_day: Optional[bool], priority: Optional[int]) -> bool:

        task = Task("0", project_id, title, content, start_date, due_date,
                    all_day if all_day is not None else False, TaskStatus.ACTIVE, priority)
        return self.add_many([task])

    def add_many(self, tasks: List[Task]) -> bool:
        url = f"https://api.ticktick.com/api/v2/batch/task"
        addBody = []
        for t in tasks:
            b = {}
            b.update({"id": "0"})
            b.update({"projectId": t.project_id})
            b.update({"title": t.title})
            if t.content is not None and t.content != "":
                b.update({"content": t.content})
            if t.priority is not None:
                b.update({"priority": t.priority})
            if t.start_date is not None:
                b.update({"startDate": self._parse_datetime(t.start_date.astimezone(timezone.utc))})
            if t.due_date is not None:
                b.update({"dueDate": self._parse_datetime(t.due_date.astimezone(timezone.utc))})
            b.update({"isAllDay": t.is_all_day})
            addBody.append(b)

        body = json.dumps({'add': addBody})
        response, content = self.client.post(url, body)
        return self.check_authorization_and_reconnect('add_many', response, content)

    def update(self, task: Task) -> bool:
        return self.update_many([task])

    def update_many(self, tasks: List[Task]) -> bool:
        url = f"https://api.ticktick.com/api/v2/batch/task"
        updateBody = []
        for t in tasks:
            b = {}
            b.update({"id": t.id})
            b.update({"projectId": t.project_id})
            b.update({"title": t.title})
            if t.content is not None and t.content != "":
                b.update({"content": t.content})
            if t.priority is not None:
                b.update({"priority": t.priority})
            if t.start_date is not None:
                b.update({"startDate": self._parse_datetime(t.start_date.astimezone(timezone.utc))})
            if t.due_date is not None:
                b.update({"dueDate": self._parse_datetime(t.due_date.astimezone(timezone.utc))})
            b.update({"status": t.status.value})
            b.update({"isAllDay": t.is_all_day})
            updateBody.append(b)

        body = json.dumps({'update': updateBody})
        response, content = self.client.post(url, body)
        return self.check_authorization_and_reconnect('update_many', response, content)

    def delete(self, task_id: str, project_id: str) -> bool:
        task = Task(task_id, project_id, "")
        return self.delete_many([task])

    def delete_many(self, tasks: List[Task]) -> bool:
        url = f"https://api.ticktick.com/api/v2/batch/task"
        deleteBoby = []
        for t in tasks:
            b = {}
            b.update({"taskId": t.id})
            b.update({"projectId": t.project_id})
            deleteBoby.append(b)

        body = json.dumps({'delete': deleteBoby})
        response, content = self.client.post(url, body)
        return self.check_authorization_and_reconnect('delete_many', response, content)

    def _build_task(self, data: dict) -> Task:
        id = data.get('id')
        title = data.get('title')
        content = data.get('content')
        priority = data.get('priority')
        project_id = data.get('projectId')
        statusNum = data.get('status')
        completed_time_str = data.get('completedTime')
        created_time_str = data.get('createdTime')
        modified_time_str = data.get('modifiedTime')
        start_date_str = data.get('startDate')
        due_date_str = data.get('dueDate')

        task = Task(
            id=id,
            content=content,
            completed_time=datetime.strptime(completed_time_str,
                                             DATE_FORMAT) if completed_time_str is not None else None,
            created_time=datetime.strptime(created_time_str,
                                           DATE_FORMAT) if created_time_str is not None else None,
            modified_time=datetime.strptime(modified_time_str,
                                            DATE_FORMAT) if modified_time_str is not None else None,
            due_date=datetime.strptime(due_date_str,
                                       DATE_FORMAT) if due_date_str is not None else None,
            start_date=datetime.strptime(start_date_str,
                                         DATE_FORMAT) if start_date_str is not None else None,
            priority=priority,
            project_id=project_id,
            status=TaskStatus(statusNum),
            title=title,
        )
        return task
