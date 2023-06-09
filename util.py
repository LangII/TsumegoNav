

import logging
from typing import Any
import json
import sys

from kivy.app import App
from kivy.logger import Logger, ColoredFormatter


####################################################################################################


PROJECT_NAME = __file__.split('/')[-2]

LOG_FORMAT = '[%(asctime)s] [%(levelname)-18s] %(message)s'

CLR_BLACK =             [0.00, 0.00, 0.00, 1.00]
CLR_WHITE =             [1.00, 1.00, 1.00, 1.00]
CLR_NOTHING =           [0.00, 0.00, 0.00, 0.00]
CLR_BOARD_YELLOW =      [0.85, 0.60, 0.00, 1.00]
CLR_PRISMARINE =        [0.00, 0.40, 0.40, 1.00]
CLR_DARK_PRISMARINE =   [0.00, 0.30, 0.30, 1.00]

PAD_MAIN = 8
# [left, top, right, bottom]
PAD_V_MAIN_TOP =    [PAD_MAIN, PAD_MAIN, PAD_MAIN,        0]
PAD_V_MAIN_MID =    [PAD_MAIN, 0,        PAD_MAIN,        0]
PAD_V_MAIN_BOTTOM = [PAD_MAIN, 0,        PAD_MAIN, PAD_MAIN]
PAD_H_MAIN_LEFT =   [PAD_MAIN, PAD_MAIN, 0,        PAD_MAIN]
PAD_H_MAIN_MID =    [0,        PAD_MAIN, 0,        PAD_MAIN]
PAD_H_MAIN_RIGHT =  [0,        PAD_MAIN, PAD_MAIN, PAD_MAIN]
PAD_MAIN_ALL =      [PAD_MAIN, PAD_MAIN, PAD_MAIN, PAD_MAIN]

SPC_MAIN = 8

SCROLL_BAR_WIDTH_MAIN = 16
SCROLL_BAR_WIDTH_SECONDARY = PAD_MAIN


####################################################################################################


class Helper():
    def __init__(self):
        self.app = App.get_running_app()
        if self.app:  self.data = self.app.data
        else:  self.data = None


####################################################################################################


def updateLogger() -> None:
    for i, formatter in zip([1, 2], [logging.Formatter, ColoredFormatter]):
        Logger.handlers[i].setFormatter(formatter(LOG_FORMAT))


def getNameFromFile(file:str) -> str:
    return file[(file.rfind(PROJECT_NAME) + len(PROJECT_NAME) + 1):file.rfind('.')]


def prettyPrint(var_name: str, obj: Any) -> None:
    default = lambda x: str(x) or x.__repr__()
    print(f"\n{var_name} = {json.dumps(obj, indent=4, default=default)}\n")


def throwError(name:str, msg:str) -> None:
    Logger.error(f"{name}: {msg}")
    sys.exit()


def convStrListCoordToListCoord(str_list_coord:str) -> list[int]:
    for char in list('[ ]'):  str_list_coord = str_list_coord.replace(char, '')
    return [int(x) for x in str_list_coord.split(',')]


####################################################################################################


NAME = getNameFromFile(__file__)



















