from argparse import ArgumentParser
from collections import namedtuple
import io
import logging
import random
import SocketServer

from PIL import Image
import pygame

from commands import Command

SCREEN_W = 800
SCREEN_H = 600
SCREEN_Y_PAD = 4

BRICK_H = 24
BRICK_W = 72
BRICK_X_PAD = 8
BRICK_Y_PAD = 4

BALL_R = 8

BAT_W = 70
BAT_H = 20
BAT_Y = SCREEN_H - BAT_H - SCREEN_Y_PAD

BALL_SPEED = 1
BAT_SPEED = 1.5

# Types
Brick = pygame.Rect # pygame.Rect
Position = namedtuple('Position', ['x', 'y'])
Movement = namedtuple('Movement', ['dx', 'dy'])


class Colours:
    Black = (0, 0, 0)
    Red = (255, 0, 0)
    Green = (0, 255, 0)
    Blue = (0, 0, 255)
    White = (255, 255, 255)


class GameState:
    WaitingToStart = 0
    Playing = 1
    GameOver = 2


class BatController(SocketServer.BaseRequestHandler):
    def handle(self):
        """
        This handler is invoked when a UDP packet is received.
        Three packets are supported, all a single byte of data:
        "L": Start moving the bat left
        "R": Start moving the bat right
        ".": Stop moving the bat
        """
        # self.request is a pair of data and client socket
        self.server.command = self.request[0].decode('utf-8')  # assumes printable
        server_command_str = str(self.server.command)
        client_address_str = str(self.client_address)
        logging.debug('Command {{}} received from {}'.format(server_command_str, client_address_str))


class ImageServer(SocketServer.BaseRequestHandler):
    def handle(self):
        # logging.debug(f"Connection from {self.client_address}")
        logging.debug("Connection from {}".format(self.client_address))
        surface = self.server.surface
        image = pygame.image.tostring(surface, 'RGB')
        image = Image.frombytes('RGB', surface.get_size(), image)
        buffer = io.BytesIO()
        image.save(buffer, self.server.format)
        data = buffer.getvalue()
        self.request.sendall(data)


def allocate_bricks():
    bricks = []
    gy = 100
    for y in range(5):
        gx = int(BRICK_X_PAD / 2)
        while gx < SCREEN_W:
            bricks.append(Brick(gx, gy, BRICK_W, BRICK_H))
            gx += BRICK_W + BRICK_X_PAD
        gy += BRICK_H + BRICK_Y_PAD
    return bricks


# def draw_bricks(surface: pygame.Surface, bricks: list):
def draw_bricks(surface, bricks):
    for brick in bricks:
        draw_brick(surface, brick)


# def draw_brick(surface: pygame.Surface, brick: pygame.Rect):
def draw_brick(surface, brick):
    surface.fill(Colours.Red, brick)
    pygame.draw.rect(surface, Colours.Black, brick, 2)


# def erase_brick(surface: pygame.Surface, brick: pygame.Rect):
def erase_brick(surface, brick):
    pygame.draw.rect(surface, Colours.White, (brick[0], brick[1], brick[2] + 2, brick[3] + 2))


# def erase_ball(surface: pygame.Surface, ballpos: Position):
def erase_ball(surface, ballpos):
    pygame.draw.circle(surface, Colours.White, ballpos, BALL_R + 1)


# def draw_ball(surface: pygame.Surface, ballpos: Position):
def draw_ball(surface, ballpos):
    pygame.draw.circle(surface, Colours.Green, ballpos, BALL_R)
    pygame.draw.circle(surface, Colours.Black, ballpos, BALL_R, 1)


# def draw_bat(surface: pygame.Surface, batpos: pygame.Rect):
def draw_bat(surface, batpos):
    batrect = (batpos, (BAT_W, BAT_H))
    pygame.draw.rect(surface, Colours.Blue, batrect)
    pygame.draw.rect(surface, Colours.Black, batrect, 2)


