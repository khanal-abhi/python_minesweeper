from os import system
import random


class Game(object):
    """
    This is the game class. This handles the game loop, as well as game logic as the user selects the mines.
    """
    BLOCK, BLANK, MINE, FLAG = chr(63), chr(32), chr(42), chr(33)

    def __init__(self, grid_size=(10, 10), mines_count=10):
        """
        This sets up the game grid.
        :param grid_size:  The tuple representing the width and the height of the map, in that order.
        """
        self.grid_size = grid_size
        self.mines_count = mines_count
        self.score = 0
        self.flags = []
        self.cleared = []
        self.distances = []
        self.__mines = []
        self.guesses = []
        self.adj_counts = []
        self.revealed = set([])
        self.game_over = False
        self.create_map()
        self.start()

    def draw_header(self):
        """
        This just draws the header for each clear render
        :return: None
        """
        system('clear')
        print(''.join(['='] * 45))
        print('Minesweeper')
        print('Grid Size: {} X {}'.format(self.grid_size[0], self.grid_size[1]))
        print('Number of mines: {}'.format(self.mines_count))
        print(''.join(['='] * 45))

    def draw_map(self):
        """
        This draws the game map.
        :return:
        """
        print('', end='\t')
        for y in range(self.grid_size[1]):
            print(y, end='\t')
        print('')
        for i in range(self.grid_size[0]):
            print(i, end='\t')
            for j in range(self.grid_size[1]):
                item = i*self.grid_size[0] + j
                if item in self.revealed:
                    if self.adj_counts[item] == 0:
                        print(Game.BLANK, end='\t')
                    else:
                        print(self.adj_counts[item], end='\t')
                else:
                    print(Game.BLOCK, end='\t')
            print('', flush=True)
        print(''.join(['='] * 45))
        if len(self.revealed) + self.mines_count == self.grid_size[0] * self.grid_size[1]:
            print()
            print('Congratulations, you have won!')
            self.game_over = True

    def reveal_recursively(self, row, column):
        """
        This reveals the map recursively
        :param row: The row that was clicked
        :param column: The column that was clicked
        :return: None
        """
        val = row*self.grid_size[0] + column
        if val in self.revealed:
            return
        self.revealed.add(val)

        start_row = max(0, row - 1)
        end_row = min(self.grid_size[0], row + 2)

        start_column = max(0, column - 1)
        end_column = min(self.grid_size[1], column + 2)
        for i in range(start_row, end_row):
            for j in range(start_column, end_column):
                if i == row and j == column:
                    continue
                else:
                    val = i*self.grid_size[0] + j
                    if self.adj_counts[val] == 0:
                        self.reveal_recursively(i, j)
                    else:
                        self.revealed.add(val)

    def ask_next(self):
        """
        Ask for the next input and parse it
        :return:
        """
        try:
            row, column = [int(x) for x in input("What is your next pick? (row column) ", ).split()]
            val = self.grid_size[0] * row + column
            self.guesses.append(val)
            if val in self.__mines:
                print()
                print("Game Over")
                self.game_over = True
            else:
                self.reveal_recursively(row, column)

        except KeyboardInterrupt:
            print()
            print("Game Over")
            self.game_over = True

    def create_map(self):
        """
        Creates the map with the random mines
        :return:
        """
        mines = set([])
        while len(mines) < self.mines_count:
            mines.add(random.randint(0, self.grid_size[0] * self.grid_size[1]))
        self.__mines = list(mines)
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                self.adj_counts.append(self.adj_count(i, j))

    def adj_count(self, row, column):
        """
        This gives the adj count for a grid item
        :return: how many mines are adjacent to this cell.
        """
        ss = 0
        start_row = max(0, row-1)
        end_row = min(self.grid_size[0], row+2)

        start_column = max(0, column-1)
        end_column = min(self.grid_size[1], column+2)
        for i in range(start_row, end_row):
            for j in range(start_column, end_column):
                if i == row and j == column:
                    continue
                val = i*self.grid_size[0] + j
                if val in self.__mines:
                    ss += 1
        return ss

    def start(self):
        """
        This runs the game loop.
        :return:
        """
        while not self.game_over:
            self.draw_header()
            self.draw_map()
            self.ask_next()


if __name__ == '__main__':
    """
    If this is run as a script.
    """
    grid_size = [int(x) for x in input("Size: (width height) ").split()]
    mines_count = int(input("Mines count: "))
    game = Game(grid_size=grid_size,mines_count=mines_count)
