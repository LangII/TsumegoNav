

from kivy.logger import Logger
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import ButtonBehavior
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Ellipse, Line

import util


####################################################################################################


NAME = util.getNameFromFile(__file__)


####################################################################################################


class Tree(BoxLayout, util.Helper):
    def __init__(self):
        super(Tree, self).__init__()
        Logger.info(f"{NAME}: init Tree")
        self.orientation = 'vertical'
        self.size_hint = [1.0, None]
        self.height = 200
        self.padding = util.PAD_MAIN_ALL
        self.tree_row_layouts = []
        self.leaves = []

        self.setAndAddCanvasBeforeObjs()
        self.updateDisplay()
        self.bind(pos=self.updateDisplay, size=self.updateDisplay)
        self.tree_scroll = TreeScroll()
        self.add_widget(self.tree_scroll)
        self.tree_scroll.initPlus()

        self.refreshLayout()

    def setAndAddCanvasBeforeObjs(self) -> None:
        with self.canvas.before:
            self.rect_color = Color(*util.CLR_DARK_PRISMARINE)
            self.rect = Rectangle()

    def updateDisplay(self, *args) -> None:
        self.rect.pos = [
            self.pos[0] + self.padding[0],
            self.pos[1] + self.padding[3]
        ]
        self.rect.size = [
            self.size[0] - self.padding[2] - self.padding[2],
            self.size[1] - self.padding[1]
        ]

    def refreshLayout(self) -> None:
        self.tree_scroll.tree_layout.clear_widgets()
        self.tree_row_layouts = []
        self.leaves = []
        if not self.data['back']['tree'].front_tree_map:
            root_leaf = RootLeaf(0, 0, is_cur_board=True)
            self.leaves += [root_leaf]
            new_tree_row_layout = TreeRowLayout()
            self.tree_row_layouts += [new_tree_row_layout]
            new_tree_row_layout.add_widget(root_leaf)
            new_tree_row_layout.resizeAfterChildren()
            self.tree_scroll.tree_layout.add_widget(new_tree_row_layout)
            self.tree_scroll.tree_layout.resizeAfterChildren()
            return
        for row in self.data['back']['tree'].front_tree_map:
            new_tree_row_layout = TreeRowLayout()
            for back_leaf_i in row:


                front_leaf_i = len(self.leaves)

                if type(back_leaf_i) == int:
                    is_cur_board = self.data['back']['tree'].leaves[back_leaf_i].is_cur_board
                    if back_leaf_i == 0:
                        new_leaf = RootLeaf(front_leaf_i, back_leaf_i, is_cur_board=is_cur_board)
                    else:
                        new_leaf = StoneLeaf(front_leaf_i, back_leaf_i, self.data['back']['tree'].leaves[back_leaf_i].stone_color, is_cur_board=is_cur_board)

                elif back_leaf_i in ['|', 'L', 'T']:
                    new_leaf = BranchLeaf(front_leaf_i, back_leaf_i)
                else:
                    new_leaf = EmptyLeaf(front_leaf_i)

                self.leaves += [new_leaf]
                new_tree_row_layout.add_widget(new_leaf)
            new_tree_row_layout.resizeAfterChildren()
            self.tree_scroll.tree_layout.add_widget(new_tree_row_layout)
            self.tree_row_layouts += [new_tree_row_layout]
        self.tree_scroll.tree_layout.resizeAfterChildren()



class TreeScroll(ScrollView, util.Helper):
    def __init__(self):
        super(TreeScroll, self).__init__()
        Logger.info(f"{NAME}: init TreeScroll")
        self.size_hint = [None, None]
        self.padding = util.PAD_MAIN_ALL
        self.scroll_type = ['bars']
        self.bar_width = util.SCROLL_BAR_WIDTH_SECONDARY
        self.bar_color = util.CLR_PRISMARINE
        self.bar_inactive_color = util.CLR_PRISMARINE
        self.tree_layout = TreeLayout()
        self.add_widget(self.tree_layout)

    def initPlus(self) -> None:
        self.updateDisplay()
        self.bind(pos=self.updateDisplay, size=self.updateDisplay)

    def updateDisplay(self, *args) -> None:
        self.pos = [
            self.parent.pos[0] + self.padding[0] + 8,
            self.parent.pos[1] + self.padding[3] + 8
        ]
        self.size = [
            self.parent.size[0] - self.padding[2] - self.padding[2] - 16,
            self.parent.size[1] - self.padding[1] - self.padding[1] - 8
        ]


