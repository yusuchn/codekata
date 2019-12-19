from collections import namedtuple
import json
import os.path
import random
import time

from atomicfile import InputAtomicFile, OutputAtomicFile

WIDTH = 20
HEIGHT = 20
NR_MINES = 12

OUTPUT_BOARDFILE = 'game.json'
INPUT_COMMANDFILE = 'command.json'

Position = namedtuple('Position', ['x', 'y'])

class GridSquare:
    EMPTY = '-'
    MINE = '#'


class PlayerSquare:
    UNKNOWN = '?'
    MINE = '#'


class GameStatus:
    PLAYING = 'playing'
    WON = 'won'
    LOST = 'lost'


class Command(object):
    pass


class CommandMove(Command):
    def __init__(self, positions):
        super().__init__()
        self.positions = positions


class CommandGuessMines(Command):
    def __init__(self, positions):
        super().__init__()
        self.positions = positions



class Minesweeper(object):
    def __init__(self, width, height, nr_mines):
        self.width = width
        self.height = height
        self.nr_mines = nr_mines

        self.grid = []
        while len(self.grid) < self.height:
            self.grid.append( self.width * [GridSquare.EMPTY] )
        self.mines = []
        while len(self.mines) < nr_mines:
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            pos = Position(x, y)
            self.set_point(pos, GridSquare.MINE)
            self.mines.append(pos)

        self.players_grid = []
        while len(self.players_grid) < self.height:
            self.players_grid.append( self.width * [PlayerSquare.UNKNOWN] )

        self.game_status = GameStatus.PLAYING

    def get_point(self, pos):
        if (0 <= pos.y < HEIGHT) and (0 <= pos.x < WIDTH):
            return self.grid[pos.y][pos.x]
        return None

    def set_point(self, pos, value):
        self.grid[pos.y][pos.x] = value

    def make_move(self, pos):
        if self.get_point(pos) == GridSquare.MINE:
            new_square_value = PlayerSquare.MINE
            self.game_status = GameStatus.LOST
        else:
            new_square_value = self.count_adjacent_mines(pos)
        self.players_grid[pos.y][pos.x] = new_square_value

    def move_already_made(self, pos):
        return self.players_grid[pos.y][pos.x] != PlayerSquare.UNKNOWN

    def count_adjacent_mines(self, pos):
        nr_mines = 0
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dx == dy == 0:
                    continue
                newpos = Position(pos.x + dx, pos.y + dy)
                if self.get_point(newpos) == GridSquare.MINE:
                    nr_mines += 1
        return nr_mines


def print_game_to_file(game, outpath):
    game_json = {
            'status': game.game_status,
            'grid': game.players_grid,
            'nmines': game.nr_mines
    }
    with OutputAtomicFile(outpath) as handle:
        json.dump(game_json, handle)


def load_command_position(position):
    if not isinstance(position, dict):
        return None
    if ('x' not in position) or ('y' not in position):
        return None
    x = position['x']
    y = position['y']
    if (not isinstance(x, int)) or (not isinstance(y, int)):
        return None
    if (x < 0) or (y < 0) or (WIDTH <= x) or (HEIGHT <= y):
        return None
    return Position(x, y)


def load_command(inpath):
    with InputAtomicFile(inpath, wait_for_file=True, remove_after_reading=True) as handle:
        command = json.load(handle)
    if not isinstance(command, dict):
        return None
    # Expected input:
    #   {"move": {"x": int, "y": int}}
    # or
    #   {"move": [{"x": int, "y": int}, ...]}
    # or
    #   {"mines": [{"x": int", "y": int}, ....]}
    if (("move" not in command) and ("mines" not in command)) or ("move" in command and "mines" in command):
        return None

    if "move" in command:
        positions = []
        if isinstance(command['move'], list):
            for position in command['move']:
                position = load_command_position(position)
                if position:
                    positions.append(position)
                # TODO: Error reporting for bad position
        else:
            positions.append(load_command_position(command['move']))
        return CommandMove(positions) if positions else None

    if "mines" in command:
        mines = command['mines']
        if not isinstance(mines, list):
            return None
        mines = [load_command_position(mine) for mine in mines]
        if not all(mines):
            return None
        return CommandGuessMines(mines)

    assert False
    return None


def print_game(game):
    print(game.game_status)
    for row in game.players_grid:
        print(' '.join(str(cell) for cell in row))
    print("")
    print("")

def main():
    game = Minesweeper(WIDTH, HEIGHT, NR_MINES)
    while game.game_status == GameStatus.PLAYING:
        print_game(game)
        print_game_to_file(game, OUTPUT_BOARDFILE)
        command = load_command(INPUT_COMMANDFILE)
        if not command:
            print("Bad input")
            continue

        if type(command) == CommandMove:
            for position in command.positions:
                if game.move_already_made(position):
                    print(f"Already played at {position}")
                else:
                    print(f"Move: {position}")
                    game.make_move(position)

        elif type(command) == CommandGuessMines:
            mines = command.positions
            if set(mines) == set(game.mines):
                print("GAME WON!")
                print_game(game)
                game.game_status = GameStatus.WON
            else:
                print("Mines guessed incorrectly")

    print_game(game)
    print_game_to_file(game, OUTPUT_BOARDFILE)


if __name__ == '__main__':
    main()
