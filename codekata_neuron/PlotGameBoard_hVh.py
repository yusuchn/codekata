#! python

import numpy as np
import matplotlib.pyplot as plt
#import tkinter as tk


# example plot
#H = np.array([[1, 2, 3, 4, 5],
#              [6, 7, 8, 9, 10],
#              [11, 12, 13, 14, 15],
#              [16, 17, 18, 19, 20],
#              [21, 22, 23, 24, 25]])  # added some commas and array creation code

#fig = plt.figure(figsize=(6, 3.2))

#ax = fig.add_subplot(111)
#ax.set_title('colorMap')
#plt.imshow(H)
#ax.set_aspect('equal')

#cax = fig.add_axes([0.12, 0.1, 0.78, 0.8])
#cax.get_xaxis().set_visible(False)
#cax.get_yaxis().set_visible(False)
#cax.patch.set_alpha(0)
#cax.set_frame_on(False)
#plt.colorbar(orientation='vertical')
#plt.show()


from tkinter import *
#from tkinter import Tk, Canvas, Frame, BOTH
from tkinter import messagebox

# if not copy tkSimpleDialog to the project folder, need to uncomment following, but doesn't seem to work?
# import sys
# # sys.path.append('C:\suyu\CodeKatas\Python-2.7.3-master\Python-2.7.3-master\Lib\lib-tk')
# sys.path.insert(0, 'C:\suyu\CodeKatas\Python-2.7.3-master\Python-2.7.3-master\Lib\lib-tk')
# print(sys.path)

# copied necessary files to project folder,
import tkSimpleDialog
import sys      # for using sys._getframe().f_code.co_name to retrieve function name for debugging


# game board
total_row = 6
total_col = 6
grid = [[1] * total_col for n in range(total_row)]
w = 100
image_shift = (100-64)/2
text_shift = 100/2      # canvas.creat_text centres the text at the coordinate

current_player = 'none'
cell_colours = {'piece_picked': 'SlateGray1',
                'piece_dropped': 'white smoke',
                'board': 'white smoke',
                'possible_move': 'wheat1',
                'invalid': 'invalid'}
cell_images = {'me_human': 'Circle_s.png',
               'me_computer': 'Circle_s.png',
               'another_human': 'Cross_s.png',
               'another_computer': 'Cross_s.png',
               'another_remote': 'Cross_s.png',
               'neutron': 'Star_s.png',
               'board': 'none',
               'invalid':'invalid'}
# cell_image_types is for checking not picking other player's piece
cell_image_types = {'Circle_s.png': 'me',
                    'Cross_s.png': 'another',
                    'Star_s.png': 'neutron',
                    'none': 'board',
                    'invalid': 'invalid'}
grid_images_default = [
    ['none',    '1_s.png',      '2_s.png',      '3_s.png',      '4_s.png',      '5_s.png'],
    ['A_s.png', 'Cross_s.png',  'Cross_s.png',  'Cross_s.png',  'Cross_s.png',  'Cross_s.png'],
    ['B_s.png', 'none',         'none',         'none',         'none',         'none'],
    ['C_s.png', 'none',         'none',         'Star_s.png',   'none',         'none'],
    ['D_s.png', 'none',         'none',         'none',         'none',         'none'],
    ['E_s.png', 'Circle_s.png', 'Circle_s.png', 'Circle_s.png', 'Circle_s.png', 'Circle_s.png']]
grid_colours_default = [
    ['SlateGray1',  'SlateGray1',   'SlateGray1',   'SlateGray1',   'SlateGray1',   'SlateGray1'],
    ['SlateGray1',  'white smoke',  'white smoke',  'white smoke',  'white smoke',  'white smoke'],
    ['SlateGray1',  'white smoke',  'white smoke',  'white smoke',  'white smoke',  'white smoke'],
    ['SlateGray1',  'white smoke',  'white smoke',  'white smoke',  'white smoke',  'white smoke'],
    ['SlateGray1',  'white smoke',  'white smoke',  'white smoke',  'white smoke',  'white smoke'],
    ['SlateGray1',  'white smoke',  'white smoke',  'white smoke',  'white smoke',  'white smoke']]
# NOTE, don't use grid_images = grid_images_default, grid_colours = grid_colours_default
# as that sets reference pointers, as the values of grid_images and grid_colours change
# so do the values of grid_images_default and grid_colours_default
#grid_images = grid_images_default
#grid_colours = grid_colours_default
grid_images = [['none'] * total_col for n1 in range(total_row)]
grid_colours = [['none'] * total_col for n2 in range(total_row)]

# # when dropping a piece, the cell image has to be what was picked with previous step
picked_cell_image = 'none'
picked_cell_image_type = cell_image_types[picked_cell_image]

# steps
step_completed_me = 0
step_completed_another = 0
steps = {0: 'invalid',
         1: 'neutron_piece_picked',
         2: 'neutron_piece_dropped',
         3: 'player_piece_picked',
         4: 'player_piece_dropped'}

# step result
# E: row_index_change = 0, col_index_change > 0
# NE: row_index_change < 0, col_index_change > 0
# N: row_index_change < 0, col_index_change = 0
# NW: row_index_change < 0, col_index_change < 0
# W: row_index_change = 0, col_index_change < 0
# SW: row_index_change > 0, col_index_change < 0
# S: row_index_change > 0, col_index_change = 0
# SE: row_index_change > 0, col_index_change > 0
move_direction_list = {'E', 'NE', 'N', 'NW', 'W', 'SW', 'S', 'SE'}
old_row_index_me = -1
old_col_index_me = -1
old_row_index_another = -1
old_col_index_another = -1

# game result
# start position: grid.row_0 is another player, cross
# start position: grid.row_total_row is me, circle
# goame overn if neutron cannot move, or one of the player piece is moved to opponent's row
# game_result values:
# 'none',
# 'me move completed' for me_xxx
# 'another move completed' for another_xxx
# 'game over, you won' for me_xxx,
# 'game over, you lost' for me_xxx
game_result = 'none'

draw_debug = False


