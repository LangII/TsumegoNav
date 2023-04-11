

from kivy.logger import Logger
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import ButtonBehavior
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle

import util


####################################################################################################


NAME = util.getNameFromFile(__file__)


####################################################################################################


class Tree(ScrollView, util.Helper):
    def __init__(self):
        super(Tree, self).__init__()
        Logger.info(f"{NAME}: init Tree")
        # self.size_hint = [1.0, 1.0]

        self.size_hint = [1.0, None]
        self.height = 200
        self.padding = util.PAD_V_MAIN_BOTTOM
        self.setAndAddCanvasBeforeObjs()
        self.updateDisplay()
        self.bind(pos=self.updateDisplay, size=self.updateDisplay)

        self.tree_layout = TreeLayout()
        self.add_widget(self.tree_layout)

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
            self.size[1] - self.padding[1] - self.padding[1]
        ]


class TreeLayout(BoxLayout, util.Helper):
    def __init__(self):
        super(TreeLayout, self).__init__()
        Logger.info(f"{NAME}: init TreeLayout")
        self.orientation = 'vertical'
        self.spacing = 0

        self.size_hint = [1.0, 1.0]

        self.tree_row_layout = TreeRowLayout()
        self.add_widget(self.tree_row_layout)

        # Forces children to top instead of bottom.
        self.add_widget(Widget())


class TreeRowLayout(BoxLayout, util.Helper):
    def __init__(self):
        super(TreeRowLayout, self).__init__()
        self.orientation = 'horizontal'
        self.spacing = 0

        self.size_hint = [1.0, None]
        self.height = 40

        self.stone_leaf = StoneLeaf()
        self.add_widget(self.stone_leaf)


    #     self.setAndAddCanvasBeforeObjs()
    #     self.updateDisplay()
    #     self.bind(pos=self.updateDisplay, size=self.updateDisplay)
    #
    # def setAndAddCanvasBeforeObjs(self) -> None:
    #     with self.canvas.before:
    #         self.rect_color = Color(*util.CLR_BOARD_YELLOW)
    #         self.rect = Rectangle()
    #
    # def updateDisplay(self, *args) -> None:
    #     self.rect.pos = self.pos
    #     self.rect.size = self.size


####################################################################################################


class Leaf(ButtonBehavior, Widget, util.Helper):
    def __init__(self):
        super(Leaf, self).__init__()

        self.size_hint = [None, None]
        self.size = [40, 40]

        self.setAndAddCanvasBeforeObjs()
        self.updateDisplay()
        self.bind(pos=self.updateDisplay, size=self.updateDisplay)

    def setAndAddCanvasBeforeObjs(self) -> None:
        with self.canvas.before:
            self.rect_color = Color(*util.CLR_PRISMARINE)
            self.rect = Rectangle()

    def updateDisplay(self, *args) -> None:
        self.rect.pos = self.pos
        self.rect.size = self.size

        print(f"\n{self.rect.pos = }")
        print(f"{self.rect.size = }")


class StoneLeaf(Leaf):
    def __init__(self):
        super(StoneLeaf, self).__init__()


class BranchLeaf(Leaf):
    def __init__(self):
        super(Branchleaf, self).__init__()


class EmptyLeaf(Leaf):
    def __init__(self):
        super(EmptyLeaf, self).__init__()
