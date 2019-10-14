from argparse import ArgumentParser
from collections import namedtuple
import random
import time
from urllib.parse import urlsplit, urlunsplit

import tkinter as tk

import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(sys.argv[0]), 'autogen', 'python-client'))
sys.path.append(os.path.join(os.path.dirname(sys.argv[0]), '..', 'common'))

from pieces import Pieces
import swagger_client
from swagger_client.models import GetGame, Move, Player

import render

ALL_DIRECTIONS = [
        (-1,  0),
        ( 0, -1),
        ( 1,  0),
        ( 0,  1)
    ]

__WIDTH__ = __HEIGHT__ = 10

class Hit(object):
    def __init__(self, position):
        self.position = position
        self.directions_to_try = list(ALL_DIRECTIONS)


class Position(object):
    def __init__(self, y=None, x=None, gridref=None):
        if gridref:
            self.y = int(ord(gridref[0])) - ord('A')
            self.x = int(gridref[1:]) - 1
        else:
            self.y = y
            self.x = x

    def as_gridref(self):
        return chr(ord('A') + self.y) + str(1 + self.x)

    def __add__(self, direction):
        new = Position(self.y + direction[0], self.x + direction[1])
        if new.y < 0 or new.x < 0 or new.y >= __HEIGHT__ or new.x >= __WIDTH__:
            raise ValueError()
        return new


class Board(object):
    def __init__(self, board):
        self.board = []
        for row in board:
            self.board.append(list(row))
        self.winner = None

    def set(self, position, piece):
        self.board[position.y][position.x] = piece

    def get(self, position):
        return self.board[position.y][position.x]


class GameState(object):
    def __init__(self, root, gameid, player_name, knowledge):
        self.gameid = gameid
        self.knowledge = Board(knowledge)
        self.hits = []
        self.window = render.GameWindow(root, gameid, player_name, self.knowledge)


def random_position():
    return Position(gridref=random.choice('ABCDEFGHIJ')+str(random.randint(1, 10)))


game_state = {}


def find_games_for(api, player_name):
    player_info = api.players_name_get(player_name)
    rtn = []
    for gameid in player_info.games:
        gameobj = api.games_game_id_get(gameid)

        if gameobj.player1.name == player_name:
            knowledge = gameobj.player1.knowledge
        elif gameobj.player2.name == player_name:
            knowledge = gameobj.player2.knowledge
        else:
            assert False

        rtn.append( (gameid, knowledge) )
    return rtn


def progress_game_from_unknown_position(api, player_name, gameid, game_state):
    while True:
        position = random_position()
        if game_state.knowledge.get(position) == Pieces.Unknown:
            break
    response = api.games_game_id_grid_ref_put(gameid, position.as_gridref(), body=Move(player_name))
    print(gameid, position.as_gridref(), response.result)

    if response.result == 'Hit':
        game_state.hits.append(Hit(position))
        piece = Pieces.Ship
    else:
        piece = Pieces.Empty

    game_state.knowledge.set(position, piece)


def progress_game_from_hit_in_direction(api, player_name, gameid, game_state, position, direction):
    """
    Return bool(continue looking in this direction), bool(moved)
    """
    while True:
        try:
            position = position + direction
        except ValueError:
            return False, False # we've reached the end of the grid in that direction

        if game_state.knowledge.get(position) == Pieces.Unknown:
            break

        if game_state.knowledge.get(position) == Pieces.Empty:
            return False, False # we've hit something we already know about

        assert game_state.knowledge.get(position) == Pieces.Ship

    response = api.games_game_id_grid_ref_put(gameid, position.as_gridref(), body=Move(player_name))
    print(gameid, position.as_gridref(), response.result)

    if response.result == 'Hit':
        piece = Pieces.Ship
    else:
        piece = Pieces.Empty

    game_state.knowledge.set(position, piece)
    return (response.result == 'Hit', True)



def progress_game_from_hit(api, player_name, gameid, game_state):
    hit = game_state.hits[0]
    position = hit.position
    while hit.directions_to_try:
        direction = hit.directions_to_try[0]
        continue_looking, moved = progress_game_from_hit_in_direction(api, player_name, gameid, game_state, position, direction)
        if not continue_looking:
            hit.directions_to_try.pop(0)

            assert game_state.knowledge.get(hit.position) == Pieces.Ship
            try:
                next_pos = hit.position + direction
                if game_state.knowledge.get(next_pos) == Pieces.Ship:
                    # we got a run of at least 2 ships in this direction.
                    # Only look backwards (if we haven't already)
                    opposite_direction = (-direction[0], -direction[1])
                    if opposite_direction in hit.directions_to_try:
                        hit.directions_to_try = [opposite_direction]
                    else:
                        hit.directions_to_try = []
            except ValueError as e:
                # can't continue that way
                pass

        if moved:
            return

    game_state.hits.pop(0) # we've exhausted the knowledge from this hit
    
        


def progress_game(api, player_name, gameid, game_state):
    if game_state.hits:
        progress_game_from_hit(api, player_name, gameid, game_state)
    else:
        progress_game_from_unknown_position(api, player_name, gameid, game_state)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--host',
                        help="Specify host. Default is taken from the generated client")
    parser.add_argument('--port',
                        help="Specify port. Default is taken from the generated client")
    parser.add_argument('player_name',
                        help="Name of player")
    parser.add_argument('-d', '--delay', type=int,
                        help="Time to wait between moves (in ms)")
    parser.set_defaults(host=None, port=None, delay=1000)
    args = parser.parse_args()
    return args


def make_moves(delay, root, api, player_name):
    games = find_games_for(api, player_name)
    for gameid, knowledge in games:
        if gameid not in game_state:
            game_state[gameid] = GameState(root, gameid, player_name, knowledge)
    # this separate loop ensures we update games that we already know about,
    # that have now finished (and hence been removed from the list of active games)
    for gameid in game_state.keys():
        game_info = api.games_game_id_get(gameid)
        to_move = game_info.move
        if to_move == player_name:
            progress_game(api, player_name, gameid, game_state[gameid])
        if game_info.winner:
            game_state[gameid].knowledge.winner = 'WIN!' if (game_info.winner == player_name) else 'LOSE!'
        game_state[gameid].window.update()

    root.after(delay, make_moves, delay, root, api, player_name)


def main():
    args = parse_args()
    api = swagger_client.api.DefaultApi()

    if args.host or args.port:
        url = urlsplit(api.api_client.configuration.host)

        host = args.host if args.host else url.hostname
        port = args.port if args.port else url.port

        url = list(url) # needs to be mutable
        url[1] = '%s:%s' % (host, port)

        api.api_client.configuration.host = urlunsplit(url)

    root = tk.Tk()
    root.after(args.delay, make_moves, args.delay, root, api, args.player_name)
    root.mainloop()


if __name__ == '__main__':
    main()
