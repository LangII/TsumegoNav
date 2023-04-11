

class Tree():
    def __init__(self):
        self.root = None
        self.front_layout = None


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
