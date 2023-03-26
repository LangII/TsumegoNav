

import logging
from typing import Any
import json

from kivy.app import App
from kivy.logger import Logger, ColoredFormatter


####################################################################################################


PROJECT_NAME = __file__.split('/')[-2]

LOG_FORMAT = '[%(asctime)s] [%(levelname)-18s] %(message)s'

PRISMARINE =    [0.00, 0.40, 0.40, 1.00]
BOARD_YELLOW =  [0.85, 0.60, 0.00, 1.00]
BLACK =         [0.00, 0.00, 0.00, 1.00]
WHITE =         [1.00, 1.00, 1.00, 1.00]
NOTHING =       [0.00, 0.00, 0.00, 0.00]


####################################################################################################


class Helper():
    def __init__(self):
        self.data = App.get_running_app().data


def updateLogger() -> None:
    for i, formatter in zip([1, 2], [logging.Formatter, ColoredFormatter]):
        Logger.handlers[i].setFormatter(formatter(LOG_FORMAT))


def getNameFromFile(file:str) -> str:
    return file[(file.rfind(PROJECT_NAME) + len(PROJECT_NAME) + 1):file.rfind('.')]


def prettyPrint(var_name: str, obj: Any) -> None:
    default = lambda x: str(x) or x.__repr__()
    print(f"\n{var_name} = {json.dumps(obj, indent=4, default=default)}\n")
