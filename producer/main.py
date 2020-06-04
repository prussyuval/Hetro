import argparse
import base64
import os
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

from utils.color_log import print_colorful_log, TASK_TYPE_TO_COLOR, print_start_color, print_done_color, ColorText
from schema.task_type import TaskType
from tasks.task import Task


class FileNotExistsException(Exception):
    pass


class Producer:
    def __init__(self, file_name: str):
        self.file_name = file_name

    @staticmethod
    def dump_content(content: Any) -> str:
        return json.dumps(content, default=json_util.default)

    @staticmethod
    def _get_ip_address():
        return requests.get('http://ident.me/').text

    @staticmethod
    def _log_task(task: dict) -> None:
        print_colorful_log('Produce task:', color=ColorText.BOLD)
        print_start_color(TASK_TYPE_TO_COLOR[task['type']])
        pprint(task)
        print_done_color()

    def create_task(self, task_type: TaskType, content: Any):
        content_str = self.dump_content(content)

        task = asdict(Task(type=task_type,
                           content=content_str,
                           source_ip=self._get_ip_address(),
                           creation_time=datetime.utcnow()))

        file = open(self.file_name, 'a')
        self._log_task(task)
        file.write(f'{json.dumps(task, default=json_util.default)}\n')
        file.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", "--file_name",
                        dest="file_name",
                        help="File name to consume tasks from",
                        required=True)
    args = parser.parse_args()

    if not os.path.exists(args.file_name):
        raise FileNotExistsException(f"File name {args.file_name} doesn't exists")

    producer = Producer(file_name=args.file_name)
    while True:
        task_type = random.choice([TaskType.IO, TaskType.RAM, TaskType.CPU])
        content = dict(image=base64.b64encode(
            ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(150)).encode()
        ).decode())
        producer.create_task(task_type=task_type, content=content)
        sleep(1)