if draw_debug:
    print('grid={}'.format(grid))
    print('grid_images={}'.format(grid_images))
    print('grid_colours={}'.format(grid_colours))
    print('cell size = {}. image size = 64, image shift = {}, text_shift = {}'.format(w, image_shift, text_shift))


def reset_grid_pattern():
    print('function: {}'.format(sys._getframe().f_code.co_name))
    global grid_images
    global grid_colours
    global grid_images_default
    global grid_colours_default
    for m in range(total_row):
        for n in range(total_col):
            grid_images[m][n] = grid_images_default[m][n]
            grid_colours[m][n] = grid_colours_default[m][n]


# test example class
class DrawLines(Frame):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.master.title("Lines")
        self.pack(fill=BOTH, expand=1)

        canvas = Canvas(self)
        canvas.create_line(15, 25, 200, 25)
        canvas.create_line(300, 35, 300, 200, dash=(4, 2))
        canvas.create_line(55, 85, 155, 85, 105, 180, 55, 85)

        canvas.pack(fill=BOTH, expand=1)


# test example class
class DrawColourRects(Frame):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.master.title("ColourRects")
        self.pack(fill=BOTH, expand=1)

        canvas = Canvas(self)
        canvas.create_rectangle(30, 10, 120, 80,
                                outline="#fb0", fill="#fb0") #yellow
        canvas.create_rectangle(150, 10, 240, 80,
                                outline="#f50", fill="#f50") #red
        canvas.create_rectangle(270, 10, 370, 80,
                                outline="#05f", fill="#05f") #blue
        canvas.pack(fill=BOTH, expand=1)


root = Tk()
root.geometry("600x600")

frame = Frame(root, width=600, height=600, background="bisque")
frame.pack(fill=None, expand=True)
# the following example line doesn't seem to take any effect?
# frame.place(relx=.5, rely=.5, anchor="c")

canvas = Canvas(frame, width=600, height=600)
canvas.pack()


def draw_game_board(canvas):
    print('function: {}'.format(sys._getframe().f_code.co_name))
    canvas.delete('all')
    x, y = 0, 0
    global draw_debug
    global grid_images
    global grid_colours
    # NOTE, photo variables need to created as global to keep the reference alive to be used by
    # canvas.create_image, otherwise, as soon as PhotoImage is completed the reference is lost,
    # and cavas.create_image won't draw anything as no reference to the object found
    # NOTE, photo variables have to be positioned outside and before the for loop, otherwise,
    # only the last image is drawn
    global photo_Cross
    global photo_Circle
    global photo_Star
    global photo_1
    global photo_2
    global photo_3
    global photo_4
    global photo_5
    global photo_A
    global photo_B
    global photo_C
    global photo_D
    global photo_E
    photo_Cross = PhotoImage(file="Cross_s.png")
    photo_Circle = PhotoImage(file="Circle_s.png")
    photo_Star = PhotoImage(file="Star_s.png")
    photo_1 = PhotoImage(file="1_s.png")
    photo_2 = PhotoImage(file="2_s.png")
    photo_3 = PhotoImage(file="3_s.png")
    photo_4 = PhotoImage(file="4_s.png")
    photo_5 = PhotoImage(file="5_s.png")
    photo_A = PhotoImage(file="A_s.png")
    photo_B = PhotoImage(file="B_s.png")
    photo_C = PhotoImage(file="C_s.png")
    photo_D = PhotoImage(file="D_s.png")
    photo_E = PhotoImage(file="E_s.png")
    for row in grid:
        for col in row:
            row_index = int(y / w)
            col_index = int(x / w)
            cell_colour = grid_colours[row_index][col_index]
            cell_image = grid_images[row_index][col_index]
            if draw_debug:
                print('row_index={}, col_indxe={}, cell_colour={}, cell_image={}'.format(
                    row_index, col_index, cell_colour, cell_image
                ))
            canvas.create_rectangle(x, y, x+w, y+w,
                                    outline="black", fill=cell_colour)
            # import os
            # print(os.path.exists("Cross.gif"))
            image_x = x + image_shift
            image_y = y + image_shift
            text_x = x + text_shift
            text_y = y + text_shift
            if cell_image == 'Cross_s.png':
                canvas.create_image(image_x, image_y, anchor=NW, image=photo_Cross)
            elif cell_image == 'Circle_s.png':
                canvas.create_image(image_x, image_y, anchor=NW, image=photo_Circle)
            elif cell_image == 'Star_s.png':
                canvas.create_image(image_x, image_y, anchor=NW, image=photo_Star)
            # NOTE, the following is for game board edges,
            # keep the image name to determine the piece, but simply use text
            elif cell_image == '1_s.png':
                canvas.create_text(text_x, text_y, font="Arial 36 bold", text="1")
            elif cell_image == '2_s.png':
                canvas.create_text(text_x, text_y, font="Arial 36 bold", text="2")
            elif cell_image == '3_s.png':
                canvas.create_text(text_x, text_y, font="Arial 36 bold", text="3")
            elif cell_image == '4_s.png':
                canvas.create_text(text_x, text_y, font="Arial 36 bold", text="4")
            elif cell_image == '5_s.png':
                canvas.create_text(text_x, text_y, font="Arial 36 bold", text="5")
            elif cell_image == 'A_s.png':
                canvas.create_text(text_x, text_y, font="Arial 36 bold", text="A")
            elif cell_image == 'B_s.png':
                canvas.create_text(text_x, text_y, font="Arial 36 bold", text="B")
            elif cell_image == 'C_s.png':
                canvas.create_text(text_x, text_y, font="Arial 36 bold", text="C")
            elif cell_image == 'D_s.png':
                canvas.create_text(text_x, text_y, font="Arial 36 bold", text="D")
            elif cell_image == 'E_s.png':
                canvas.create_text(text_x, text_y, font="Arial 36 bold", text="E")
            x = x + w
        y = y + w
        x = 0
    canvas.pack(fill=BOTH, expand=1)


