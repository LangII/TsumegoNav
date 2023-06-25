

from __future__ import annotations
from copy import deepcopy

from kivy.logger import Logger
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import ButtonBehavior, Button
from kivy.uix.widget import Widget
from kivy.properties import ListProperty
from kivy.graphics import Color, Line, Rectangle, Ellipse

import util
from back.board import Board as BackBoard
from back.tree import Leaf as BackLeaf


####################################################################################################


NAME = util.getNameFromFile(__file__)


####################################################################################################


class Board(GridLayout, util.Helper):
    def __init__(self):
        super(Board, self).__init__()
        Logger.info(f"{NAME}: init Board")
        self.size_hint = [None, None]
        self.cols = self.data['board']['size']
        self.padding = util.PAD_V_MAIN_MID
        self.main_scroll_bar_pad = 0

        self.buttons = self.getAndAddButtons()
        self.bind(pos=self.updateDisplay, size=self.updateDisplay)

        self.resetBoard(self.data['input']['cur_problem'])

    def updateDisplay(self, *args) -> None:
        self.size = [self.parent.width - self.main_scroll_bar_pad] * 2

    def getAndAddButtons(self) -> dict:
        buttons = {}
        for i in range(self.cols ** 2):
            coord = [i // self.cols, i % self.cols]
            button = BoardButton(coord)
            self.add_widget(button)
            buttons[str(coord)] = button
        return buttons

    def getButtonByCoord(self, coord:list[int]) -> BoardButton:
        return self.buttons[str(coord)]

    def resetBoard(self, stones:dict[list[list]], include_back_board:bool=True) -> None:
        all_coords = [[i // self.cols, i % self.cols] for i in range(self.cols ** 2)]
        for coord in all_coords:  self.buttons[str(coord)].setToNoStone()
        for color, coords in stones.items():
            for coord in coords:
                self.buttons[str(coord)].setStoneColor(color)
        if include_back_board:  self.data['back']['board'].resetBoard(stones)


class BoardButton(ButtonBehavior, Widget, util.Helper):
    def __init__(self, coord:list[int]):
        super(BoardButton, self).__init__()
        self.coord = coord
        self.cur_stone = 'no'
        self.size_hint = [1.0, 1 / self.data['board']['size']]
        self.hor_line_type = self.getHorLineType()
        self.vert_line_type = self.getVertLineType()
        self.is_star = self.getIsStar()
        self.setAndAddCanvasBeforeObjs()
        self.setAndAddCanvasAfterObjs()
        self.bind(pos=self.updateDisplay, size=self.updateDisplay)

    def setAndAddCanvasBeforeObjs(self) -> None:
        with self.canvas.before:
            self.rect_color = Color(*util.CLR_BOARD_YELLOW)
            self.rect = Rectangle()
            self.hor_line_color = Color(*util.CLR_BLACK)
            self.hor_line = Line()
            self.vert_line_color = Color(*util.CLR_BLACK)
            self.vert_line = Line()
            self.star = self.getStar()

    def setAndAddCanvasAfterObjs(self) -> None:
        with self.canvas.after:
            self.stone_color = Color(*util.CLR_NOTHING)
            self.stone = Ellipse()
            self.stone_line_color = Color(*util.CLR_NOTHING)
            self.stone_line = Line()

    def updateDisplay(self, *args) -> None:
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.hor_line.points = self.getHorLinePoints()
        self.vert_line.points = self.getVertLinePoints()
        if self.is_star:  self.star.pos = self.getStarPos()
        self.stone.pos = self.pos
        self.stone.size = self.size
        self.stone_line.circle = self.getStoneLineCircleArgs()

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

    def getHorLinePoints(self) -> list[float]:
        line_type, pos_x, pos_y, size_x, size_y = self.hor_line_type, *self.rect.pos, *self.rect.size
        x1 = pos_x if line_type in ['center', 'right'] else (pos_x + (size_x / 2))
        x2 = (pos_x + size_x) if line_type in ['left', 'center'] else (pos_x + (size_x / 2))
        y1, y2 = [pos_y + (size_y / 2)] * 2
        return [x1, y1, x2, y2]

    def getVertLinePoints(self) -> list[float]:
        line_type, pos_x, pos_y, size_x, size_y = self.vert_line_type, *self.rect.pos, *self.rect.size
        y1 = (pos_y + size_y) if line_type in ['center', 'bottom'] else (pos_y + (size_y / 2))
        y2 = pos_y if line_type in ['top', 'center'] else (pos_y + (size_y / 2))
        x1, x2 = [pos_x + (size_x / 2)] * 2
        return [x1, y1, x2, y2]

    def getStarPos(self) -> list[float]:
        return [(self.pos[i] + (self.size[i] / 2)) - (self.star.size[i] / 2) for i in [0, 1]]

    def getStoneLineCircleArgs(self) -> list[float]:
        return [self.center_x, self.center_y, self.width / 2]

    #####

    def setToNoStone(self) -> None:
        self.cur_stone = 'no'
        self.stone_color.rgba = util.CLR_NOTHING
        self.stone_line_color.rgba = util.CLR_NOTHING

    def setStoneColor(self, color:str=None) -> None:
        if not color:  color = self.data['input']['board_options']['cur_stone']
        self.cur_stone = color
        self.stone_color.rgba = util.CLR_BLACK if color in ['b', 'black'] else util.CLR_WHITE
        self.stone_line_color.rgba = util.CLR_BLACK

    def getBackTreeAddLeafKwargs(self, cur_back_leaf:BackLeaf) -> dict:
        stone_color = 'b' if cur_back_leaf.stone_color == 'w' else 'w'
        add_leaf_kwargs = {
            'path_to_parent': cur_back_leaf.path_to_self,
            'leaf_kwargs': {
                'stone_color': stone_color,
                'move_count': cur_back_leaf.move_count + 1,
                'stone_pos': self.coord,
                'parent_leaf_i': cur_back_leaf.back_leaf_i,
                'is_cur_board': True,
            }
        }
        add_leaf_kwargs['leaf_kwargs']['board_pos'] = deepcopy(cur_back_leaf.board_pos)
        add_leaf_kwargs['leaf_kwargs']['board_pos'][stone_color] += [self.coord]
        return add_leaf_kwargs

    def on_release(self) -> None:
        if self.data['input']['mode'] == 'navigate':  self.handleNavigateInputMode()
        elif self.data['input']['mode'] == 'edit':  self.handleEditInputMode()

    def handleNavigateInputMode(self) -> None:
        if self.cur_stone == 'no':  self.handleNoCurStone()
        else:  self.handleYesCurStone()

    def handleNoCurStone(self) -> None:
        back_leaves = self.data['back']['tree'].leaves
        cur_back_leaf = back_leaves[self.data['input']['tree_options']['cur_back_leaf_i']]
        pos_already_selected = self.coord in [back_leaves[c].stone_pos for c in cur_back_leaf.children]

        if pos_already_selected:  self.handlePosAlreadySelected(back_leaves, cur_back_leaf)
        else:  self.handlePosNotAlreadySelected(cur_back_leaf)

    def handlePosAlreadySelected(self, back_leaves:list[BackLeaf], cur_back_leaf:BackLeaf) -> None:
        # Find this position's Front Leaf and force UI select it.
        selected_back_leaf = None
        for c in cur_back_leaf.children:
            if self.coord == back_leaves[c].stone_pos:
                selected_back_leaf = back_leaves[c] ; break
        self.app.main_window.main_scroll.main_scroll_layout.tree.leaves[selected_back_leaf.front_leaf_i].on_release()

    def handlePosNotAlreadySelected(self, cur_back_leaf:BackLeaf) -> None:
        opp_stone_color = 'b' if cur_back_leaf.stone_color == 'w' else 'w'
        is_legal, reason = self.data['back']['board'].play(opp_stone_color, self.coord, only_test_legality=True)
        if not is_legal:  Logger.info(f"{NAME}: BoardButton '{self.coord}' on_release() = 'illegal move - {reason}'")
        else:  self.handleIsLegal()

    def handleIsLegal(self) -> None:
        # get current backend leaf (has to be collected before updating 'main' 'data')
        cur_back_leaf = self.data['back']['tree'].leaves[self.data['input']['tree_options']['cur_back_leaf_i']]
        # update 'main' 'data' (has to be after previously collecting 'main' 'data')
        self.data['input']['tree_options']['cur_back_leaf_i'] = self.data['back']['tree'].next_leaf
        # update current backend leaf
        cur_back_leaf.is_cur_board = False
        # update backend tree with addLeaf()
        self.data['back']['tree'].addLeaf(**self.getBackTreeAddLeafKwargs(cur_back_leaf))
        # refresh frontend tree layout
        self.parent.parent.tree.refreshLayout()
        # update self
        self.setStoneColor()
        # update backend board with play()
        self.data['back']['board'].play(self.data['input']['board_options']['cur_stone'][0], self.coord)
        # update board options
        self.cycleCurNextStoneButtons()

    def handleYesCurStone(self) -> None:
        # Handle when a Board Button is selected and it already has a stone...
        # When selecting a Stone on the Board, reset the Tree to have it's current Leaf be the
        # Leaf that has the selected Stone's coordinates as it's stone_pos.  Will require
        # alternative logic for when the User selects a Stone from the Root pos.
        return

    def handleEditInputMode(self) -> None:
        if self.cur_stone == self.data['input']['board_options']['cur_stone']:
            self.setToNoStone()
        else:
            self.setStoneColor()
            if self.data['input']['board_options']['next_stone_state'] == 'alternate':
                self.cycleCurNextStoneButtons()

    #####

    def cycleCurNextStoneButtons(self):
        self.parent.parent.board_options.cur_next_stone_options.cur_stone_button.cycleColor()
        self.parent.parent.board_options.cur_next_stone_options.next_stone_button.cycleColor()



