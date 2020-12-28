from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class TaskStatus(Enum):
    ACTIVE = 0
    COMPLETED = 2


@dataclass
class Task:
    id: str
    project_id: str
    title: str
    content: Optional[str] = None
    start_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    is_all_day: bool = False
    status: TaskStatus = TaskStatus.ACTIVE
    priority: Optional[int] = 0
    created_time: Optional[datetime] = None
    modified_time: Optional[datetime] = None
    completed_time: Optional[datetime] = None