def determine_cell_colour(step_completed):
    print('function: {}'.format(sys._getframe().f_code.co_name))
    step = steps[step_completed]
    if step.find('piece_picked') != -1:
        cell_colour = cell_colours['piece_picked']
    elif step.find('piece_dropped') != -1:
        cell_colour = cell_colours['piece_dropped']
    else:
        cell_colour = cell_colours[step]
    return cell_colour


def determine_cell_image(current_row_index, current_col_index, step_completed):
    print('function: {}'.format(sys._getframe().f_code.co_name))
    global picked_cell_image
    global picked_cell_image_type
    global steps
    step = steps[step_completed]
    # if picked a piece, update the image picked
    if step.find('piece_picked') != -1:
        picked_cell_image = grid_images[current_row_index][current_col_index]
        picked_cell_image_type = cell_image_types[picked_cell_image]
    # always set set cell_image to the picked one picked or dropped
    cell_image = picked_cell_image
    return cell_image


def determine_step_results(current_row_index, old_row_index, current_col_index, old_col_index):
    print('function: {}'.format(sys._getframe().f_code.co_name))
    row_index_change = current_row_index - old_row_index
    col_index_change = current_col_index - old_col_index
    # NOTE, only horizaontal, vertical, and diagnal move (i.e._index_change == col_index_change) allowed,
    # so, distance moved is the max of the index change
    move_distance = max(row_index_change, col_index_change)
    if row_index_change == 0 and col_index_change > 0:
        step_result = 'E {}'.format(move_distance)
    elif row_index_change < 0 and col_index_change > 0:
        step_result = 'NE {}'.format(move_distance)
    elif row_index_change < 0 and col_index_change == 0:
        step_result = 'N {}'.format(move_distance)
    elif row_index_change < 0 and col_index_change < 0:
        step_result = 'NW {}'.format(move_distance)
    elif row_index_change == 0 and col_index_change < 0:
        step_result = 'W {}'.format(move_distance)
    elif row_index_change > 0 and col_index_change < 0:
        step_result = 'SW {}'.format(move_distance)
    elif row_index_change > 0 and col_index_change == 0:
        step_result = 'S {}'.format(move_distance)
    elif row_index_change > 0 and col_index_change > 0:
        step_result = 'SE {}'.format(move_distance)
    else:
        step_result = 'none'
    return step_result


def determine_piece(step_completed):
    print('function: {}'.format(sys._getframe().f_code.co_name))
    global steps
    step = steps[step_completed]
    if step.find('player') != -1:
        piece = 'player piece'
    elif step.find('neutron') != -1:
        piece = 'neutron piece'
    else:
        piece = 'invalid'
    return piece


