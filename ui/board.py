

from kivy.logger import Logger
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import ButtonBehavior, Button
from kivy.uix.widget import Widget
from kivy.properties import ListProperty
from kivy.graphics import Color, Line, Rectangle, Ellipse

import util


####################################################################################################


NAME = util.getNameFromFile(__file__)


class Board(GridLayout, util.Helper):
    def __init__(self):
        super(Board, self).__init__()
        self.cols = self.data['board']['size']
        self.buttons = self.getAndAddButtons()
        self.data['board']['button_objs'] = self.buttons
        self.size_hint = [1.0, None]
        self.bind(pos=self.updateCanvas, size=self.updateCanvas)

    def updateCanvas(self, *args) -> None:
        self.size = [self.parent.width] * 2

    def getAndAddButtons(self) -> dict:
        buttons = {}
        for i in range(self.cols ** 2):
            coord = [i // self.cols, i % self.cols]
            button = BoardButton(coord)
            self.add_widget(button)
            buttons[str(coord)] = button
        return buttons


class BoardButton(ButtonBehavior, Widget, util.Helper):
    def __init__(self, coord:list[int]):
        super(BoardButton, self).__init__()
        self.coord = coord
        self.hor_line_type = self.getHorLineType()
        self.vert_line_type = self.getVertLineType()
        self.is_star = self.getIsStar()
        self.setAndAddCanvasBeforeObjs()
        self.size_hint = [1.0, 1 / self.data['board']['size']]
        self.bind(pos=self.updateCanvas, size=self.updateCanvas)

    def setAndAddCanvasBeforeObjs(self) -> None:
        with self.canvas.before:
            self.rect_color = Color(*util.BOARD_YELLOW)
            self.rect = Rectangle()
            self.hor_line_color = Color(*util.BLACK)
            self.hor_line = Line()
            self.vert_line_color = Color(*util.BLACK)
            self.vert_line = Line()
            self.star = self.getStar()

    def updateCanvas(self, *args) -> None:
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.hor_line.points = self.getHorLinePoints()
        self.vert_line.points = self.getVertLinePoints()
        if self.is_star:  self.star.pos = self.getStarPos()

    def getHorLineType(self) -> str:
        if self.coord[1] == 0:  return 'left'
        elif self.coord[1] == self.data['board']['size'] - 1:  return 'right'
        return 'center'

    def getVertLineType(self) -> str:
        if self.coord[0] == 0:  return 'top'
        elif self.coord[0] == self.data['board']['size'] - 1:  return 'bottom'
        return 'center'

    def getIsStar(self) -> bool:
        return True if self.coord in self.data['board']['grid']['star_coords'] else False

    def getStar(self) -> Ellipse:
        return Ellipse(size=[self.data['board']['grid']['star_size']] * 2) if self.is_star else None

    def getHorLinePoints(self) -> list[int]:
        line_type, pos_x, pos_y, size_x, size_y = self.hor_line_type, *self.rect.pos, *self.rect.size
        x1 = pos_x if line_type in ['center', 'right'] else (pos_x + (size_x / 2))
        x2 = (pos_x + size_x) if line_type in ['left', 'center'] else (pos_x + (size_x / 2))
        y1, y2 = [pos_y + (size_y / 2)] * 2
        return [x1, y1, x2, y2]

    def getVertLinePoints(self) -> list[int]:
        line_type, pos_x, pos_y, size_x, size_y = self.vert_line_type, *self.rect.pos, *self.rect.size
        y1 = (pos_y + size_y) if line_type in ['center', 'bottom'] else (pos_y + (size_y / 2))
        y2 = pos_y if line_type in ['top', 'center'] else (pos_y + (size_y / 2))
        x1, x2 = [pos_x + (size_x / 2)] * 2
        return [x1, y1, x2, y2]

    def getStarPos(self) -> list[int]:
        return [(self.pos[i] + (self.size[i] / 2)) - (self.star.size[i] / 2) for i in [0, 1]]

    def on_release(self) -> None:
        print(f"{self.coord = }")




