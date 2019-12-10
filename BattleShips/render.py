import tkinter as tk
from pieces import Pieces

WIDTH = 10
HEIGHT = 10

MARGIN = 10
PADDING = 3
TILE_SIZE = 40

class GameWindow(object):
    def __init__(self, root, gameid, player_name, knowledge):
        self.window_w = MARGIN*2 + WIDTH*TILE_SIZE + (WIDTH-1)*PADDING
        self.window_h = MARGIN*2 + HEIGHT*TILE_SIZE + (HEIGHT-1)*PADDING
        root.geometry(f'{self.window_w}x{self.window_h+40}')
        self.window = tk.Toplevel(root, width=self.window_w, height=self.window_h)
        self.window.title(f'{gameid} ({player_name})')
        self.window.geometry(f'{self.window_w}x{self.window_h}')
        self.canvas = tk.Canvas(self.window, width=self.window_w, height=self.window_h)
        self.canvas.config(bg='white')
        self.canvas.pack()
        self.knowledge = knowledge

    def update(self):
        self.canvas.delete(tk.ALL)

        gy = MARGIN
        for y, row in enumerate(self.knowledge.board):
            gx = MARGIN
            for piece in row:
                if piece == Pieces.Unknown:
                    fill = '#ccc'
                elif piece == Pieces.Empty:
                    fill = '#8888ff' # pale blue
                elif piece == Pieces.Ship:
                    fill = '#000'
                else:
                    assert False
                self.canvas.create_rectangle( (gx, gy, gx+TILE_SIZE, gy+TILE_SIZE), fill=fill)
                gx += TILE_SIZE + PADDING
            gy += TILE_SIZE + PADDING

        if self.knowledge.winner:
            self.canvas.create_text((self.window_w/2, self.window_h/2),
                                    fill='#f00',
                                    text=self.knowledge.winner,
                                    font=('Arial Bold', 48))