def is_valid_move(current_row_index, old_row_index, current_col_index, old_col_index, attempted_step_completed):
    print('function: {}'.format(sys._getframe().f_code.co_name))
    global grid_images
    global steps
    global move_direction_list
    global current_player
    global game_result
    row_index_change = current_row_index - old_row_index
    col_index_change = current_col_index - old_col_index
    step = steps[attempted_step_completed]
    opponent_player_type = 'none'

    if current_player.find('me') != -1:
        opponent_player_type = 'another'
    elif current_player.find('another') != -1:
        opponent_player_type = 'me'

    print('game_result = {}, current_player = {}, '
          'current_row_index = {}, current_col_index = {}, '
          'old_row_index = {}, old_col_index = {}, '
          'attempted_step_completed = {}'.format(
        game_result, current_player,
        current_row_index, current_col_index,
        old_row_index, old_col_index,
        attempted_step_completed
    ))

    # invalid move if current player just completed a move, and attempting to move again
    if ((game_result == 'me move completed' and
            current_player.find('me') != -1) or
        (game_result == 'another move completed' and
            current_player.find('another') != -1)):
        print('you have completed your move, wait for another player')
        return False

    # invlid move if moving to top row or left most column, they are part of the board, never should change
    if current_row_index == 0 or current_col_index == 0:
        print('Top row and the left most column is part of the board')
        return False
    # initialising cell_image
    # cell_image = 'none'
    # cell_image_type = cell_image_types[cell_image]
    if step.find("piece_picked") != -1:
        # NOTE, do NOT call determine_cell_image as it will updates picked_cell_image and picked_cell_image_type,
        # but, if invalid move, picked_cell_image and picked_cell_image_type shouldn't be modified
        # determine_cell_image(current_row_index, current_col_index, step_completed)
        cell_image = grid_images[current_row_index][current_col_index]
        cell_image_type = cell_image_types[cell_image]
        print('picked cell image = {}, picked cell_image_type = {}, '.format(
            cell_image, cell_image_type
        ))
        # invalid move if trying to pick an empty cell
        if cell_image == 'none':
            print('You must pick a piece to move, invalid move')
            return False
        # invalid move if it's neutron step but picked a player piece
        elif step.find("neutron") != -1 and cell_image_type != 'neutron':
            print('Your must move neutron before you can move a piece')
            return False
        # invalid move if it's player piece step but picked neutron
        elif step.find("player") != -1 and cell_image_type == 'neutron':
            print('Your must move a player piece before you can move neutron again')
            return False
        # invalid move if picking up other player's piece
        elif opponent_player_type.find(cell_image_type) != -1:
            print('You picked another player\'s piece, invalid move')
            return False
    # invalid move if dropped at where it was
    elif step.find("piece_dropped") != -1:
        # invalid move if dropping piece in an occuplied cell
        if grid_images[current_row_index][current_col_index] != 'none':
            print('You cannot drop the piece in an occupied cell')
            return False
        # invalid move if not moving the piece
        if row_index_change == 0 and col_index_change == 0:
            print('Each move of a piece must move to a new cell')
            return False
        # invalid move if not moving in straight line, and not in diagonal
        elif not (row_index_change == 0 or col_index_change == 0):
            if abs(row_index_change) != abs(col_index_change):
                print('Each move of a piece must move that piece in one of the eight straight lines: {}'.format(
                    move_direction_list     # '(forward/back/left/right/4 diagonals)')
                ))
                return False

        # NOTE, only do the following checking when dropping a piece, not when picking a piece
        # NOTE, pieces cannot go beyond the edge of the board - already guarantted, see click_me, and click_another
        # invalid move if jumping over pieces -
        # There is no capturing; pieces cannot exist on the same square of the board;
        if check_jumping_over_piece(current_row_index, current_col_index, old_row_index, old_col_index):
            print('Jumping over another piece is not allowed')
            return False

        # invalid move if the move didn't go as far as possible,
        # Each move of a piece must move that piece as far as possible
        furthest_possible_row_index = current_row_index
        furthest_possible_col_index = current_col_index
        # NOTE, moving right, E, row index no change, col index increment
        if row_index_change == 0 and col_index_change > 0:
            furthest_possible_coordinate = get_furthest_possible_move(current_row_index, current_col_index, 'E')
            furthest_possible_row_index = furthest_possible_coordinate[0]
            furthest_possible_col_index = furthest_possible_coordinate[1]
        # NOTE, moving diagonal, NE, abs(row_index_change) = abs(col_index_change), see code above
        # row index decrement, col index increment
        elif row_index_change < 0 and col_index_change > 0:
            furthest_possible_coordinate = get_furthest_possible_move(current_row_index, current_col_index, 'NE')
            furthest_possible_row_index = furthest_possible_coordinate[0]
            furthest_possible_col_index = furthest_possible_coordinate[1]
        # NOTE, moving up, N, row index decrement, col index no change
        elif row_index_change < 0 and col_index_change == 0:
            furthest_possible_coordinate = get_furthest_possible_move(current_row_index, current_col_index, 'N')
            furthest_possible_row_index = furthest_possible_coordinate[0]
            furthest_possible_col_index = furthest_possible_coordinate[1]
        # NOTE, moving diagonal, NW, abs(row_index_change) = abs(col_index_change), see code above
        # row index decrement, col index decrement
        elif row_index_change < 0 and col_index_change < 0:
            furthest_possible_coordinate = get_furthest_possible_move(current_row_index, current_col_index, 'NW')
            furthest_possible_row_index = furthest_possible_coordinate[0]
            furthest_possible_col_index = furthest_possible_coordinate[1]
        # NOTE, moving left, W, row index no change, col index decrement
        elif row_index_change == 0 and col_index_change < 0:
            furthest_possible_coordinate = get_furthest_possible_move(current_row_index, current_col_index, 'W')
            furthest_possible_row_index = furthest_possible_coordinate[0]
            furthest_possible_col_index = furthest_possible_coordinate[1]
        # NOTE, moving diagonal, SW, abs(row_index_change) = abs(col_index_change), see code above
        # row index increment, col index decrement
        elif row_index_change > 0 and col_index_change < 0:
            furthest_possible_coordinate = get_furthest_possible_move(current_row_index, current_col_index, 'SW')
            furthest_possible_row_index = furthest_possible_coordinate[0]
            furthest_possible_col_index = furthest_possible_coordinate[1]
        # NOTE, moving down, S, row index increment, col index no change
        elif row_index_change > 0 and col_index_change == 0:
            furthest_possible_coordinate = get_furthest_possible_move(current_row_index, current_col_index, 'S')
            furthest_possible_row_index = furthest_possible_coordinate[0]
            furthest_possible_col_index = furthest_possible_coordinate[1]
        # NOTE, moving diagonal, SE, abs(row_index_change) = abs(col_index_change), see code above
        # row index increment, col index increment
        elif row_index_change > 0 and col_index_change > 0:
            furthest_possible_coordinate = get_furthest_possible_move(current_row_index, current_col_index, 'SE')
            furthest_possible_row_index = furthest_possible_coordinate[0]
            furthest_possible_col_index = furthest_possible_coordinate[1]

        if (furthest_possible_row_index != current_row_index or
            furthest_possible_col_index != current_col_index):
            print('Move need to go as far as possible')
            return False
    # if all checks passed return True
    return True


def check_jumping_over_piece(current_row_index, current_col_index, old_row_index, old_col_index):
    print('function: {}'.format(sys._getframe().f_code.co_name))
    global grid_images
    row_index_change = current_row_index - old_row_index
    col_index_change = current_col_index - old_col_index
    # invalid move if jumping over pieces -
    # There is no capturing; pieces cannot exist on the same square of the board;
    moved_cells = max(abs(row_index_change), abs(col_index_change))
    print('moved_cells = {}'.format(moved_cells))
    # NOTE, do not use nested loop as it will check around right angle
    for n in range(moved_cells):
        n_one_based = n + 1
        row_index = old_row_index
        col_index = old_col_index
        # NOTE, moving right, E, row index no change, col index increment
        if row_index_change == 0 and col_index_change > 0:
            row_index = old_row_index
            col_index = old_col_index + n_one_based
        # NOTE, moving diagonal, NE, abs(row_index_change) = abs(col_index_change), see code above
        # row index decrement, col index increment
        elif row_index_change < 0 and col_index_change > 0:
            row_index = old_row_index - n_one_based
            col_index = old_col_index + n_one_based
        # NOTE, moving up, N, row index decrement, col index no change
        elif row_index_change < 0 and col_index_change == 0:
            row_index = old_row_index - n_one_based
            col_index = old_col_index
        # NOTE, moving diagonal, NW, abs(row_index_change) = abs(col_index_change), see code above
        # row index decrement, col index decrement
        elif row_index_change < 0 and col_index_change < 0:
            row_index = old_row_index - n_one_based
            col_index = old_col_index - n_one_based
        # NOTE, moving left, W, row index no change, col index decrement
        elif row_index_change == 0 and col_index_change < 0:
            row_index = old_row_index
            col_index = old_col_index - n_one_based
        # NOTE, moving diagonal, SW, abs(row_index_change) = abs(col_index_change), see code above
        # row index increment, col index decrement
        elif row_index_change > 0 and col_index_change < 0:
            row_index = old_row_index + n_one_based
            col_index = old_col_index - n_one_based
        # NOTE, moving down, S, row index increment, col index no change
        elif row_index_change > 0 and col_index_change == 0:
            row_index = old_row_index + n_one_based
            col_index = old_col_index
        # NOTE, moving diagonal, SE, abs(row_index_change) = abs(col_index_change), see code above
        # row index increment, col index increment
        elif row_index_change > 0 and col_index_change > 0:
            row_index = old_row_index + n_one_based
            col_index = old_col_index + n_one_based

        if grid_images[row_index][col_index] != 'none':
            print('n_one_based = {}, row_index = {}, col_index = {}, '
                  'Jumping over another piece'.format(
                n_one_based, row_index, col_index
            ))
            return True
    # if not jumping over piece, return False
    return False