class TreeLayout(BoxLayout, util.Helper):
    def __init__(self):
        super(TreeLayout, self).__init__()
        Logger.info(f"{NAME}: init TreeLayout")
        self.orientation = 'vertical'
        self.spacing = 0
        self.size_hint = [None, None]
        self.bind(minimum_height=self.setter('height'), minimum_width=self.setter('width'))

        #####  \/  MANUAL LEAF LAYOUT FOR TESTING

        # self.tree_row_layout_1 = TreeRowLayout()
        # self.add_widget(self.tree_row_layout_1)
        #
        # self.tree_row_layout_1.root_leaf = RootLeaf()
        # self.tree_row_layout_1.add_widget(self.tree_row_layout_1.root_leaf)

        # self.tree_row_layout_1.stone_leaf_1 = StoneLeaf('b')
        # self.tree_row_layout_1.add_widget(self.tree_row_layout_1.stone_leaf_1)
        #
        # self.tree_row_layout_1.stone_leaf_2 = StoneLeaf('w')
        # self.tree_row_layout_1.add_widget(self.tree_row_layout_1.stone_leaf_2)
        #
        # self.tree_row_layout_1.stone_leaf_3 = StoneLeaf('b')
        # self.tree_row_layout_1.add_widget(self.tree_row_layout_1.stone_leaf_3)
        #
        # self.tree_row_layout_1.stone_leaf_4 = StoneLeaf('w')
        # self.tree_row_layout_1.add_widget(self.tree_row_layout_1.stone_leaf_4)
        #
        # self.tree_row_layout_1.stone_leaf_5 = StoneLeaf('b')
        # self.tree_row_layout_1.add_widget(self.tree_row_layout_1.stone_leaf_5)
        #
        # self.tree_row_layout_1.stone_leaf_6 = StoneLeaf('w')
        # self.tree_row_layout_1.add_widget(self.tree_row_layout_1.stone_leaf_6)
        #
        # self.tree_row_layout_1.stone_leaf_7 = StoneLeaf('b')
        # self.tree_row_layout_1.add_widget(self.tree_row_layout_1.stone_leaf_7)
        #
        # self.tree_row_layout_1.stone_leaf_8 = StoneLeaf('w')
        # self.tree_row_layout_1.add_widget(self.tree_row_layout_1.stone_leaf_8)
        #
        # self.tree_row_layout_1.stone_leaf_9 = StoneLeaf('b')
        # self.tree_row_layout_1.add_widget(self.tree_row_layout_1.stone_leaf_9)
        #
        # self.tree_row_layout_1.stone_leaf_10 = StoneLeaf('w')
        # self.tree_row_layout_1.add_widget(self.tree_row_layout_1.stone_leaf_10)
        #
        # self.tree_row_layout_1.stone_leaf_11 = StoneLeaf('b')
        # self.tree_row_layout_1.add_widget(self.tree_row_layout_1.stone_leaf_11)
        #
        # self.tree_row_layout_1.stone_leaf_12 = StoneLeaf('w')
        # self.tree_row_layout_1.add_widget(self.tree_row_layout_1.stone_leaf_12)

        # self.tree_row_layout_1.resizeAfterChildren()

        # self.tree_row_layout_2 = TreeRowLayout()
        # self.add_widget(self.tree_row_layout_2)
        #
        # self.tree_row_layout_2.branch_leaf_1 = BranchLeaf('|')
        # self.tree_row_layout_2.add_widget(self.tree_row_layout_2.branch_leaf_1)
        #
        # self.tree_row_layout_2.empty_leaf_2 = EmptyLeaf()
        # self.tree_row_layout_2.add_widget(self.tree_row_layout_2.empty_leaf_2)
        #
        # self.tree_row_layout_2.empty_leaf_3 = EmptyLeaf()
        # self.tree_row_layout_2.add_widget(self.tree_row_layout_2.empty_leaf_3)
        #
        # self.tree_row_layout_2.branch_leaf_2 = BranchLeaf('L')
        # self.tree_row_layout_2.add_widget(self.tree_row_layout_2.branch_leaf_2)
        #
        # self.tree_row_layout_2.stone_leaf_1 = StoneLeaf('w')
        # self.tree_row_layout_2.add_widget(self.tree_row_layout_2.stone_leaf_1)
        #
        # self.tree_row_layout_2.stone_leaf_2 = StoneLeaf('b')
        # self.tree_row_layout_2.add_widget(self.tree_row_layout_2.stone_leaf_2)
        #
        # self.tree_row_layout_2.resizeAfterChildren()
        #
        # self.tree_row_layout_3 = TreeRowLayout()
        # self.add_widget(self.tree_row_layout_3)
        #
        # self.tree_row_layout_3.branch_leaf_1 = BranchLeaf('T')
        # self.tree_row_layout_3.add_widget(self.tree_row_layout_3.branch_leaf_1)
        #
        # self.tree_row_layout_3.stone_leaf_1 = StoneLeaf('b')
        # self.tree_row_layout_3.add_widget(self.tree_row_layout_3.stone_leaf_1)
        #
        # self.tree_row_layout_3.stone_leaf_2 = StoneLeaf('w')
        # self.tree_row_layout_3.add_widget(self.tree_row_layout_3.stone_leaf_2)
        #
        # self.tree_row_layout_3.resizeAfterChildren()
        #
        # self.tree_row_layout_4 = TreeRowLayout()
        # self.add_widget(self.tree_row_layout_4)
        #
        # self.tree_row_layout_4.branch_leaf_1 = BranchLeaf('|')
        # self.tree_row_layout_4.add_widget(self.tree_row_layout_4.branch_leaf_1)
        #
        # self.tree_row_layout_4.branch_leaf_2 = BranchLeaf('L')
        # self.tree_row_layout_4.add_widget(self.tree_row_layout_4.branch_leaf_2)
        #
        # self.tree_row_layout_4.stone_leaf_1 = StoneLeaf('w')
        # self.tree_row_layout_4.add_widget(self.tree_row_layout_4.stone_leaf_1)
        #
        # self.tree_row_layout_4.resizeAfterChildren()
        #
        # self.tree_row_layout_5 = TreeRowLayout()
        # self.add_widget(self.tree_row_layout_5)
        #
        # self.tree_row_layout_5.branch_leaf_1 = BranchLeaf('L')
        # self.tree_row_layout_5.add_widget(self.tree_row_layout_5.branch_leaf_1)
        #
        # self.tree_row_layout_5.stone_leaf_1 = StoneLeaf('b')
        # self.tree_row_layout_5.add_widget(self.tree_row_layout_5.stone_leaf_1)
        #
        # self.tree_row_layout_5.stone_leaf_2 = StoneLeaf('w')
        # self.tree_row_layout_5.add_widget(self.tree_row_layout_5.stone_leaf_2)
        #
        # self.tree_row_layout_5.stone_leaf_3 = StoneLeaf('b')
        # self.tree_row_layout_5.add_widget(self.tree_row_layout_5.stone_leaf_3)
        #
        # self.tree_row_layout_5.resizeAfterChildren()
        #
        # self.resizeAfterChildren()

        #####  /\  MANUAL LEAF LAYOUT FOR TESTING

        # Forces children to top instead of bottom.
        # self.add_widget(Widget())

    def resizeAfterChildren(self) -> None:
        self.height = 40 * len(self.children)
        self.width = max([c.width for c in self.children])


