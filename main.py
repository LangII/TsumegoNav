

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

from kivy.uix.splitter import Splitter

import util
from ui.menu import BoardOptions
from ui.board import Board


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
        'button_objs': [],
    },
}


####################################################################################################


def main() -> None:

    util.updateLogger()

    Logger.info(f"{NAME}: start {util.PROJECT_NAME}")

    MainApp().run()

    Logger.info(f"{NAME}: end {util.PROJECT_NAME}\n")


####################################################################################################


class MainApp(App):
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        self.data = DATA
        self.main_window = None
        Window.size = self.data['window']['size_default']
        Window.clearcolor = util.PRISMARINE
        Window.bind(on_key_down=self.keyboardInput)

    def build(self):
        self.main_window = MainWindow()
        return self.main_window

    #####  \/  IN APP TESTING

    def keyboardInput(self, obj:WindowSDL, num1:int, num2:int, text:str, *args) -> None:
        if text == ' ':  self.spaceBarInput()

    def spaceBarInput(self) -> None:
        print(f"\n{self.data = }\n")
        for k, button in self.data['board']['buttons'].items():
            print(f"{k = }")
            print(f"{button.pos = }")
            print(f"{button.size = }\n")

    #####  /\  IN APP TESTING


class MainWindow(BoxLayout, util.Helper):
    def __init__(self):
        super(MainWindow, self).__init__()
        Logger.info(f"{NAME}: init MainWindow()")
        self.orientation = 'vertical'
        self.main_scroll = MainScroll()
        self.add_widget(self.main_scroll)


class MainScroll(ScrollView, util.Helper):
    def __init__(self):
        super(MainScroll, self).__init__()
        Logger.info(f"{NAME}: init MainScroll()")
        # self.do_scroll_x = False

        self.size_hint = [1.0, None]
        self.size = [Window.width, Window.height]

        self.box_layout = BoxLayout()
        self.box_layout.size_hint = [1.0, None]
        self.box_layout.orientation = 'vertical'
        self.box_layout.bind(minimum_height=self.box_layout.setter('height'))  # \_(**)_/
        self.add_widget(self.box_layout)

        # self.board_options = BoardOptions()
        # self.add_widget(self.board_options)
        # self.box_layout.add_widget(self.board_options)

        from kivy.uix.button import Button

        for i in range(3):
            self.box_layout.add_widget(Button(size_hint=[1.0, None], height=40))

        self.board = Board()
        # self.add_widget(self.board)
        self.box_layout.add_widget(self.board)

        # self.button_1 = Button()
        # self.button_1.size_hint = [1.0, None]
        # self.button_1.height = 20
        # self.board_options.add_widget(self.button_1)




####################################################################################################


if __name__ == '__main__':  main()

