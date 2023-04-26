

def main() -> None:

    tree = Tree()

    print(f"\n{tree.tree = }")

    tree.addLeaf([1, 3])
    tree.addLeaf([1, 3, 6])
    tree.addLeaf([2])

    print(f"\n{tree.tree = }")

    return


####################################################################################################


class Tree():
    def __init__(self):
        self.root_leaf = None
        # self.front_layout = None
        self.next_leaf = 6
        self.tree = {
            'root': {
                1: {
                    3: {
                        5: {}
                    },
                    4: {}
                },
                2: {}
            }
        }

    def addLeaf(self, path_to_parent:list[int]) -> None:
        cur_leaf = self.tree['root']
        for leaf in path_to_parent:  cur_leaf = cur_leaf[leaf]
        cur_leaf[self.next_leaf] = {}
        self.next_leaf += 1



class Leaf():
    def __init__(self):
        self.cur_board_pos = None
        self.coord = None
        self.y = None
        self.x = None
        self.color = None
        self.char = None
        self.move_number = None
        self.children = None
        self.leaf_i = None
        self.path_from_root = None


####################################################################################################


if __name__ == '__main__':  main()