def get_furthest_possible_move(current_row_index, current_col_index, move_direction):
    print('function: {}'.format(sys._getframe().f_code.co_name))
    global grid_images
    furthest_possible_row_index = current_row_index
    furthest_possible_col_index = current_col_index
    # NOTE, moving right, E, row index no change, col index increment
    if move_direction == 'E':       # row_index_change == 0 and col_index_change > 0:
        col_index_edge = 5
        for n in range(abs(col_index_edge - current_col_index)):
            n_one_based = n + 1
            furthest_possible_row_index = current_row_index
            furthest_possible_col_index = current_col_index + n_one_based
            # checking reaching first occupied cell
            if grid_images[furthest_possible_row_index][furthest_possible_col_index] != 'none':
                furthest_possible_col_index -= 1  # reached furthest occupied cell, the left cell is empty
                print('moving E, col_index_edge = {}, n_one_based = {}, '
                      'furthest_possible_row_index = {}, furthest_possible_col_index = {}'.format(
                    col_index_edge, n_one_based,
                    furthest_possible_row_index, furthest_possible_col_index
                ))
                break
    # NOTE, moving diagonal, NE, abs(row_index_change) = abs(col_index_change), see code above
    # row index decrement, col index increment
    elif move_direction == 'NE':        # row_index_change < 0 and col_index_change > 0:
        row_index_edge = 2
        col_index_edge = 5
        for n in range(min(abs(row_index_edge - current_row_index), abs(col_index_edge - current_col_index))):
            n_one_based = n + 1
            furthest_possible_row_index = current_row_index - n_one_based
            furthest_possible_col_index = current_col_index + n_one_based
            # checking reaching first occupied cell
            if grid_images[furthest_possible_row_index][furthest_possible_col_index] != 'none':
                furthest_possible_row_index += 1  # reached furthest occupied cell, the lower-left cell is empty
                furthest_possible_col_index -= 1  # reached furthest occupied cell, the lower-left cell is empty
                print('moving NE, row_index_edge = {}, col_index_edge = {}, n_one_based = {}, '
                      'furthest_possible_row_index = {}, furthest_possible_col_index = {}'.format(
                    row_index_edge, col_index_edge, n_one_based,
                    furthest_possible_row_index, furthest_possible_col_index
                ))
                break
    # NOTE, moving up, N, row index decrement, col index no change
    elif move_direction == 'N':     # row_index_change < 0 and col_index_change == 0:
        row_index_edge = 2
        for n in range(abs(row_index_edge - current_row_index)):
            n_one_based = n + 1
            furthest_possible_row_index = current_row_index - n_one_based
            furthest_possible_col_index = current_col_index
            # checking reaching first occupied cell
            if grid_images[furthest_possible_row_index][furthest_possible_col_index] != 'none':
                furthest_possible_row_index += 1  # reached furthest occupied cell, the lower cell is empty
                print('moving N, row_index_edge = {}, n_one_based = {}, '
                      'furthest_possible_row_index = {}, furthest_possible_col_index = {}'.format(
                    row_index_edge, n_one_based,
                    furthest_possible_row_index, furthest_possible_col_index
                ))
                break
    # NOTE, moving diagonal, NW, abs(row_index_change) = abs(col_index_change), see code above
    # row index decrement, col index decrement
    elif move_direction == 'NW':        # row_index_change < 0 and col_index_change < 0:
        row_index_edge = 2
        col_index_edge = 1
        for n in range(min(abs(row_index_edge - current_row_index), abs(col_index_edge - current_col_index))):
            n_one_based = n + 1
            furthest_possible_row_index = current_row_index - n_one_based
            furthest_possible_col_index = current_col_index - n_one_based
            # checking reaching first occupied cell
            if grid_images[furthest_possible_row_index][furthest_possible_col_index] != 'none':
                furthest_possible_row_index += 1  # reached furthest occupied cell, the lower-right cell is empty
                furthest_possible_col_index += 1  # reached furthest occupied cell, the lower-right cell is empty
                print('moving NW, row_index_edge = {}, col_index_edge = {}, n_one_based = {}, '
                      'furthest_possible_row_index = {}, furthest_possible_col_index = {}'.format(
                    row_index_edge, col_index_edge, n_one_based,
                    furthest_possible_row_index, furthest_possible_col_index
                ))
                break
    # NOTE, moving left, W, row index no change, col index decrement
    elif move_direction == 'W':     # row_index_change == 0 and col_index_change < 0:
        col_index_edge = 1
        for n in range(abs(col_index_edge - current_col_index)):
            n_one_based = n + 1
            furthest_possible_row_index = current_row_index
            furthest_possible_col_index = current_col_index - n_one_based
            # checking reaching first occupied cell
            if grid_images[furthest_possible_row_index][furthest_possible_col_index] != 'none':
                furthest_possible_col_index += 1  # reached furthest occupied cell, the right cell is empty
                print('moving W, col_index_edge = {}, n_one_based = {}, '
                      'furthest_possible_row_index = {}, furthest_possible_col_index = {}'.format(
                    col_index_edge, n_one_based,
                    furthest_possible_row_index, furthest_possible_col_index
                ))
                break
    # NOTE, moving diagonal, SW, abs(row_index_change) = abs(col_index_change), see code above
    # row index increment, col index decrement
    elif move_direction == 'SW':        # row_index_change > 0 and col_index_change < 0:
        row_index_edge = 5
        col_index_edge = 1
        for n in range(min(abs(row_index_edge - current_row_index), abs(col_index_edge - current_col_index))):
            n_one_based = n + 1
            furthest_possible_row_index = current_row_index + n_one_based
            furthest_possible_col_index = current_col_index - n_one_based
            # checking reaching first occupied cell
            if grid_images[furthest_possible_row_index][furthest_possible_col_index] != 'none':
                furthest_possible_row_index -= 1  # reached furthest occupied cell, the upper-right cell is empty
                furthest_possible_col_index += 1  # reached furthest occupied cell, the upper-right cell is empty
                print('moving SW, row_index_edge = {}, col_index_edge = {}, n_one_based = {}, '
                      'furthest_possible_row_index = {}, furthest_possible_col_index = {}'.format(
                    row_index_edge, col_index_edge, n_one_based,
                    furthest_possible_row_index, furthest_possible_col_index
                ))
                break
    # NOTE, moving down, S, row index increment, col index no change
    elif move_direction == 'S':     # row_index_change > 0 and col_index_change == 0:
        row_index_edge = 5
        for n in range(abs(row_index_edge - current_row_index)):
            n_one_based = n + 1
            furthest_possible_row_index = current_row_index + n_one_based
            furthest_possible_col_index = current_col_index
            # checking reaching first occupied cell
            if grid_images[furthest_possible_row_index][furthest_possible_col_index] != 'none':
                furthest_possible_row_index -= 1  # reached furthest occupied cell, the upper cell is empty
                print('moving SW, row_index_edge = {}, n_one_based = {}, '
                      'furthest_possible_row_index = {}, furthest_possible_col_index = {}'.format(
                    row_index_edge, n_one_based,
                    furthest_possible_row_index, furthest_possible_col_index
                ))
                break
    # NOTE, moving diagonal, SE, abs(row_index_change) = abs(col_index_change), see code above
    # row index increment, col index increment
    elif move_direction == 'SE':     # move_direction == 'SE':        # row_index_change > 0 and col_index_change > 0:
        row_index_edge = 5
        col_index_edge = 5
        for n in range(min(abs(row_index_edge - current_row_index), abs(col_index_edge - current_col_index))):
            n_one_based = n + 1
            furthest_possible_row_index = current_row_index + n_one_based
            furthest_possible_col_index = current_col_index + n_one_based
            # checking reaching first occupied cell
            if grid_images[furthest_possible_row_index][furthest_possible_col_index] != 'none':
                furthest_possible_row_index -= 1  # reached furthest occupied cell, the upper-left cell is empty
                furthest_possible_col_index -= 1  # reached furthest occupied cell, the upper-left cell is empty
                print('moving SE, row_index_edge = {}, col_index_edge = {}, n_one_based = {}, '
                      'furthest_possible_row_index = {}, furthest_possible_col_index = {}'.format(
                    row_index_edge, col_index_edge, n_one_based,
                    furthest_possible_row_index, furthest_possible_col_index
                ))
                break

    return [furthest_possible_row_index, furthest_possible_col_index]


