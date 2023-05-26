

"""
The design of this App is inspired by https://tsumego.tasuki.org/.  A tsumego collection that
intentionally provides no solutions.  The reason is that it is believed you get stronger by solving
and then doing the work to verify the solution for yourself, rather than by solving and just simply
confirming.

Yes, this method of studying tsumego did prove to be more advantageous for me personally.  But, the
process of solving was noticeably more time consuming.  I felt that there was the potential for a
player to become stronger faster, if they studied tsumego via this method AND had a convenient
time saving tool to do so.  That is the purpose of this App:  To make studying solutionless-tsumego
easier and faster.

---

"It is a matter of life and death, a road either to safety or to ruin.  Hence it is a subject of
inquiry which can on no account be neglected."
- Sun Tzu:  The Art of War

"The problems come without solutions for two reasons:  first, one can learn more by reading out all
the paths and solving the problems oneself; second, the solutions are copyrighted."
- Vit Brunner

"Don't look at the solutions!!!"
- Benjamin Teuber
"""


"""
TURNOVER NOTES:

2023-03-17
- Next to do is make a board.  Review board from GoCalc for references...  Good luck!

2023-05-11

- Doing very good at building Front Tree and making it interactive with Front Board, Back Board, and
Back Tree.  "Doing very good", yes functional, but still very dirty.  Need to clean!

DONE
- Next is make it so user can click on Leaves in Front Tree and have the Front Board update to the
board position of the Front Tree Leaf clicked on.
DONE

- Then update Front Board so a Symbol appears on Stone of 'stone_pos' of Front Tree Cur Leaf.  Be
sure to make Symbol dynamic.

IN REVIEW / CLEAN UP
- Also need to make it so that if on a Leaf that already has children leaves, the user can click
on a Front Board position that is already a child, and the Front Board and Front Tree, instead of
creating a new Leaf, will just take the user to Leaf of clicked board position.
IN REVIEW / CLEAN UP

2023-05-22

- Implement the use of back board for illegal moves.
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
from front.board import Board as FrontBoard
from front.tree import Tree as FrontTree
from back.board import Board as BackBoard
from back.tree import Tree as BackTree


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
        'cur_problem': {
            'b': [[2, 2], [2, 3], [2, 4], [2, 5], [1, 7], ],
            'w': [[1, 1], [1, 2], [1, 3], [1, 4], [1, 5], ]
        },
        'board_options': {
            'cur_stone': 'black',  # 'black' or 'white'
            'next_stone': 'white',  # 'black' or 'white'
            'next_stone_state': 'alternate',  # 'alternate' or 'consecutive'
        },
        'tree_options': {
            'cur_back_leaf_i': 0,
            # 'cur_front_leaf_i': 0,
        },
    },
    'back': {
        'board': None,
        'tree': None,
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
    def __init__(self):
        super(MainApp, self).__init__()
        self.data = DATA
        self.title = util.PROJECT_NAME
        self.main_window = None
        Window.size = self.data['window']['size_default']
        Window.clearcolor = util.CLR_PRISMARINE
        Window.bind(on_key_down=self.keyboardInput)

        self.data['back']['board'] = BackBoard()
        self.data['back']['tree'] = BackTree()

    def build(self):
        self.main_window = MainWindow()
        self.main_window.main_scroll.main_scroll_layout.tree.refreshLayout()
        return self.main_window

    #####  \/  IN APP TESTING

    def keyboardInput(self, obj:WindowSDL, num1:int, num2:int, text:str, *args) -> None:
        Logger.info(f"{NAME}: keyboardInput text = '{text}'")
        if text == ' ':  self.spaceBarInput()
        if text in ['w', 'a', 's', 'd']:  self.wasdInput(text)

    def spaceBarInput(self) -> None:
        print("")
        print(f"{Window.mouse_pos = }")

        # var1 = self.main_window.main_scroll.main_scroll_layout.tree.tree_scroll.viewport_size
        # var2 = self.main_window.main_scroll.main_scroll_layout.tree.tree_layout.size
        print("")
        # print(f"{self.data['back']['tree'].tree = }")
        # print(f"{self.data['back']['tree'].leaves[1].stone_pos = }")
        # print(f"{var2 = }")
        self.data['back']['tree'].printLeaves()
        # self.data['back']['tree'].printTree()
        # front_tree_leaves = self.main_window.main_scroll.main_scroll_layout.tree.leaves
        # print(f"{front_tree_leaves = }")

    def wasdInput(self, key:str) -> None:

        if key == 'a':

            cur_leaf_i = self.data['input']['tree_options']['cur_back_leaf_i']
            if cur_leaf_i == 0:  return
            back_tree = self.data['back']['tree']
            front_board = self.main_window.main_scroll.main_scroll_layout.board
            cur_parent_leaf = back_tree.leaves[back_tree.leaves[cur_leaf_i].parent_leaf_i]

            front_board.resetBoard(cur_parent_leaf.board_pos)

            back_tree.leaves[cur_leaf_i].is_cur_board = False
            cur_parent_leaf.is_cur_board = True
            self.main_window.main_scroll.main_scroll_layout.tree.refreshLayout()

            self.data['input']['tree_options']['cur_back_leaf_i'] = cur_parent_leaf.back_leaf_i

            self.main_window.main_scroll.main_scroll_layout.board_options.cur_next_stone_options.cur_stone_button.cycleColor()
            self.main_window.main_scroll.main_scroll_layout.board_options.cur_next_stone_options.next_stone_button.cycleColor()

        elif key == 's':

            cur_leaf_i = self.data['input']['tree_options']['cur_back_leaf_i']
            if cur_leaf_i == 0:  return
            back_tree = self.data['back']['tree']
            front_board = self.main_window.main_scroll.main_scroll_layout.board
            cur_parent_leaf = back_tree.leaves[back_tree.leaves[cur_leaf_i].parent_leaf_i]

            cur_sibling_pos = cur_parent_leaf.children.index(cur_leaf_i)
            next_sibling_i = 0 if cur_sibling_pos == len(cur_parent_leaf.children) - 1 else cur_sibling_pos + 1

            next_leaf_i = cur_parent_leaf.children[next_sibling_i]
            next_leaf = back_tree.leaves[next_leaf_i]

            front_board.resetBoard(next_leaf.board_pos)

            self.data['input']['tree_options']['cur_back_leaf_i'] = next_leaf.back_leaf_i

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

        # presets = {
        #     'b': [[2, 2], [2, 3], [2, 4], [2, 5], [1, 7],],
        #     'w': [[1, 1], [1, 2], [1, 3], [1, 4], [1, 5],]
        # }
        # for color, coords in presets.items():
        #     for coord in coords:
        #         self.main_scroll.main_scroll_layout.board.buttons[str(coord)].setStoneColor(color)
        # self.data['back']['board'].resetBoard(presets)

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
            self.main_scroll_layout.board.main_scroll_bar_pad = 0
        else:
            self.main_scroll_layout.padding = [0, 0, self.bar_width + util.PAD_MAIN, 0]
            self.main_scroll_layout.board.main_scroll_bar_pad = self.bar_width + util.PAD_MAIN

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

        self.board = FrontBoard()
        self.add_widget(self.board)

        self.tree = FrontTree()
        self.add_widget(self.tree)
        self.tree.refreshLayout()

        self.bind(
            pos=self.board.updateDisplay,
            size=self.board.updateDisplay,
            # Not sure why this is needed, but the example in the docs has it.  \_(**)_/
            minimum_height=self.setter('height')
        )


####################################################################################################


if __name__ == '__main__':  main()

