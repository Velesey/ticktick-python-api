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
    content: Optional[str]
    start_date: Optional[datetime]
    due_date: Optional[datetime]
    status: TaskStatus
    priority: int
    created_time: datetime
    modified_time: Optional[datetime]
    completed_time: Optional[datetime]
