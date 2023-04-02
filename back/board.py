

import sys
new_path = __file__
for _ in range(2):  new_path = new_path.rfind('/')
sys.path += [new_path]

import util


####################################################################################################


SETTINGS = {

    # 'size': 19,
    'size': 9,

    'black_char': '#',
    'white_char': 'O',
    'no_char': '-',
}


####################################################################################################


def main():
    board = Board()

    # board.resetBoard({
    #     'b': [[15, 16], [ 2, 15], [16,  5]],
    #     'w': [[15,  3], [ 3,  3]],
    # })
    board.resetBoard({
        'b': [[2, 3], [3, 3], [3, 4], [3, 5], [3, 6], [4, 6], [6, 3], [7, 3], [6, 4], [3, 1]],
        'w': [],
    })

    board.printBoard()
    print(f"\n{board.stones = }")

    board.setGroups()
    print(f"\n{board.groups = }")


####################################################################################################


class Board():
    """
    NOTES:
    - All board coordinates are represented in the form of '[y, x]'.  Where 'y' represents the
    vertical coordinate starting at '0' in the top-left, and ending at 'self.size - 1' in the
    bottom-left.  And 'x' represents the horizontal coordinate start at '0' in the top-left, and
    ending at 'self.size - 1' in the top-right.
    """
    def __init__(self, settings:dict=SETTINGS):
        self.size = settings['size']
        self.black_char = settings['black_char']
        self.white_char = settings['white_char']
        self.no_char = settings['no_char']
        self.board = []
        self.stones = {'b': [], 'w': []}
        self.resetBoard()

    def printBoard(self) -> None:
        print("")
        for row in self.board:  print(' '.join(row))

    def resetBoard(self, presets:dict[list[list]]=None) -> None:
        presets = presets if presets else {}
        self.board = [[self.no_char for y in range(self.size)] for x in range(self.size)]
        for color, presets in presets.items():
            char = self.black_char if color.lower() == 'b' else self.white_char
            for y, x in presets:  self.board[y][x] = char
        self.setStones()

    def setStones(self) -> None:
        self.stones = {'b': [], 'w': []}
        for y, row in enumerate(self.board):
            for x, stone in enumerate(row):
                if stone == self.black_char:  self.stones['b'] += [[y, x]]
                elif stone == self.white_char:  self.stones['w'] += [[y, x]]

    def setGroups(self) -> None:
        """
        NOTES:
        - Must be called after 'setStones', 'setGroups' is dependent on an updated 'self.stones'.
        """
        self.groups = {'b': [], 'w': []}
        for color, stones in self.stones.items():
            if not stones:  continue
            # 'group_labels' is a parallel array to 'stones'.  Where each value is an int and each
            # int value represents a group.  Examples:
            # [1, 1] = 1 group:  1 group of 2 stones
            # [1, 1, 2] = 2 groups:  1 group of 2 stones and 1 group of 1 stone
            # [1, 1, 2, 3] = 3 groups:  1 group of 2 stones, 1 group of 1 stone, and 1 group of 1 stone
            group_labels = [0] * len(stones)
            new_label = 1
            for i, stone in enumerate(stones):
                # Assign new label to stone, if stone has yet to be labelled.
                if group_labels[i] == 0:
                    group_labels[i] = new_label
                    new_label += 1
                # Inner loop compares outer loop 'stone' with all other 'stones'.
                for other_i, other_stone in enumerate(stones):
                    if i == other_i:  continue
                    # If inner loop stone is a neighbor to the outer loop stone...
                    if stone in self.getStoneNeighbors(other_stone):
                        # If inner loop stone has yet to be labelled, then inner loop stone is
                        # labelled with out loop stones label.
                        if group_labels[other_i] == 0:
                            group_labels[other_i] = group_labels[i]
                        # If inner loop stone has already been labelled, then all stones previously
                        # labelled with outer loop stone's label, get their labels reassigned to the
                        # inner loop stone's label.
                        else:
                            new_labels = []
                            for group_label in group_labels:
                                if group_label == group_labels[i]:  new_labels += [group_labels[other_i]]
                                else:  new_labels += [group_label]
                            group_labels = new_labels
            # The actual 'groups' are now created that 'group_labels' has been generated.
            for master_label in set(group_labels):
                stones_to_group = []
                for i, label in enumerate(group_labels):
                    if master_label == label:
                        stones_to_group += [self.stones[color][i]]
                self.groups[color] += [stones_to_group]
                # self.groups[color] += [Group(stones_to_group)]
                """
                TURNOVER NOTES:
                - Implement the use of Group() as a class.  ^
                """

    def getStoneNeighbors(self, coord:list[int]) -> list[list[int]]:
        if type(coord) == 'str':  coord = util.convStrListCoordToListCoord(coord)
        y, x = coord
        neighbors = [
            [y - 1, x    ] if y != 0             else None,
            [y    , x - 1] if x != 0             else None,
            [y + 1, x    ] if y != self.size - 1 else None,
            [y    , x + 1] if x != self.size - 1 else None,
        ]
        return [n for n in neighbors if n]




####################################################################################################





####################################################################################################


if __name__ == '__main__':  main()



















