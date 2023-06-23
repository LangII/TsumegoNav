

from __future__ import annotations
import sys
new_path = __file__
for _ in range(2):  new_path = new_path[:new_path.rfind('/')]
sys.path += [new_path]

from copy import deepcopy
import json

from kivy.logger import Logger

import util


####################################################################################################


NAME = util.getNameFromFile(__file__)

SETTINGS = {
    'size': 19,
    'black_char': 'X',
    'white_char': 'O',
    'no_char': '-',
    'ko_char': '+',
}


####################################################################################################


def main():

    back_board = Board()

    back_board.resetBoard({
        'b': [[2, 2], [2, 3], [2, 4], [2, 5], [1, 7], [2, 0], [0, 6],],
        'w': [[1, 1], [1, 2], [1, 3], [1, 4], [1, 5], ]
    })

    back_board.printVars()

    back_board.printBoard()

    return


####################################################################################################


class Board(util.Helper):
    """
    NOTES:
    - All board coordinates are represented in the form of '[y, x]'.  Where 'y' represents the
    vertical coordinate starting at '0' in the top-left, and ending at 'self.size - 1' in the
    bottom-left.  And 'x' represents the horizontal coordinate start at '0' in the top-left, and
    ending at 'self.size - 1' in the top-right.
    """
    def __init__(self, settings:dict=SETTINGS):
        super(Board, self).__init__()
        Logger.info(f"{NAME}: init Board")
        self.size = settings['size']
        self.black_char = settings['black_char']
        self.white_char = settings['white_char']
        self.no_char = settings['no_char']
        self.ko_char = settings['ko_char']
        self.board = []
        self.captures = {'b': 0, 'w': 0}
        self.ko = None
        self.board_pos_history = []
        self.stones = {'b': [], 'w': []}
        self.groups = {'b': [], 'w': []}
        self.play_data = {
            'color': None, 'opp_color': None, 'char': None, 'opp_char': None, 'coord': None,
            'y': None, 'x': None, 'temp_board': None, 'capturing_groups': None, 'makes_ko': None,
        }

        if self.data:  self.resetBoard(self.data['input']['cur_problem'])

    def printVars(self) -> None:
        dont_print = ['board', 'board_pos_history', 'data', 'stones', 'app', 'play_data']
        prints = {k: v for k, v in vars(self).items() if k not in dont_print}
        print(f"\nback/board vars =\n{json.dumps(prints, indent=4, default=str)}")

    def printBoard(self, with_coord:bool=True) -> None:
        print("")
        if with_coord:
            hor_coords = f"  {' '.join([str(x).rjust(2) for x in range(self.size)])}"
            print(hor_coords)
            for i, row in enumerate(self.board):
                vert_coord = str(i).rjust(2)
                print(f"{vert_coord}{' '.join([f' {x}' for x in row])} {vert_coord}")
            print(hor_coords)
        else:
            for row in self.board:  print(' '.join(row))
        print(self.captures)

    def resetBoard(self, presets:dict[list[list]]=None) -> None:
        presets = presets if presets else {}
        self.board = [[self.no_char for y in range(self.size)] for x in range(self.size)]
        for color, presets in presets.items():
            char = self.black_char if color.lower() == 'b' else self.white_char
            for y, x in presets:  self.board[y][x] = char
        self.recordBoardPos()
        self.setStones()
        self.setGroups()

    def play(self, color:str, coord:list[int], only_test_legality:bool=False) -> None:
        self.play_data['color'] = color
        self.play_data['opp_color'] = 'b' if color == 'w' else 'w'
        self.play_data['char'] = self.black_char if color == 'b' else self.white_char
        self.play_data['opp_char'] = self.white_char if color == 'b' else self.black_char
        self.play_data['coord'] = coord
        self.play_data['y'], self.play_data['x'] = coord

        if only_test_legality:
            legality, reason = self.playIsLegal()
            self.resetPlayData()
            return legality, reason

        if not self.playIsLegal()[0]:  self.resetPlayData()  ;  return
        self.board[self.play_data['y']][self.play_data['x']] = self.play_data['char']
        self.setStones()
        self.setGroups()
        self.handleCapturesDuringPlay()
        self.handleKoDuringPlay()
        self.recordBoardPos()
        self.resetPlayData()

    def resetPlayData(self) -> None:
        for k in self.play_data.keys():  self.play_data[k] = None

    # def kivyDeepCopyErrorWorkAround(self) -> dict:
    #     attr_dict = vars(self)
    #     del attr_dict['app']
    #     print(f"\n{attr_dict = }\n")

    def playIsLegal(self) -> tuple[bool, str]:
        # play is illegal because another stone is currently at that coord
        if self.play_data['coord'] in self.stones['b'] + self.stones['w']:  return False, 'occupied'
        # play is illegal due to ko
        if self.board[self.play_data['y']][self.play_data['x']] == self.ko_char:  return False, 'ko'

        data, app = self.data, self.app
        del self.data ; del self.app
        self.play_data['temp_board'] = deepcopy(self)
        self.data, self.app = data, app

        """
        2023-05-26
        TURNOVER NOTES:
        
        - Having an issue...  For some reason Kivy is throwing an odd error when using `deepcopy()`
        on Kivy objects (or so it says).  I'm not 100% sure this is my problem because I just ^
        removed the Kivy objects before deepcopy()-ing and I'm still having the same error.
        
            - 2nd thought...  Try removing (just comment out) all current/previous uses of
            BackBoard.  Then start from scratch with BackBoard implementation.
        """

        self.play_data['temp_board'].board[self.play_data['y']][self.play_data['x']] = self.play_data['char']
        self.play_data['temp_board'].setStones()
        self.play_data['temp_board'].setGroups()
        self.play_data['temp_board'].handleCapturesDuringPlay()
        # play is illegal due to suicide
        if self.play_data['temp_board'].getGroupFromCoord(self.play_data['coord']).liberties_count == 0:  return False, 'suicide'
        # play is illegal due to true ko verification (board repeated)
        if self.play_data['temp_board'].board in self.play_data['temp_board'].board_pos_history:  return False, 'true ko'
        return True, ''

    def handleCapturesDuringPlay(self) -> None:
        self.play_data['capturing_groups'] = [g for g in self.groups[self.play_data['opp_color']] if g.liberties_count == 0]
        if self.play_data['capturing_groups']:
            for group in self.play_data['capturing_groups']:
                self.captures[self.play_data['color']] += len(group.stones)
                for y, x in group.stones:  self.board[y][x] = self.no_char
            self.setStones()
            self.setGroups()

    def handleKoDuringPlay(self) -> None:
        self.play_data['makes_ko'] = False
        if (
            len(self.play_data['capturing_groups']) == 1 and
            len(self.play_data['capturing_groups'][0].stones) == 1
        ):
            neighbors = self.getStoneNeighbors(self.play_data['coord'])
            neighbors.remove(self.play_data['capturing_groups'][0].stones[0])
            # print(f"{[self.getStoneColor(n) == self.play_data['opp_color'] for n in neighbors] = }")
            if all([self.getStoneColor(n) == self.play_data['opp_color'] for n in neighbors]):
                # play("!!!")
                self.ko = self.play_data['capturing_groups'][0].stones[0]
                self.board[self.ko[0]][self.ko[1]] = self.ko_char
                self.play_data['makes_ko'] = True
        # if last play was ko
        if not self.play_data['makes_ko'] and self.ko:
            self.board[self.ko[0]][self.ko[1]] = self.no_char
            self.ko = None

    def recordBoardPos(self) -> None:
        self.board_pos_history += [deepcopy(self.board)]

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
                self.groups[color] += [Group(self, color, stones_to_group)]

        """
        # This is ChatGPT's "simplified" version of this method...  I'm actually pretty impressed.
        # I'm keeping my original though because I think the logic flow of this function is very
        # complicated, so I think the comments are required for reading.  And I also feel that due
        # to its complexity, breaking down the comprehensions helps with readability.
        self.groups = {'b': [], 'w': []}
        for color, stones in self.stones.items():
            if not stones:  continue
            group_labels = [0] * len(stones)
            new_label = 1
            for i, stone in enumerate(stones):
                if group_labels[i] == 0:
                    group_labels[i] = new_label
                    new_label += 1
                for other_i, other_stone in enumerate(stones):
                    if i == other_i:  continue
                    if stone in self.getStoneNeighbors(other_stone) and group_labels[other_i] != 0:
                        group_labels = [group_labels[other_i] if label == group_labels[i] else label for label in group_labels]
            for master_label in set(group_labels):
                stones_to_group = [self.stones[color][i] for i, label in enumerate(group_labels) if master_label == label]
                self.groups[color] += [Group(self, color, stones_to_group)]
        """

    def getStoneNeighbors(self, stone:list[int]) -> list[list[int]]:
        if type(stone) == 'str':  stone = util.convStrListCoordToListCoord(stone)
        y, x = stone
        neighbors = [
            [y - 1, x    ] if y != 0             else None,
            [y    , x - 1] if x != 0             else None,
            [y + 1, x    ] if y != self.size - 1 else None,
            [y    , x + 1] if x != self.size - 1 else None,
        ]
        neighbors = [n for n in neighbors if n]
        return neighbors

    def getStoneColor(self, stone:list[int]) -> str:
        y, x = stone
        char = self.board[y][x]
        if char == self.black_char:  color = 'b'
        elif char == self.white_char:  color = 'w'
        else:  color = ''
        return color

    def getGroupFromCoord(self, coord: list[int]) -> Group:
        for group in self.groups['b'] + self.groups['w']:
            if coord in group.stones:  return group


