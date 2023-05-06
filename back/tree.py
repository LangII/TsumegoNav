

####################################################################################################


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
    tree.tree = {
        0: {
            1: {
                2: {
                    3: {
                        4: {
                            5: {
                                16: {
                                    17: {},
                                },
                            },
                        },
                    },
                    8: {},
                    9: {
                        10: {},
                    },
                },
            },
            6: {
                12: {
                    14: {},
                    15: {},
                },
                13: {},
            },
            7: {
                11: {},
            },
        },
    }

    print(f"\n{tree.tree = }")

    tree.refreshFrontTreeMap()

    tree.printFrontTreeMap()

    return


####################################################################################################


class Tree(util.Helper):
    def __init__(self):
        super(Tree, self).__init__()

        Logger.info(f"{NAME}: init Tree")

        if self.data:  board_pos = self.data['back']['board'].stones
        else:  board_pos = None
        self.leaves = [Leaf(self, is_root=True, leaf_i=0, board_pos=board_pos)]
        self.next_leaf = 1
        self.tree = {0: {}}
        self.front_tree_map = []

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

    def printLeaves(self) -> None:
        for leaf in self.leaves:
            print(f"\nis_root       = {leaf.is_root}")
            print(f"leaf_i        = {leaf.leaf_i}")
            print(f"parent_leaf_i = {leaf.parent_leaf_i}")
            print(f"move_count    = {leaf.move_count}")
            print(f"stone_color   = {leaf.stone_color}")
            print(f"stone_pos     = {leaf.stone_pos}")
            print(f"board_pos     = {leaf.board_pos}")
            print(f"children      = {leaf.children}")

    def printTree(self) -> None:
        print(f"\n{self.tree = }")
        # print(json.loads(self.tree, indent=4))





    def refreshFrontTreeMap(self) -> None:

        tree = deepcopy(self.tree)

        self.front_tree_map = [[]]

        leaves_placed = []

        # First, create the complete first row.
        cur_layer = tree
        while True:
            if len(cur_layer.keys()) == 0:  break
            cur_first_key = list(cur_layer.keys())[0]
            self.front_tree_map[0] += [cur_first_key]
            leaves_placed += [cur_first_key]
            cur_layer = cur_layer[cur_first_key]

        # Second, create the rest of the rows that have a leaf in the 1st layer.
        for key in list(tree[0].keys())[1:]:
            self.front_tree_map += [[' ', key]]







    def printFrontTreeMap(self) -> None:
        pad = len(str(max([x if type(x) == int else 0 for x in sum(self.front_tree_map, [])])))
        front_tree_map = [[f'{x: {pad}d}' if type(x) == int else ' ' * pad for x in row] for row in self.front_tree_map]
        print("\nself.front_tree_map = [")
        for row in front_tree_map:
            print(f"\t{' '.join(row)}")
        print("]")


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
            self.parent_leaf_i = None
            self.stone_pos = None
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


# if __name__ == '__main__':  main()





this = {
    0: {
        1: {
            2: {
                3: {
                    4: {
                        5: {
                            16: {
                                17: {},
                            },
                        },
                    },
                },
                8: {},
                9: {
                    10: {},
                },
            },
        },
        6: {
            12: {
                14: {},
                15: {},
            },
            13: {},
        },
        7: {
            11: {},
        },
    },
}

that = []

# for k1 in this.keys():
#     that += [k1]
#     for k2 in this[k1].keys():
#         that += [k2]
#         for k3 in this[k1][k2].keys():
#             that += [k3]
#             for k4 in this[k1][k2].keys():
#                 that += [k4]

def shit(d=None, layer=None):
    print(f"\n{d = }")
    print(f"{layer = }")
    damnit = []
    if not d.keys():  return [None]
    for k in d.keys():


        new_damnit = shit(d[k], layer + 1)
        # new_damnit, end_of_line = shit(d[k], layer + 1)
        # print(f"{new_damnit = }")
        # damnit += new_damnit

        # if new_damnit[-1] == '\n':
        #     print("end_of_line")
        #     damnit += [' '] * (layer - 1)

        if damnit and damnit[-1] is None:
            damnit += [' '] * layer

        print(f"{k = }")
        print(f"{damnit = }")
        print(f"{layer = }")
        damnit += [k]

        damnit += new_damnit


    return damnit

def more_shit(damnit):
    more_damnit = [[]]
    cur_row = 0
    for d in damnit[:-1]:
        if d is None:
            more_damnit += [[]]
            cur_row += 1
            continue
        more_damnit[cur_row] += [d]
    return more_damnit

# def more_more_shit(more):
#     shit = []
#     for row in

that = shit(this, 0)
that = more_shit(that)
# that = more_more_shit(that)

print(f"\n{this = }")
print("")
for row in that:  print(row)
# print(f"\n{that = }")

"""
2023-05-06
TURNOVER NOTES:
- This ^ is it!!!  Do not lose this!  Yes, it's super ugly.  But this is how to get front_tree_map!
- Next to do is clean up, get it out of this unit test, and implement!
"""
















