class TreeRowLayout(BoxLayout, util.Helper):
    def __init__(self):
        super(TreeRowLayout, self).__init__()
        self.orientation = 'horizontal'
        self.spacing = 0
        self.size_hint = [None, None]
        self.height = 40

    def resizeAfterChildren(self) -> None:
        self.size = [40 * len(self.children), 40]


####################################################################################################


class Leaf(ButtonBehavior, Widget, util.Helper):
    def __init__(self, front_leaf_i:int):
        super(Leaf, self).__init__()
        self.front_leaf_i = front_leaf_i
        self.size_hint = [None, None]
        self.size = [40, 40]

    def on_release(self) -> None:

        # print(f"\n{dir(self.app.main_window) = }\n")

        self.app.main_window.main_scroll.main_scroll_layout.board.resetBoard(
            self.data['back']['tree'].leaves[self.back_leaf_i].board_pos
        )

        for leaf in self.data['back']['tree'].leaves:
            if leaf.is_cur_board:  leaf.is_cur_board = False  ;  break

        self.data['back']['tree'].leaves[self.back_leaf_i].is_cur_board = True

        self.app.main_window.main_scroll.main_scroll_layout.tree.refreshLayout()

        self.data['input']['tree_options']['cur_back_leaf_i'] = self.back_leaf_i

        # print(f"\n{self.color_text = }\n")

        if self.leaf_type == 'stone':
            cur_stone_button_color = 'b' if self.color_text == 'w' else 'w'
        elif self.leaf_type == 'root':
            color = self.data['back']['tree'].leaves[self.back_leaf_i].stone_color
            cur_stone_button_color  = 'b' if color == 'w' else 'w'

        if self.data['input']['board_options']['next_stone_state'] == 'alternate':
            next_stone_button_color = 'b' if cur_stone_button_color == 'w' else 'w'
        else:
            next_stone_button_color = cur_stone_button_color


        self.app.main_window.main_scroll.main_scroll_layout.board_options.cur_next_stone_options.cur_stone_button.setColor(cur_stone_button_color)
        self.app.main_window.main_scroll.main_scroll_layout.board_options.cur_next_stone_options.next_stone_button.setColor(next_stone_button_color)