def possible_move_generator(current_row_index, current_col_index):
    print('function: {}'.format(sys._getframe().f_code.co_name))
    e_move = get_furthest_possible_move(current_row_index, current_col_index, 'E')
    ne_move = get_furthest_possible_move(current_row_index, current_col_index, 'NE')
    n_move = get_furthest_possible_move(current_row_index, current_col_index, 'N')
    nw_move = get_furthest_possible_move(current_row_index, current_col_index, 'NW')
    w_move = get_furthest_possible_move(current_row_index, current_col_index, 'W')
    sw_move = get_furthest_possible_move(current_row_index, current_col_index, 'SW')
    s_move = get_furthest_possible_move(current_row_index, current_col_index, 'S')
    se_move = get_furthest_possible_move(current_row_index, current_col_index, 'SE')

    return {'E': e_move,
            'NE': ne_move,
            'N': n_move,
            'NW': nw_move,
            'W': w_move,
            'SW': sw_move,
            'S': s_move,
            'SE': se_move}


def show_possible_moves(current_row_index, current_col_index):
    print('function: {}'.format(sys._getframe().f_code.co_name))
    global grid_colours
    possible_moves = possible_move_generator(current_row_index, current_col_index)
    for m in range(total_row):
        for n in range(total_col):
            for key, value in possible_moves.items():
                if value[0] == m and value[1] == n:
                    grid_colours[m][n] = cell_colours['possible_move']


def hide_possible_moves():
    print('function: {}'.format(sys._getframe().f_code.co_name))
    global grid_colours
    for m in range(total_row):
        for n in range(total_col):
            if grid_colours[m][n] == cell_colours['possible_move']:
                grid_colours[m][n] = cell_colours['board']


def check_game_result(step_completed, current_player):
    print('function: {}'.format(sys._getframe().f_code.co_name))
    global steps
    # value options for result, i.e. game_result
    # game_result values:
    # 'none',
    # 'me move completed' for me_xxx
    # 'another move completed' for another_xxx
    # 'game over, you won' for me_xxx,
    # 'game over, you lost' for me_xxx
    result = 'none'

    if step_completed == len(steps.keys()) - 1:
        if current_player.find('me') != -1:
            result = 'me move completed'
        elif current_player.find('another')!= -1:
            result = 'another move completed'

    # set the neutron index to default value first
    neutron_row_index = 3
    neutron_col_index = 3
    for i in range(total_row):
        for j in range (total_col):
            if grid_images[i][j] == 'Star_s.png':
                neutron_row_index = i
                neutron_col_index = j
                # checking - game over if neutron is trapped
                if check_neutron_trapped(neutron_row_index, neutron_col_index):
                    if current_player.find('another') != -1:
                        result = 'game over, you lost'
                    else:
                        result = 'game over, you won'
                    break
                # checking - neutron reached opponent's base row
                elif current_player.find('me') != -1:
                    opponent_base_row = 1
                    for i in range(total_col):
                        if grid_images[opponent_base_row][i] == 'Star_s.png':
                            result = 'game over, you won'
                            break
                elif current_player.find('another') != -1:
                    opponent_base_row = total_row - 1
                    for i in range(total_col):
                        if grid_images[opponent_base_row][i] == 'Star_s.png':
                            result = 'game over, you lost'
                            break
    # the following is just for testing - mimick game over - need to be removed once done
    #result = 'game over, you won'
    return result


