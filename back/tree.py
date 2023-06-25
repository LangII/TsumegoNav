

from __future__ import annotations
import sys
new_path = __file__
for _ in range(2):  new_path = new_path[:new_path.rfind('/')]
sys.path += [new_path]

import json
from copy import deepcopy

from kivy.logger import Logger

import util
import back.board as back_board


####################################################################################################


NAME = util.getNameFromFile(__file__)


####################################################################################################


def main() -> None:

    tree = Tree()

    print(f"\n{tree.tree = }")

    tree.refreshFrontTreeMap()

    tree.printFrontTreeMap()

    return


####################################################################################################


class Tree(util.Helper):
    def __init__(self):
        super(Tree, self).__init__()
        Logger.info(f"{NAME}: init Tree")
        board_pos = self.data['input']['cur_problem'] if self.data else None
        self.leaves = [Leaf(self, is_root=True, is_cur_board=True, back_leaf_i=0, board_pos=board_pos)]
        self.next_leaf = 1
        self.tree = {0: {}}
        self.front_tree_map = []

    def addLeaf(self, path_to_parent:list[int], leaf_kwargs:dict) -> None:
        cur_leaf = self.tree
        for leaf in path_to_parent:  cur_leaf = cur_leaf[leaf]
        cur_leaf[self.next_leaf] = {}
        leaf_kwargs['back_leaf_i'] = self.next_leaf
        new_leaf = Leaf(self, **leaf_kwargs)
        self.leaves += [new_leaf]
        self.leaves[new_leaf.parent_leaf_i].setChildrenSiblingI()
        self.next_leaf += 1
        self.refreshFrontTreeMap()

    def moveLeaf(self, path_to_parent:list[int], leaf:int, move:str) -> None:
        """ Move a leaf up, down, to top, or to bottom through its sibling list. """
        # get leaf siblings (keys)
        cur_leaf = self.tree
        for l in path_to_parent:  cur_leaf = cur_leaf[l]
        keys = list(cur_leaf.keys())
        # get leaf pos
        leaf_i = keys.index(leaf)
        # handle bad moves
        if (
            (move in ['up', 'to_top'] and leaf_i == 0)
            or (move in ['down', 'to_bottom'] and leaf_i == len(keys))
        ):
            Logger.warning(f"{NAME}: Tree.moveLeaf leaf is unable to move '{warning_type}'")
            return
        # get new pos of leaf
        new_leaf_i = None
        if move == 'up':  new_leaf_i = leaf_i - 1
        elif move == 'down':  new_leaf_i = leaf_i + 1
        elif move == 'top':  new_leaf_i = 0
        elif move == 'bottom':  new_leaf_i = -1
        # do the move and update whole tree
        new_keys = deepcopy(keys)
        new_keys.insert(new_leaf_i, new_keys.pop(leaf_i))
        cur_leaf_2 = self.tree
        for leaf in path_to_parent[:-1]:  cur_leaf_2 = cur_leaf_2[leaf]
        cur_leaf_2[path_to_parent[-1]] = {k: cur_leaf[k] for k in new_keys}
        self.refreshFrontTreeMap()

    def refreshFrontTreeMap(self) -> None:
        # recursively flatten tree
        def recurse(d:dict, layer:int=0) -> list:
            tree_map = []
            if not d.keys():  return ['\n']
            for k in d.keys():
                if tree_map and tree_map[-1] == '\n':  tree_map += [' '] * layer
                tree_map += [k, *recurse(d[k], layer + 1)]
            return tree_map
        tree_map = recurse(self.tree)
        # reshape to 2D
        self.front_tree_map = [[]]
        cur_row = 0
        for leaf_pos in tree_map[:-1]:
            if leaf_pos == '\n':
                self.front_tree_map += [[]]
                cur_row += 1
                continue
            self.front_tree_map[cur_row] += [leaf_pos]
        # add Ls
        prev_row_len = 0
        all_the_Ls = []
        for y, row in enumerate(self.front_tree_map):
            for x, leaf_pos in enumerate(row):
                cur_value = self.front_tree_map[y][x]
                cur_right_value = self.front_tree_map[y][x + 1] if x < len(row) - 1 else None
                if cur_value == ' ' and type(cur_right_value) == int:
                    self.front_tree_map[y][x] = 'L'
                    all_the_Ls += [[y, x]]
            prev_row_len = len(row)
        # add Ts and |s
        for y, x in all_the_Ls[::-1]:
            if self.front_tree_map[y][x] != 'L':  continue
            for new_y in list(range(1, y))[::-1]:
                new_value = self.front_tree_map[new_y][x]
                if type(new_value) == int:  break
                if new_value == 'L':  update = 'T'
                elif new_value == ' ':  update = '|'
                self.front_tree_map[new_y][x] = update

    def updateLeavesIsCurBoard(self, new_is_cur_board_leaf_i:int) -> None:
        for leaf in self.leaves:
            if leaf.is_cur_board:  leaf.is_cur_board = False  ;  break
        self.leaves[new_is_cur_board_leaf_i].is_cur_board = True

    def printLeaves(self) -> None:
        for leaf in self.leaves:
            print(f"\nis_root        = {leaf.is_root}")
            print(f"back_leaf_i    = {leaf.back_leaf_i}")
            print(f"front_leaf_i   = {leaf.front_leaf_i}")
            print(f"parent_leaf_i  = {leaf.parent_leaf_i}")
            print(f"is_cur_board   = {leaf.is_cur_board}")
            print(f"move_count     = {leaf.move_count}")
            print(f"stone_color    = {leaf.stone_color}")
            print(f"stone_pos      = {leaf.stone_pos}")
            print(f"board_pos      = {leaf.board_pos}")
            print(f"children       = {leaf.children}")
            print(f"path_to_parent = {leaf.path_to_parent}")
            print(f"path_to_self   = {leaf.path_to_self}")
            print(f"sibling_i      = {leaf.sibling_i}")

    def printTree(self, type:str='flat') -> None:
        if type == 'flat':  print(f"\n{self.tree = }")
        elif type == 'json':  print(f"\nself.tree = {json.dumps(self.tree, indent=4, default=str)}")

    def printFrontTreeMap(self) -> None:
        if not self.front_tree_map:  print("\nself.front_tree_map = []")  ;  return
        pad = len(str(max([x if type(x) == int else 0 for x in sum(self.front_tree_map, [])])))
        front_tree_map = [[str(x).rjust(pad, ' ') for x in row] for row in self.front_tree_map]
        print("\nself.front_tree_map = [")
        for row in front_tree_map:  print(f"\t{' '.join(row)}")
        print("]")


