

from kivy.logger import Logger
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import ButtonBehavior
from kivy.graphics import Color, Rectangle, Ellipse, Line

import util


####################################################################################################


NAME = util.getNameFromFile(__file__)


####################################################################################################


class BoardOptions(BoxLayout, util.Helper):
    def __init__(self):
        super(BoardOptions, self).__init__()
        Logger.info(f"{NAME}: init BoardOptions")
        self.orientation = 'horizontal'
        self.size_hint = [1.0, None]
        self.height = 80
        self.padding_outer = util.PAD_V_MAIN_TOP
        self.padding_inner = util.PAD_MAIN_ALL
        self.padding = [self.padding_outer[i] + self.padding_inner[i] for i in range(4)]
        self.spacing = util.SPC_MAIN
        self.setAndAddCanvasBeforeObjs()
        self.cur_next_stone_options = CurNextStoneOptions()
        self.add_widget(self.cur_next_stone_options)
        self.updateDisplay()
        self.bind(pos=self.updateDisplay, size=self.updateDisplay)

    def setAndAddCanvasBeforeObjs(self) -> None:
        with self.canvas.before:
            self.rect_color = Color(*util.CLR_DARK_PRISMARINE)
            self.rect = Rectangle()

    def updateDisplay(self, *args) -> None:
        self.rect.pos = [
            self.pos[0] + self.padding_outer[0],
            self.pos[1] + self.padding_outer[3]
        ]
        self.rect.size = [
            self.size[0] - self.padding_outer[1] - self.padding_outer[0],
            self.size[1] - self.padding_outer[2] - self.padding_outer[3]
        ]


class CurNextStoneOptions(BoxLayout, util.Helper):
    def __init__(self):
        super(CurNextStoneOptions, self).__init__()
        Logger.info(f"{NAME}: init CurNextStoneOptions")
        self.orientation = 'horizontal'
        self.spacing = util.SPC_MAIN
        self.padding = util.PAD_MAIN_ALL
        self.size_hint = [None, 1.0]
        self.setAndAddCanvasBeforeObjs()
        self.cur_stone_button = CurStoneButton()
        self.add_widget(self.cur_stone_button)
        self.next_stone_button = NextStoneButton()
        self.add_widget(self.next_stone_button)
        self.width = self.getWidth()
        self.updateDisplay()
        self.bind(pos=self.updateDisplay, size=self.updateDisplay)

    def getWidth(self) -> float:
        return (self.cur_stone_button.height * 2) + (util.SPC_MAIN * 3)

    def setAndAddCanvasBeforeObjs(self) -> None:
        with self.canvas.before:
            self.rect_color = Color(*util.CLR_PRISMARINE)
            self.rect = Rectangle()

    def updateDisplay(self, *args) -> None:
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.cur_stone_button.width = self.cur_stone_button.height
        self.next_stone_button.width = self.next_stone_button.height
        self.width = self.getWidth()


class CurNextStoneButton(ButtonBehavior, Widget, util.Helper):
    def __init__(self, option:str):
        super(CurNextStoneButton, self).__init__()
        self.option = option
        with self.canvas.after:
            self.stone_color = Color(*util.CLR_WHITE)
            self.stone = Ellipse()
            self.stone_line_color = Color(*util.CLR_BLACK)
            self.stone_line = Line()
        self.bind(pos=self.updateDisplay, size=self.updateDisplay)

    def updateDisplay(self, *args) -> None:
        self.stone.pos = self.pos
        self.stone.size = self.size
        self.stone_line.circle = self.getStoneLineCircleArgs()

    def getStoneLineCircleArgs(self) -> list[float]:
        return [self.center_x, self.center_y, self.width / 2]

    def setColor(self, color:str) -> None:
        self.data['input']['board_options'][self.option] = color
        self.color = color
        self.stone_color.rgba = util.CLR_BLACK if color == 'black' else util.CLR_WHITE

    def cycleColor(self) -> None:
        if self.color == 'black':  self.setColor('white')
        elif self.color == 'white':  self.setColor('black')


class CurStoneButton(CurNextStoneButton):
    def __init__(self):
        super(CurStoneButton, self).__init__('cur_stone')
        Logger.info(f"{NAME}: init CurStoneButton")
        self.setColor(self.data['input']['board_options']['cur_stone'])

    def on_release(self) -> None:
        self.cycleColor()
        self.parent.next_stone_button.cycleColor()


class NextStoneButton(CurNextStoneButton):
    def __init__(self):
        super(NextStoneButton, self).__init__('next_stone')
        Logger.info(f"{NAME}: init NextStoneButton")
        self.setColor(self.data['input']['board_options']['next_stone'])

    def cycleNextStoneState(self) -> None:
        if self.data['input']['board_options']['next_stone_state'] == 'alternate':
            self.data['input']['board_options']['next_stone_state'] = 'consecutive'
        elif self.data['input']['board_options']['next_stone_state'] == 'consecutive':
            self.data['input']['board_options']['next_stone_state'] = 'alternate'

    def on_release(self) -> None:
        self.cycleColor()
        self.cycleNextStoneState()





























