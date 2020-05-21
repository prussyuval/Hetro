from schema.task_type import TaskType
from tasks.task import Task


class UploadImage(Task):
    type = TaskType.IO
    content: bytes
