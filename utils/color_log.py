import time
import platform
from enum import Enum

from schema.task_type import TaskType


class ColorText(Enum):
    RESET = "\033[0m"

    BOLD = "\033[1m"

    GRAY = "\x1b[1;30;40m"
    RED = "\033[1;31m"
    GREEN = "\033[1;32m"
    YELLOW = "\x1b[1;33;40m"
    BLUE = "\x1b[1;34;40m"
    PURPLE = "\x1b[1;35;40m"
    LIGHT_YELLOW = "\x1b[1;36;40m"
    WHITE = "\033[37m"


TASK_TYPE_TO_COLOR = {
    TaskType.RAM: ColorText.RED,
    TaskType.IO: ColorText.GREEN,
    TaskType.CPU: ColorText.PURPLE
}

IS_COLORING_ENABLED = False


def enable_coloring_in_windows_10():
    global IS_COLORING_ENABLED
    if not IS_COLORING_ENABLED and platform.system() == 'Windows' and platform.win32_ver()[0] == '10':
        # Enable coloring in windows 10
        import ctypes
        kernel32 = ctypes.WinDLL('kernel32')
        std_handle = kernel32.GetStdHandle(-11)
        mode = ctypes.c_ulong()
        kernel32.GetConsoleMode(std_handle, ctypes.byref(mode))
        mode.value |= 4
        kernel32.SetConsoleMode(std_handle, mode)

    IS_COLORING_ENABLED = True


def print_colorful_log(message: str, color: ColorText = ColorText.WHITE, bold: bool = False) -> None:
    enable_coloring_in_windows_10()

    text = f"{color.value}{message}{ColorText.RESET.value}"
    if bold:
        text = f"{ColorText.BOLD.value}{text}{ColorText.RESET.value}"
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}]: {text}")


def print_start_color(color):
    print(color.value)


def print_done_color():
    print(ColorText.RESET.value)