####################################################################################################


class Group():
    def __init__(self, board:Board, color:str, stones:list[list[int]]):
        self.board = board
        self.color = color
        self.stones = stones
        self.neighbors = []
        self.neighbors_count = 0
        self.liberties = []
        self.liberties_count = 0
        self.setNeighborsAndCount()
        self.setLibertiesAndCount()

    def __repr__(self):
        return f"Group('{self.color}': {self.stones})"

    def setNeighborsAndCount(self) -> None:
        neighbors = []
        for stone in self.stones:
            neighbors += [x for x in self.board.getStoneNeighbors(stone) if x not in self.stones]
        no_dupes = set([str(n) for n in neighbors])
        self.neighbors = [util.convStrListCoordToListCoord(n) for n in no_dupes]
        self.neighbors_count = len(self.neighbors)

    def setLibertiesAndCount(self) -> None:
        """
        NOTES:
        - Must be called after 'setNeighborsAndCount', 'setLibertiesAndCount' is dependent on an
        updated 'self.neighbors'.
        """
        other_color = 'b' if self.color == 'w' else 'w'
        self.liberties = [n for n in self.neighbors if n not in self.board.stones[other_color]]
        self.liberties_count = len(self.liberties)


####################################################################################################


if __name__ == '__main__':  main()



