def check_neutron_trapped(neutron_row_index, neutron_col_index):
    print('function: {}'.format(sys._getframe().f_code.co_name))
    global grid_images
    game_over = False
    # NOTE, the following goes clockwise
    left_row = neutron_row_index
    left_col = neutron_col_index - 1
    top_left_row = neutron_row_index - 1
    top_left_col = neutron_col_index - 1
    top_row = neutron_row_index - 1
    top_col = neutron_col_index
    top_right_row = neutron_row_index - 1
    top_right_col = neutron_col_index + 1
    right_row = neutron_row_index
    right_col = neutron_col_index + 1
    lower_right_row = neutron_row_index + 1
    lower_right_col = neutron_col_index + 1
    lower_row = neutron_row_index + 1
    lower_col = neutron_col_index
    lower_left_row = neutron_row_index + 1
    lower_left_col = neutron_col_index + 1

    left_trapped = False
    if left_row <= 1 or left_row > 5:
        left_trapped = True
    elif left_col <= 1 or left_col > 5:
        left_trapped = True
    elif grid_images[left_row][left_col] != 'none':
        left_trapped = True

    lower_left_trapped = False
    if lower_left_row <= 1 or lower_left_row > 5:
        lower_left_trapped = True
    elif lower_left_col <= 1 or lower_left_col > 5:
        lower_left_trapped = True
    elif grid_images[lower_left_row][lower_left_col] != 'none':
        lower_left_trapped = True

    lower_trapped = False
    if lower_row <= 1 or lower_row > 5:
        lower_trapped = True
    elif lower_col <= 1 or lower_col > 5:
        lower_trapped = True
    elif grid_images[lower_row][lower_col] != 'none':
        lower_trapped = True

    lower_right_trapped = False
    if lower_right_row <= 1 or lower_right_row > 5:
        lower_right_trapped = True
    elif lower_right_col <= 1 or lower_right_col > 5:
        lower_right_trapped = True
    elif grid_images[lower_right_row][lower_right_col] != 'none':
        lower_right_trapped = True

    right_trapped = False
    if right_row <= 1 or right_row > 5:
        right_trapped = True
    elif right_col <= 1 or right_col > 5:
        right_trapped = True
    elif grid_images[right_row][right_col] != 'none':
        right_trapped = True

    top_right_trapped = False
    if top_right_row <= 1 or top_right_row > 5:
        top_right_trapped = True
    elif top_right_col <= 1 or top_right_col > 5:
        top_right_trapped = True
    elif grid_images[top_right_row][top_right_col] != 'none':
        top_right_trapped = True

    top_trapped = False
    if top_row <= 1 or top_row > 5:
        top_trapped = True
    elif top_col <= 1 or top_col > 5:
        top_trapped = True
    elif grid_images[top_row][top_col] != 'none':
        top_trapped = True

    top_left_trapped = False
    if top_left_row <= 1 or top_left_row > 5:
        top_left_trapped = True
    elif top_left_col <= 1 or top_left_col > 5:
        top_left_trapped = True
    elif grid_images[top_left_row][top_left_col] != 'none':
        top_left_trapped = True

    if (left_trapped and lower_left_trapped and lower_trapped and lower_right_trapped and
            right_trapped and top_right_trapped and top_trapped and top_left_trapped):
        game_over = True

    return game_over


def reset_game_params():
    print('function: {}'.format(sys._getframe().f_code.co_name))
    global current_player
    global game_result
    global grid_images
    global grid_colours
    global grid_images_default
    global grid_colours_default
    global picked_cell_image
    global picked_cell_image_type
    global step_completed_me
    global step_completed_another
    global old_row_index_me
    global old_col_index_me
    global old_row_index_another
    global old_col_index_another

    print('resetting game params.....')
    current_player = 'none'
    game_result = 'none'

    reset_grid_pattern()

    picked_cell_image = 'none'
    picked_cell_image_type = cell_image_types[picked_cell_image]

    step_completed_me = 0
    step_completed_another = 0

    old_row_index_me = -1
    old_col_index_me = -1

    old_row_index_another = -1
    old_col_index_another = -1


# test example callback
def motion(event):
    x, y = event.x, event.y
    print('{}, {}'.format(x/w, y/w))