# def erase_bat(surface: pygame.Surface, batpos: pygame.Rect):
def erase_bat(surface, batpos):
    pygame.draw.rect(surface, Colours.White, (batpos, (BAT_W + 2, BAT_H + 2)))


class GameController(object):
    def __init__(self, surface, commandserver, speed):
        self.surface = surface
        self.commandserver = commandserver
        self.speed = speed
        self.reset()

    def reset(self):
        self.game_state = GameState.WaitingToStart
        self.bricks = allocate_bricks()
        self.ballpos = Position(int(SCREEN_W / 2 - BALL_R), int(self.bricks[-1].y + BRICK_H + BRICK_Y_PAD + BALL_R * 2))
        self.ballspeed = Movement(0, 0)
        self.batpos = Position(SCREEN_W / 2 - BAT_W / 2, BAT_Y)
        self.batspeed = Movement(0, 0)
        self.surface.fill(Colours.White)
        draw_bricks(self.surface, self.bricks)

    def idle_loop(self, time_passed):
        self.commandserver.handle_request()
        if self.commandserver.command:
            logging.debug(self.commandserver.command)

        if self.commandserver.command == Command.ResetGame:
            self.reset()
        else:
            if self.game_state == GameState.GameOver:
                return

            if self.game_state == GameState.WaitingToStart:
                # only one command is accepted: start game
                if self.commandserver.command == Command.StartGame:
                    self.ballspeed = Movement(BALL_SPEED * random.choice((-1, 1)), BALL_SPEED)
                    self.game_state = GameState.Playing
            elif self.game_state == GameState.Playing:
                if self.commandserver.command == Command.MoveLeft:
                    self.batspeed = Movement(-BAT_SPEED, 0)
                elif self.commandserver.command == Command.MoveRight:
                    self.batspeed = Movement(BAT_SPEED, 0)
                elif self.commandserver.command == Command.StopMoving:
                    self.batspeed = Movement(0, 0)
        self.commandserver.command = None

        self.move_bat(time_passed)

        self.move_ball(time_passed)

        text_to_show = None
        if self.ballpos.y > SCREEN_H - SCREEN_Y_PAD:
            text_to_show = "Game over!"
        elif not self.bricks:
            text_to_show = "YOU WIN!!"
        if text_to_show:
            font = pygame.font.Font('AGENCYB.TTF', 48)
            text_surface = font.render(text_to_show, True, Colours.Black)
            text_w, text_h = text_surface.get_size()
            self.surface.blit(text_surface, ((SCREEN_W - text_w) / 2, (SCREEN_H - text_h) / 2))
            self.game_state = GameState.GameOver

    def move_bat(self, time_passed):
        erase_bat(self.surface, self.batpos)
        dx = int(float(self.batspeed.dx) * float(time_passed) / float(self.speed))
        dy = int(float(self.batspeed.dy) * float(time_passed) / float(self.speed))
        self.batpos = Position(self.batpos.x + dx, self.batpos.y + dy)  # dy=0, but gives symmetry with move_ball
        if (self.batpos.x + BAT_W) >= SCREEN_W:
            self.batpos = Position(SCREEN_W - BAT_W, self.batpos.y)
            self.batspeed = Movement(0, 0)
        if self.batpos.x <= 0:
            self.batpos = Position(0, self.batpos.y)
            self.batspeed = Movement(0, 0)
        draw_bat(self.surface, self.batpos)

    def move_ball(self, time_passed):
        erase_ball(self.surface, self.ballpos)
        oldpos = self.ballpos
        dx = int(float(self.ballspeed.dx) * float(time_passed) / float(self.speed))
        dy = int(float(self.ballspeed.dy) * float(time_passed) / float(self.speed))
        self.ballpos = Position(self.ballpos.x + dx, self.ballpos.y + dy)
        # bounce off edge of screen
        if (self.ballpos.y - BALL_R <= 0):
            self.ballpos = Position(self.ballpos.x, BALL_R)
            self.ballspeed = Movement(self.ballspeed.dx, -self.ballspeed.dy)
        if (self.ballpos.x + BALL_R >= SCREEN_W) and (dx > 0):
            self.ballspeed = Movement(-self.ballspeed.dx, self.ballspeed.dy)
        elif (self.ballpos.x - BALL_R <= 0) and (dx < 0):
            self.ballspeed = Movement(-self.ballspeed.dx, self.ballspeed.dy)
        # bounce off bat
        if (self.ballpos.y + BALL_R >= BAT_Y - 2) and \
           (self.batpos.x <= self.ballpos.x <= self.batpos.x + BAT_W) and \
           (self.ballspeed.dy > 0):
            self.ballspeed = Movement(self.ballspeed.dx, -self.ballspeed.dy)
        # hit any bricks?
        ball_rect = pygame.Rect(self.ballpos.x - BALL_R, self.ballpos.y - BALL_R, BALL_R * 2, BALL_R * 2)
        hit_brick_index = ball_rect.collidelist(self.bricks)
        if hit_brick_index > -1:
            hit_brick = self.bricks.pop(hit_brick_index)
            erase_brick(self.surface, hit_brick)
            # figure out which edge of the brick was hit:
            if (self.ballpos.y - BALL_R <= hit_brick.bottom <= oldpos.y - BALL_R) or \
               (oldpos.y + BALL_R <= hit_brick.top <= self.ballpos.y + BALL_R):
                # we hit the top or bottom edge:
                self.ballspeed = Movement(self.ballspeed.dx, -self.ballspeed.dy)
            else:
                # hit a left or right edge:
                self.ballspeed = Movement(-self.ballspeed.dx, self.ballspeed.dy)
        draw_ball(self.surface, self.ballpos)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-H', '--listen-host', type=str, metavar='HOST',
                        help="Listen on HOST. Default %(default)s")
    parser.add_argument('-P', '--listen-port', type=int, metavar='PORT',
                        help="Listen on PORT. Default %(default)s")
    parser.add_argument('-f', '--format', choices=['bmp', 'png'], metavar='TYPE',
                        help="Serve images as TYPE. Default %(default)s")
    parser.add_argument('-s', '--speed', type=int, choices=range(1, 20),
                        help="Select speed. Smaller number is faster.")
    parser.set_defaults(host='0.0.0.0', port=0xB407, format='png', speed=8)
    args = parser.parse_args()
    return args