class RootLeaf(Leaf):
    def __init__(self, front_leaf_i:int, back_leaf_i:int, is_cur_board:bool=False):
        super(RootLeaf, self).__init__(front_leaf_i)
        self.leaf_type = 'root'
        self.back_leaf_i = back_leaf_i
        self.is_cur_board = is_cur_board
        self.is_cur_board_color = util.CLR_BOARD_YELLOW if self.is_cur_board else util.CLR_NOTHING
        self.setAndAddCanvasBeforeObjs()
        self.updateDisplay()
        self.bind(pos=self.updateDisplay, size=self.updateDisplay)

    def setAndAddCanvasBeforeObjs(self) -> None:
        with self.canvas.before:
            self.is_cur_board_rect_color = Color(*self.is_cur_board_color)
            self.is_cur_board_rect = Rectangle()
            self.tl_stone_color = Color(*util.CLR_BLACK)
            self.tl_stone = Ellipse()
            self.tr_stone_color = Color(*util.CLR_WHITE)
            self.tr_stone = Ellipse()
            self.bl_stone_color = Color(*util.CLR_WHITE)
            self.bl_stone = Ellipse()
            self.br_stone_color = Color(*util.CLR_BLACK)
            self.br_stone = Ellipse()

    def updateDisplay(self, *args) -> None:
        self.is_cur_board_rect.pos = self.pos
        self.is_cur_board_rect.size = self.size
        half = self.size[0] / 2
        self.tl_stone.pos = [self.pos[0], self.pos[1] + half]
        self.tl_stone.size = [half] * 2
        self.tr_stone.pos = [self.pos[0] + half, self.pos[1] + half]
        self.tr_stone.size = [half] * 2
        self.bl_stone.pos = self.pos
        self.bl_stone.size = [half] * 2
        self.br_stone.pos = [self.pos[0] + half, self.pos[1]]
        self.br_stone.size = [half] * 2


class StoneLeaf(Leaf):
    def __init__(self, front_leaf_i:int, back_leaf_i:int, color:str, is_cur_board:bool=False):
        super(StoneLeaf, self).__init__(front_leaf_i)
        self.leaf_type = 'stone'
        self.is_cur_board = is_cur_board
        self.is_cur_board_color = util.CLR_BOARD_YELLOW if self.is_cur_board else util.CLR_NOTHING
        self.back_leaf_i = back_leaf_i
        self.color_text = color
        self.color = util.CLR_BLACK if color == 'b' else util.CLR_WHITE
        self.setAndAddCanvasBeforeObjs()
        self.updateDisplay()
        self.bind(pos=self.updateDisplay, size=self.updateDisplay)

    def setAndAddCanvasBeforeObjs(self) -> None:
        with self.canvas.before:
            self.is_cur_board_rect_color = Color(*self.is_cur_board_color)
            self.is_cur_board_rect = Rectangle()
            self.stone_color = Color(*self.color)
            self.stone = Ellipse()

    def updateDisplay(self, *args) -> None:
        self.is_cur_board_rect.pos = self.pos
        self.is_cur_board_rect.size = self.size
        self.stone.pos = self.pos
        self.stone.size = self.size



class BranchLeaf(Leaf):
    def __init__(self, front_leaf_i:int, branch_type:str):
        super(BranchLeaf, self).__init__(front_leaf_i)
        self.leaf_type = 'branch'
        self.line_width = 1.1
        self.branch_type = branch_type
        self.setAndAddCanvasBeforeObjs()
        self.setLineType()
        self.updateDisplay()
        self.bind(pos=self.updateDisplay, size=self.updateDisplay)

    def setAndAddCanvasBeforeObjs(self) -> None:
        with self.canvas.before:
            self.top_line_color = Color(*util.CLR_WHITE)
            self.top_line = Line(width=self.line_width)
            self.right_line_color = Color(*util.CLR_WHITE)
            self.right_line = Line(width=self.line_width)
            self.bottom_line_color = Color(*util.CLR_WHITE)
            self.bottom_line = Line(width=self.line_width)

    def setLineType(self) -> None:
        colors = [util.CLR_BOARD_YELLOW] * 3
        if self.branch_type == 'L':  colors[2] = util.CLR_NOTHING
        elif self.branch_type == '|':  colors[1] = util.CLR_NOTHING
        self.top_line_color.rgba = colors[0]
        self.right_line_color.rgba = colors[1]
        self.bottom_line_color.rgba = colors[2]

    def setLinePoints(self) -> None:
        full = self.size[0]
        half = full / 2
        center = [self.pos[i] + half for i in range(2)]
        top = [self.pos[0] + half, self.pos[1] + full]
        right = [self.pos[0] + full, self.pos[1] + half]
        bottom = [self.pos[0] + half, self.pos[1]]
        self.top_line.points = [*center, *top]
        self.right_line.points = [*center, *right]
        self.bottom_line.points = [*center, *bottom]

    def updateDisplay(self, *args) -> None:
        self.setLinePoints()


class EmptyLeaf(Leaf):
    def __init__(self, front_leaf_i:int):
        super(EmptyLeaf, self).__init__(front_leaf_i)