class Leaf(util.Helper):
    def __init__(
        self,
        tree:Tree,
        is_root:bool=False,
        back_leaf_i:int=None,
        front_leaf_i:int=None,
        parent_leaf_i:int=None,
        is_cur_board:bool=None,
        stone_color:str=None,
        move_count:int=None,
        stone_pos:list[int]=None,
        board_pos:dict[list[list]]=None,
        ko:list[int]=None,
        captures:dict[int]=None,
    ):
        super(Leaf, self).__init__()
        Logger.info(f"{NAME}: init Leaf {back_leaf_i}")
        self.tree = tree
        self.is_root = is_root
        self.back_leaf_i = back_leaf_i
        self.front_leaf_i = front_leaf_i
        self.is_cur_board = is_cur_board
        self.stone_color = stone_color
        self.stone_char = back_board.SETTINGS['black_char'] if self.stone_color == 'b' else back_board.SETTINGS['white_char']
        self.move_count = move_count
        self.stone_pos = stone_pos
        self.board_pos = board_pos
        self.ko = ko
        self.captures = captures
        self.children = []
        self.sibling_i = []
        if self.is_root:
            self.move_count = 0
            self.stone_color = 'w'
            self.parent_leaf_i = None
            self.stone_pos = None
            self.path_to_parent = None
            self.path_to_self = [0]
            self.sibling_i = None
        else:
            self.parent_leaf_i = parent_leaf_i
            self.path_to_parent = self.tree.leaves[self.parent_leaf_i].path_to_self
            self.path_to_self = self.path_to_parent + [self.back_leaf_i]
            self.tree.leaves[self.parent_leaf_i].children += [self.back_leaf_i]

    def setSiblingI(self) -> None:
        self.sibling_i = [c for c in self.tree.leaves[self.parent_leaf_i].children if c != self.back_leaf_i]

    def setChildrenSiblingI(self) -> None:
        for child_i in self.children:  self.tree.leaves[child_i].setSiblingI()


####################################################################################################


if __name__ == '__main__':  main()











