def main():
    logging.basicConfig(level=logging.DEBUG)
    args = parse_args()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.font.init()

    surface = pygame.Surface((SCREEN_W, SCREEN_H))

    screen.blit(surface, (0, 0))
    pygame.display.flip()

    clock = pygame.time.Clock()
    quit = False

    SocketServer.ThreadingTCPServer.allow_reuse_address = True
    commandserver = SocketServer.UDPServer((args.host, args.port), BatController)
    imageserver = SocketServer.ThreadingTCPServer((args.host, args.port), ImageServer)
    # the following is python 3 syntax, we are using python 2.7 for the simplicity of PyOpenCL
    # with SocketServer.UDPServer((args.host, args.port), BatController) as commandserver, \
    #         SocketServer.ThreadingTCPServer((args.host, args.port), ImageServer) as imageserver:
    commandserver.timeout = imageserver.timeout = 0
    commandserver.command = None
    game_controller = GameController(surface, commandserver, args.speed)
    imageserver.surface = surface
    imageserver.format = args.format
    while not quit:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            quit = True
        elif event.type == pygame.NOEVENT:
            game_controller.idle_loop(time_passed=clock.tick())
            imageserver.handle_request()

            screen.blit(surface, (0, 0))
            pygame.display.flip()


if __name__ == '__main__':
    main()
