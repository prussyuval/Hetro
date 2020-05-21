from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import uuid4

from schema.task_type import TaskType


@dataclass
class Task:
    type: TaskType
    source_ip: str
    content: Any
    creation_time: datetime
    id: str = str(uuid4())
