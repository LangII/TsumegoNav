

"""
TURNOVER NOTES:

2023-03-17
- Next to do is make a board.  Review board from GoCalc for references...  Good luck!
"""


import json

from kivy.logger import Logger
from kivy.app import App
from kivy.core.window import Window
from kivy.core.window.window_sdl2 import WindowSDL
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView

import util
from front.menu import BoardOptions
from front.board import Board
from front.tree import Tree


####################################################################################################


NAME = util.getNameFromFile(__file__)

DATA = {
    'window': {
        'size_default': [600, 800],
    },
    'board': {
        'size': 19,
        'grid': {
            'star_size': 5,
            'star_coords': [
                [3, 3], [3, 9], [3, 15], [9, 3], [9, 9], [9, 15], [15, 3], [15, 9], [15, 15],
            ],
        },
    },
    'input': {
        'board_options': {
            'cur_stone': 'black',  # 'black' or 'white'
            'next_stone': 'white',  # 'black' or 'white'
            'next_stone_state': 'alternate',  # 'alternate' or 'consecutive'
        },
    },
    'back': {
        'board_obj': None,
        'tree_obj': None,
    }
}


####################################################################################################


def main() -> None:

    util.updateLogger()

    Logger.info(f"{NAME}: start {util.PROJECT_NAME}")

    MainApp().run()

    Logger.info(f"{NAME}: end {util.PROJECT_NAME}\n")


####################################################################################################


class MainApp(App):
    def __init__(self):
        super(MainApp, self).__init__()
        self.data = DATA
        self.title = util.PROJECT_NAME
        self.main_window = None
        Window.size = self.data['window']['size_default']
        Window.clearcolor = util.CLR_PRISMARINE
        Window.bind(on_key_down=self.keyboardInput)

    def build(self):
        self.main_window = MainWindow()
        return self.main_window

    #####  \/  IN APP TESTING

    def keyboardInput(self, obj:WindowSDL, num1:int, num2:int, text:str, *args) -> None:
        if text == ' ':  self.spaceBarInput()

    def spaceBarInput(self) -> None:
        print("")
        print(f"{Window.mouse_pos = }")

        var = self.main_window.main_scroll.vbar
        print("")
        print(f"{var = }")

        # board_options = self.main_window.main_scroll.main_scroll_layout.board_options
        # print("")
        # print(f"{board_options.padding = }")
        # print(f"{board_options.pos = }")
        # print(f"{board_options.size = }")
        # print(f"{board_options.rect.pos = }")
        # print(f"{board_options.rect.size = }\n")

    #####  /\  IN APP TESTING


class MainWindow(BoxLayout, util.Helper):
    def __init__(self):
        super(MainWindow, self).__init__()
        Logger.info(f"{NAME}: init MainWindow")
        self.orientation = 'vertical'
        self.main_scroll = MainScroll()
        self.add_widget(self.main_scroll)

        # Fixes problem where content does not stay at top of scroll during window resizing.
        self.bind(pos=self.main_scroll.updateDisplay, size=self.main_scroll.updateDisplay)

        #####  \/  SETUP TESTING

        presets = {
            'b': [[2, 2], [2, 3], [2, 4], [2, 5], [1, 7],],
            'w': [[1, 1], [1, 2], [1, 3], [1, 4], [1, 5],]
        }
        for color, coords in presets.items():
            for coord in coords:
                self.main_scroll.main_scroll_layout.board.buttons[str(coord)].setStoneColor(color)

        ##### /\  SETUP TESTING



class MainScroll(ScrollView, util.Helper):
    def __init__(self):
        super(MainScroll, self).__init__()
        Logger.info(f"{NAME}: init MainScroll")
        self.size = [Window.width, Window.height]
        self.scroll_type = ['bars']
        self.bar_width = util.SCROLL_BAR_WIDTH_MAIN
        self.bar_color = util.CLR_DARK_PRISMARINE
        self.bar_inactive_color = util.CLR_DARK_PRISMARINE
        self.bar_margin = util.PAD_MAIN

        self.main_scroll_layout = MainScrollLayout()
        self.add_widget(self.main_scroll_layout)

        self.bind(pos=self.scrollBarVisibleCheck, size=self.scrollBarVisibleCheck)
        self.scrollBarVisibleCheck()

    def scrollBarVisibleCheck(self, *args) -> None:
        if self.vbar == (0, 1.0):
            self.main_scroll_layout.padding = [0, 0, 0, 0]
            self.main_scroll_layout.board.main_scroll_bar_pad_mod = 0
        else:
            self.main_scroll_layout.padding = [0, 0, self.bar_width + util.PAD_MAIN, 0]
            self.main_scroll_layout.board.main_scroll_bar_pad_mod = self.bar_width + util.PAD_MAIN

    def updateDisplay(self, *args):
        # See note for MainWindow.bind().
        self.pos, self.size = self.parent.pos, self.parent.size


class MainScrollLayout(BoxLayout, util.Helper):
    def __init__(self):
        super(MainScrollLayout, self).__init__()
        Logger.info(f"{NAME}: init MainScrollLayout")
        self.size_hint = [1.0, None]
        self.orientation = 'vertical'
        self.spacing = util.SPC_MAIN

        self.board_options = BoardOptions()
        self.add_widget(self.board_options)
        self.board = Board()
        self.add_widget(self.board)
        self.tree = Tree()
        self.add_widget(self.tree)

        self.bind(
            pos=self.board.updateDisplay,
            size=self.board.updateDisplay,
            # Not sure why this is needed, but the example in the docs has it.  \_(**)_/
            minimum_height=self.setter('height')
        )


####################################################################################################


if __name__ == '__main__':  main()