def click_me(event):
    print('function: {}'.format(sys._getframe().f_code.co_name))
    global old_row_index_me
    global old_col_index_me
    global current_player
    global step_completed_me
    global step_completed_another
    global game_result
    global steps
    global picked_cell_image
    global picked_cell_image_type
    your_turn = step_completed_another == 0 or step_completed_another == len(steps.keys())-1
    if not your_turn:
        print('the other player has not yet completed their move, please wait')
    else:
        x, y = event.x, event.y
        row_index = int(y/w)
        col_index = int(x/w)
        if row_index > total_row-1 or col_index > total_col-1:
            print('row index {} or col index {} out of range'.format(
                row_index, col_index
            ))
        else:
            current_player = 'me_human'
            attempted_step_completed = step_completed_me + 1
            if steps[attempted_step_completed].find('piece_picked') != -1:
                old_row_index_me = row_index
                old_col_index_me = col_index
            # NOTE, we are checking if the player picked opponent's piece, so use 'another' instead of 'me' here
            if is_valid_move(row_index, old_row_index_me, col_index, old_col_index_me,
                             attempted_step_completed):
                if steps[attempted_step_completed].find('piece_picked') != -1:
                    show_possible_moves(row_index, col_index)
                elif steps[attempted_step_completed].find('piece_dropped') != -1:
                    hide_possible_moves()
                cell_colour = determine_cell_colour(attempted_step_completed)
                # NOTE, determine_cell_image has to be prior to updating grid_images to determine what piece is picked
                cell_image = determine_cell_image(row_index, col_index, attempted_step_completed)
                grid_colours[row_index][col_index] = cell_colour
                grid_images[row_index][col_index] = cell_image
                if steps[attempted_step_completed].find('piece_dropped') != -1:
                    grid_colours[old_row_index_me][old_col_index_me] = cell_colours['board']
                    grid_images[old_row_index_me][old_col_index_me] = cell_images['board']
                draw_game_board(canvas)
                step_result = determine_step_results(row_index, old_row_index_me, col_index, old_col_index_me)
                # all done, set new global values
                step_completed_me += 1
                piece = determine_piece(step_completed_me)
                print('{} moved {}: {}'.format(
                    current_player, piece, step_result
                ))
                old_row_index_me = row_index
                old_col_index_me = col_index
                # completed the move, reset globals
                if step_completed_me == 4:
                    game_result = check_game_result(step_completed_me, current_player)
                    if game_result == 'me move completed':
                        print('game_result = {}, your move is completed, wait for other player'.format(
                            game_result
                        ))
                    elif game_result == 'game over, you won' or game_result == 'game over, you lost':
                        # d = MyDialog(root)
                        # print('d.result = {}'.format(d.result))
                        # if d.result is None:
                        if messagebox.askyesno("Game result", '{}, redraw game board?'.format(game_result)):
                            reset_game_params()
                            print('game_result = {}, redrawing game board....'.format(
                                game_result
                            ))
                            draw_game_board(canvas)
                    # game_result = 'none'
                    step_completed_me = 0
                    old_row_index_me = -1
                    old_col_index_me = -1
                    picked_cell_image = 'none'
                    picked_cell_image_type = cell_image_types[picked_cell_image]
            else:
                #TODO, display popup dialog to warn the user
                print('Invalid move')


def click_another(event):
    print('function: {}'.format(sys._getframe().f_code.co_name))
    global old_row_index_another
    global old_col_index_another
    global current_player
    global step_completed_me
    global step_completed_another
    global game_result
    global picked_cell_image
    global picked_cell_image_type
    your_turn = step_completed_me == 0 or step_completed_me == len(steps.keys())-1
    if not your_turn:
        print('the other player has not yet completed their move, please wait')
    else:
        x, y = event.x, event.y
        row_index = int(y/w)
        col_index = int(x/w)
        if row_index > total_row-1 or col_index > total_col-1:
            print('row index {} or col index {} out of range'.format(
                row_index,col_index
            ))
        else:
            current_player = 'another_human'
            attempted_step_completed = step_completed_another + 1
            if steps[attempted_step_completed].find('piece_picked') != -1:
                old_row_index_another = row_index
                old_col_index_another = col_index
            if is_valid_move(row_index, old_row_index_another, col_index, old_col_index_another,
                             attempted_step_completed):
                if steps[attempted_step_completed].find('piece_picked') != -1:
                    show_possible_moves(row_index, col_index)
                elif steps[attempted_step_completed].find('piece_dropped') != -1:
                    hide_possible_moves()
                cell_colour = determine_cell_colour(attempted_step_completed)
                # NOTE, determine_cell_image has to be prior to updating grid_images to determine what piece is picked
                cell_image = determine_cell_image(row_index, col_index, attempted_step_completed)
                grid_colours[row_index][col_index] = cell_colour
                grid_images[row_index][col_index] = cell_image
                if steps[attempted_step_completed].find('piece_dropped') != -1:
                    grid_colours[old_row_index_another][old_col_index_another] = cell_colours['board']
                    grid_images[old_row_index_another][old_col_index_another] = cell_images['board']
                draw_game_board(canvas)
                step_result = determine_step_results(row_index, old_row_index_another, col_index, old_col_index_another)
                # all done, set new global values
                step_completed_another += 1
                piece = determine_piece(step_completed_another)
                print('{} moved {}: {}'.format(
                    current_player, piece, step_result
                ))
                old_row_index_another = row_index
                old_col_index_another = col_index
                # completed the move, reset globals
                if step_completed_another == 4:
                    game_result = check_game_result(step_completed_another, current_player)
                    if game_result == 'another move completed':
                        print('game_result = {}, your move is completed, wait for other player'.format(
                            game_result
                        ))
                    elif game_result == 'game over, you won' or game_result == 'game over, you lost':
                        # d = MyDialog(root)
                        # print('d.result = {}'.format(d.result))
                        # if d.result is None:
                        if messagebox.askyesno("Game result", '{}, redraw game board?'.format(game_result)):
                            reset_game_params()
                            print('game_result = {}, redrawing game board....'.format(
                                game_result
                            ))
                            draw_game_board(canvas)
                    # game_result = 'none'
                    step_completed_another = 0
                    old_row_index_another = -1
                    old_col_index_another = -1
                    picked_cell_image = 'none'
                    picked_cell_image_type = cell_image_types[picked_cell_image]
            else:
                # TODO, display popup dialog to warn the user
                print('Invalid move')


def main():
    # Note, to initialise the board, pass a hard coded zero to draw the board cell in blue
    reset_grid_pattern()
    draw_game_board(canvas)
    canvas.bind('<Button-1>', click_me) # left mouse click is always me - can be human or computer
    canvas.bind('<Button-3>', click_another) # right mouse click is always another player - can be human or computer
    root.mainloop()

    # root = Tk()
    # #draw = DrawLines()
    # #draw = DrawColourRects()
    # #draw = DrawGameBoard()
    # #root.geometry("400x250+300+300")
    # root.geometry("800x600")
    # #root.bind('<Motion>', motion)
    # root.bind('<Button-1>', click)
    # root.mainloop()

    # root.geometry("500x900")
    # canvas = Canvas(root, width=550, height=820)
    # canvas.pack()
    # #png = PhotoImage(file = r'example.png') # Just an example
    # #canvas.create_image(0, 0, image = png, anchor = "nw")
    #
    # a = canvas.create_rectangle(50, 0, 100, 50, fill='red')
    # canvas.move(a, 20, 20)


if __name__ == '__main__':
    main()
