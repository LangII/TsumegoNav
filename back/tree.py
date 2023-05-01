

####################################################################################################


import json
from copy import deepcopy

from kivy.logger import Logger


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


class Tree():
    def __init__(self):

        Logger.info(f"{NAME}: init Tree")

        self.root_leaf = None
        # self.front_layout = None
        self.next_leaf = 14

        self.tree = {
            'root': {
                1: {
                    4: {
                        6: {
                            7: {},
                        },
                    },
                    5: {},
                },
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

    def addLeaf(self, path_to_parent:list[int]) -> None:
        cur_leaf = self.tree['root']
        for leaf in path_to_parent:  cur_leaf = cur_leaf[leaf]
        cur_leaf[self.next_leaf] = {}
        self.next_leaf += 1

    def moveLeaf(self, path_to_parent:list[int], leaf:int, move:str) -> None:
        """ Move a leaf up, down, to top, or to bottom through its sibling list. """

        # get leaf siblings (keys)
        cur_leaf = self.tree['root']
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
        cur_leaf_2 = self.tree['root']
        for leaf in path_to_parent[:-1]:  cur_leaf_2 = cur_leaf_2[leaf]
        cur_leaf_2[path_to_parent[-1]] = {k: cur_leaf[k] for k in new_keys}



class Leaf():
    def __init__(self):

        self.children = None
        self.leaf_i = None

        self.cur_board_pos = None
        self.coord = None
        self.y = None
        self.x = None
        self.color = None
        self.char = None
        self.move_number = None
        self.path_from_root = None


####################################################################################################


if __name__ == '__main__':  main()

