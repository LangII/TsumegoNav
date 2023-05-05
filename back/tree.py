

####################################################################################################


from __future__ import annotations
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

    # tree.addLeaf([2, 8, 9])

    tree.moveLeaf([1], 5, 'up')

    print(f"\n{tree.tree = }")

    return


####################################################################################################


class Tree(util.Helper):
    def __init__(self):
        super(Tree, self).__init__()

        Logger.info(f"{NAME}: init Tree")

        self.leaves = [Leaf(self, is_root=True, leaf_i=0, board_pos=self.data['back']['board'].stones)]
        self.next_leaf = 1

        self.tree = {
            0: {
                # 1: {
                #     4: {
                #         6: {
                #             7: {},
                #         },
                #     },
                #     5: {},
                # },
                # 2: {
                #     8: {
                #         9: {
                #             12: {
                #                 13: {},
                #             },
                #         },
                #     },
                #     10: {},
                #     11: {},
                # },
                # 3: {},
            }
        }

    def addLeaf(self, path_to_parent:list[int], leaf_kwargs:dict) -> None:
        cur_leaf = self.tree
        for leaf in path_to_parent:  cur_leaf = cur_leaf[leaf]
        cur_leaf[self.next_leaf] = {}

        leaf_kwargs['leaf_i'] = self.next_leaf

        self.leaves += [Leaf(self, **leaf_kwargs)]

        self.next_leaf += 1

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



class Leaf(util.Helper):
    def __init__(
        self,
        tree:Tree,
        is_root:bool=False,
        leaf_i:int=None,
        stone_color:str=None,
        move_count:int=None,
        stone_pos:list[int]=None,
        board_pos:dict[list[list]]=None,
        ko:list[int]=None,
        captures:dict[int]=None,
        parent_leaf_i:int=None
    ):

        super(Leaf, self).__init__()
        Logger.info(f"{NAME}: init Leaf {leaf_i}")

        self.tree = tree
        self.is_root = is_root
        self.leaf_i = leaf_i
        self.stone_color = stone_color
        self.stone_char = back_board.SETTINGS['black_char'] if self.stone_color == 'b' else back_board.SETTINGS['white_char']
        self.move_count = move_count
        self.stone_pos = stone_pos
        self.board_pos = board_pos
        self.ko = ko
        self.captures = captures

        self.children = []

        if self.is_root:
            self.move_count = 0
            self.stone_color = 'w'
            self.path_to_self = [0]
            self.board_pos = self.data['back']['board'].stones
            return

        self.parent_leaf_i = parent_leaf_i
        self.path_to_parent = self.tree.leaves[self.parent_leaf_i].path_to_self
        self.path_to_self = self.path_to_parent + [self.leaf_i]
        self.sibling_i = len(self.tree.leaves[self.parent_leaf_i].children)

        self.tree.leaves[self.parent_leaf_i].children += [self.leaf_i]


        # self.children = None
        # self.leaf_i = None
        #
        # self.cur_board_pos = None
        # self.coord = None
        # self.y = None
        # self.x = None
        # self.color = None
        # self.char = None
        # self.move_number = None
        # self.path_from_root = None


####################################################################################################


if __name__ == '__main__':  main()

