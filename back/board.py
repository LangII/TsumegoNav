

#


####################################################################################################


SETTINGS = {
    'size': 19,
    'black_char': '#',
    'white_char': 'O',
    'no_char': '-',
}


####################################################################################################


def main():
    board = Board()
    board.resetBoard({
        'b': [[3, 3]],
        'w': [],
    })
    board.printBoard()


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
        self.resetBoard()

    def resetBoard(self, presets:dict[list[list]]=None) -> None:
        presets = presets if presets else {}
        self.board = [[self.no_char for y in range(self.size)] for x in range(self.size)]
        for color, presets in presets.items():
            char = self.black_char if color.lower() == 'b' else self.white_char
            for y, x in presets:  self.board[y][x] = char

    def printBoard(self) -> None:
        print("")
        for row in self.board:  print(' '.join(row))


####################################################################################################


if __name__ == '__main__':  main()



















