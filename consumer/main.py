import argparse
import json
import os
from dataclasses import asdict
from pprint import pprint
from typing import Tuple, Optional

from bson import json_util
from time import sleep

from utils.color_log import print_colorful_log, TASK_TYPE_TO_COLOR, print_start_color, print_done_color
from schema.task_type import TaskType
from tasks.task import Task


class FileNotExistsException(Exception):
    pass


class UnknownTaskType(Exception):
    pass


class Consumer:
    def __init__(self, task_type: TaskType, file_name: str):
        self.task_type = task_type
        self.file_name = file_name

    def _find_task(self) -> Tuple[Optional[Task], Optional[int]]:
        file = open(self.file_name, 'r')
        str_tasks = file.readlines()
        file.close()
        for index, task_str in enumerate(str_tasks):
            task_dict = json.loads(task_str, object_hook=json_util.object_hook)
            task = Task(**task_dict)
            task.type = TaskType(task.type)

            if task.type != self.task_type:
                continue

            return task, index

        return None, None

    def consume_task(self):
        task, line_number = self._find_task()
        if not task:
            print('Task not found, sleeping')
            return

        self.process_task(task, line_number)

    @staticmethod
    def _log_consumed_task(task: Task) -> None:
        print_colorful_log(f'Consuming task: {task.type}', color=TASK_TYPE_TO_COLOR[task.type])
        print_start_color(TASK_TYPE_TO_COLOR[task.type])
        pprint(asdict(task))
        print_done_color()

    def process_task(self, task: Task, line_number: int):
        self._log_consumed_task(task)
        self._remove_task_line(line_number)

    def _remove_task_line(self, line_number: int):
        file = open(self.file_name, 'r')
        lines = file.readlines()
        file.close()

        lines = lines[0:line_number] + lines[line_number+1:]
        file = open(self.file_name, 'w')
        file.writelines(lines)
        file.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--type", "--task_type",
                        dest="task_type",
                        help="Task type to consume",
                        required=True)
    parser.add_argument("-f", "--file", "--file_name",
                        dest="file_name",
                        help="File name to consume tasks from",
                        required=True)
    args = parser.parse_args()

    if not os.path.exists(args.file_name):
        raise FileNotExistsException(f"File name {args.file_name} doesn't exists")

    try:
        task_type = TaskType[args.task_type.upper()]
    except KeyError:
        raise UnknownTaskType('Task type is not supported by the digestive cluster')

    consumer = Consumer(task_type=task_type, file_name=args.file_name)
    while True:
        consumer.consume_task()
        sleep(3)
