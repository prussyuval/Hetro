import base64
import random
import string
from pprint import pprint

from bson import json_util
import json
from dataclasses import asdict
from datetime import datetime
from time import sleep
from typing import Any

import requests

from schema.task_type import TaskType
from tasks.task import Task


class Producer:
    def __init__(self, file_name: str):
        self.file_name = file_name

    @staticmethod
    def dump_content(content: Any) -> str:
        return json.dumps(content, default=json_util.default)

    @staticmethod
    def _get_ip_address():
        return requests.get('http://ident.me/').text

    def create_task(self, task_type: TaskType, content: Any):
        content_str = self.dump_content(content)

        task = asdict(Task(type=task_type,
                           content=content_str,
                           source_ip=self._get_ip_address(),
                           creation_time=datetime.utcnow()))

        file = open(self.file_name, 'a')
        print('Produce task:')
        pprint(task)
        file.write(f'{json.dumps(task, default=json_util.default)}\n')
        file.close()


if __name__ == '__main__':
    producer = Producer(r'C:\Users\pruss\Desktop\tasks.txt')
    while True:
        task_type = random.choice([TaskType.IO, TaskType.RAM, TaskType.CPU])
        content = dict(image=base64.b64encode(
            ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(150)).encode()
        ).decode())
        producer.create_task(task_type=task_type, content=content)
        sleep(1)
