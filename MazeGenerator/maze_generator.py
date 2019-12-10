#! python

import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
#import tkinter as tk
#from tkinter import Tk, Canvas, Frame, BOTH
from tkinter import messagebox

import tkSimpleDialog
import sys      # for using sys._getframe().f_code.co_name to retrieve function name for debugging
import random   # for generating a random number for computer player to decide which player piece to move

# custom dialog for choosing player
from MyDialog import *
from collections import namedtuple


# type def
# this will be used as the key of the container of unique lines, to speed/simplfy drawing,
Line_Corrd = namedtuple('Single_BlockBorder', ['x_b', 'y_b', 'x_e', 'y_e'])

# below is the definition for each single border
# x_b: x beginning coordinate, int
# y_b: y beginning coordinate, int
# x_e: x end coordinate, int
# y_e: y end coordinate, int
# to_draw: to_draw flag, int, 0: not, 1: yes
Single_BlockBorder = namedtuple('Single_BlockBorder', ['x_b', 'y_b', 'x_e', 'y_e', 'to_draw'])

# below is the definition of a single block including four borders
# each element is a Single_BlockBorder object
# t: top border - a Single_BlockBorder object
# b: bottom border - a Single_BlockBorder object
# l: left border - a Single_BlockBorder object
# r: right border - a Single_BlockBorder object
Single_Block_With_Four_Borders = namedtuple('Single_Block_With_Four_Borders', ['t', 'b', 'l', 'r'])

# below is the path_id's for the four meighbors of a block
# t_p: path_id for the block on top of the current block, int
# b_p: path_id for the block at the bottom of the current block, int
# l_p: path_id for the block to the left of the current block, int
# r_p: path_id for the block to the right of the current block, int
# -1: block on the border of the grid
Block_NeighborPaths = namedtuple('Block_NeighborPaths', ['t_p', 'b_p', 'l_p', 'r_p'])
Block_Index_NeighborPaths_Pair = namedtuple('Block_Index_NeighborPaths_Pair', ['block_index', 'block_neighborpaths'])

Block_Index = namedtuple('Block_Index', ['i', 'j'])


# initialise values
create_same_randomised_array = True
global_flag_path = True
draw_block = True
special_rule_for_path1 = True
# note, when setting total_rows and total_cols to 50, interestingly:
# 1. if setting special_rules_for_path to ['D', 'R', 'L', 'U'], block coverage can be to 0.51,
#    results generated very quickly, but if setting to 0.41, locked in loop
# 2. if setting special_rules_for_path to ['D', 'R'], block coverage can be set to 0.49,
#    results generated very quickly, but if setting to 0.5, locked in loop
special_rules_for_path = ['D', 'R', 'L', 'U']   # ['D', 'R']    # ['D', 'R', 'L']   #
# note when setting a 50x50 grid, the block converage threshold has to be set lower to avoid being trapped
block_in_path_percentage_threshold = 0.81   # 0.92   # 0.9   #
draw_debug = False
print_func_name = False
test_or_for_line_container = False
global_prioritise_current_path = True

total_rows = 18
total_cols = 18
# width of each block
w = 10
text_shift = int(w/2)
root_width = w*total_cols+6
root_height = w*total_rows+6
root_geometry_str = '{}x{}'.format(root_width, root_height)

entrance = Block_Index(0, 0)
exit = Block_Index(total_rows-1, total_cols-1)

# below is to initialise the maze, set all the border coordinate to (0, 0, 0, 0)
# and each border to_draw flag set to 1, ie. draw
maze = [[Single_Block_With_Four_Borders(
    Single_BlockBorder(0, 0, 0, 0, 1),
    Single_BlockBorder(0, 0, 0, 0, 1),
    Single_BlockBorder(0, 0, 0, 0, 1),
    Single_BlockBorder(0, 0, 0, 0, 1))] * total_cols for n in range(total_rows)]

# maze_path is primarily for making sure the constraints are satisfied, ie. every point linked to entrance/exit?
# element[0]=0: the block is not included in any route
# element[0]>0: the block is included in one route, the value will be path_ID
# element[1]: path mark character if set to draw when element[0]>0
maze_path = [[0] * total_cols for mp in range(total_rows)]
maze_path_text = [['X'] * total_cols for mpt in range(total_rows)]


def reset_maze_properties(maze_param, w_param):
    if print_func_name:
        print('function: {}'.format(sys._getframe().f_code.co_name))

    # reset the maze:
    # 1. calculate border coordinates for all blocks,
    # 2, set their to_draw flags to 1, i.e. to be drawn.
    line_container = dict()
    x, y = 2, 2
    for i in range(total_rows):
        for j in range(total_cols):
            # Note, for namedtuple, cannot set atribute value, override is the only option
            # Note, x -> col, y -> row
            maze_param[i][j] = Single_Block_With_Four_Borders(
                Single_BlockBorder(x, y, x+w_param, y, 1),
                Single_BlockBorder(x, y+w_param, x+w_param, y+w_param, 1),
                Single_BlockBorder(x, y, x, y+w_param, 1),
                Single_BlockBorder(x+w_param, y, x+w_param, y+w_param, 1))
            x = x + w
        y = y + w
        x = 2


def get_lines(maze_param):
    if print_func_name:
        print('function: {}'.format(sys._getframe().f_code.co_name))

    line_container = dict()
    for i in range(total_rows):
        for j in range(total_cols):
            line_key_t = Line_Corrd(maze_param[i][j].t.x_b, maze_param[i][j].t.y_b,
                                    maze_param[i][j].t.x_e, maze_param[i][j].t.y_e)
            if line_key_t in line_container.keys():
                if not test_or_for_line_container:
                    line_container[line_key_t] = (maze_param[i][j].t.to_draw == 1) and line_container[line_key_t]
                else:
                    line_container[line_key_t] = (maze_param[i][j].t.to_draw == 1) or line_container[line_key_t]
            else:
                line_container[line_key_t] = maze_param[i][j].t.to_draw == 1

            line_key_b = Line_Corrd(maze_param[i][j].b.x_b, maze_param[i][j].b.y_b,
                                    maze_param[i][j].b.x_e, maze_param[i][j].b.y_e)
            if line_key_b in line_container.keys():
                if not test_or_for_line_container:
                    line_container[line_key_b] = (maze_param[i][j].b.to_draw == 1) and line_container[line_key_b]
                else:
                    line_container[line_key_b] = (maze_param[i][j].b.to_draw == 1) or line_container[line_key_b]
            else:
                line_container[line_key_b] = maze_param[i][j].b.to_draw == 1

            line_key_l = Line_Corrd(maze_param[i][j].l.x_b, maze_param[i][j].l.y_b,
                                    maze_param[i][j].l.x_e, maze_param[i][j].l.y_e)
            if line_key_l in line_container.keys():
                if not test_or_for_line_container:
                    line_container[line_key_l] = (maze_param[i][j].l.to_draw == 1) and line_container[line_key_l]
                else:
                    line_container[line_key_l] = (maze_param[i][j].l.to_draw == 1) or line_container[line_key_l]
            else:
                line_container[line_key_l] = maze_param[i][j].l.to_draw == 1

            line_key_r = Line_Corrd(maze_param[i][j].r.x_b, maze_param[i][j].r.y_b,
                                    maze_param[i][j].r.x_e, maze_param[i][j].r.y_e)
            if line_key_r in line_container.keys():
                if not test_or_for_line_container:
                    line_container[line_key_r] = (maze_param[i][j].r.to_draw == 1) and line_container[line_key_r]
                else:
                    line_container[line_key_r] = (maze_param[i][j].r.to_draw == 1) or line_container[line_key_r]
            else:
                line_container[line_key_r] = maze_param[i][j].r.to_draw == 1
    print('line_container='.format(line_container))
    return line_container


def draw_maze_use_block(canvas_param, maze_param, maze_path_param, maze_path_text_param, text_shiift_param):
    if print_func_name:
        print('function: {}'.format(sys._getframe().f_code.co_name))

    canvas_param.delete('all')

    # note, this function doesn't take in to acount the fact that overlapping borders can have
    # different properties, the grosss efect is that the obrder has been taken out of drawing
    # by one blcok could be added back in by another block, block value set the route,
    # >0: in a route, =0 not included in any route
    for i in range(total_rows):
        for j in range(total_cols):
            # print('maze_param[{}][{}].t.to_draw={}'.format(i, j, maze_param[i][j].t.to_draw))
            if maze_param[i][j].t.to_draw == 1:
                canvas_param.create_line(maze_param[i][j].t.x_b, maze_param[i][j].t.y_b, maze_param[i][j].t.x_e, maze_param[i][j].t.y_e)
            if maze_param[i][j].b.to_draw == 1:
                canvas_param.create_line(maze_param[i][j].b.x_b, maze_param[i][j].b.y_b, maze_param[i][j].b.x_e, maze_param[i][j].b.y_e)
            if maze_param[i][j].l.to_draw == 1:
                canvas_param.create_line(maze_param[i][j].l.x_b, maze_param[i][j].l.y_b, maze_param[i][j].l.x_e, maze_param[i][j].l.y_e)
            if maze_param[i][j].r.to_draw == 1:
                canvas_param.create_line(maze_param[i][j].r.x_b, maze_param[i][j].r.y_b, maze_param[i][j].r.x_e, maze_param[i][j].r.y_e)
            # if global_flag_path and maze_path_param[i][j] > 0:
            #     text_x = maze_param[i][j].t.x_b + text_shiift_param
            #     text_y = maze_param[i][j].t.y_b + text_shiift_param
            #     font_size = int(w/2)+1
            #     font_str = "Arial {}".format(font_size)
            #     text_to_draw = str(maze_path_param[i][j])    # maze_path_text_param[i][j]
            #     # print('text_to_draw={}'.format(text_to_draw))
            #     canvas_param.create_text(text_x, text_y, font=font_str, text=text_to_draw)
            text_x = maze_param[i][j].t.x_b + text_shiift_param
            text_y = maze_param[i][j].t.y_b + text_shiift_param
            font_size = int(w/2)+1
            font_str = "Arial {}".format(font_size)
            text_to_draw = str(maze_path_param[i][j])    # maze_path_text_param[i][j]
            # print('text_to_draw={}'.format(text_to_draw))
            canvas_param.create_text(text_x, text_y, font=font_str, text=text_to_draw)

    canvas_param.pack(fill=BOTH, expand=1)
    # canvas_param.pack(fill=BOTH, expand=0)


def draw_maze_use_line(canvas_param, line_container_param):
    if print_func_name:
        print('function: {}'.format(sys._getframe().f_code.co_name))

    canvas_param.delete('all')

    # note, this function does take in to acount the overlapping borders,
    # all lines in line_container_param, are unique, keyed on their coordinates
    # ref. get_lines
    for k, v in line_container_param.items():
        if v:
            print('line({}).to_draw={}'.format(k, v))
            canvas_param.create_line(k.x_b, k.y_b, k.x_e, k.y_e)

    canvas_param.pack(fill=BOTH, expand=1)
    # following tests for the margin needed for the whole plot to be displayed properly
    # canvas_param.pack(fill=BOTH, expand=0)


def set_block_borders_random(block_param, row_index_param, col_index_param):
    if print_func_name:
        print('function: {}'.format(sys._getframe().f_code.co_name))

    # note, if the border lies on the grid outer borader always set to_draw to true
    t_to_draw = 1
    b_to_draw = 1
    l_to_draw = 1
    r_to_draw = 1
    if row_index_param == 0:
        t_to_draw = 1
    else:
        t_to_draw = get_random_bool()
    if row_index_param == total_rows-1:
        b_to_draw = 1
    else:
        b_to_draw = get_random_bool()
    if col_index_param == 0:
        l_to_draw = 1
    else:
        l_to_draw = get_random_bool()
    if col_index_param == total_cols-1:
        r_to_draw = 1
    else:
        r_to_draw = get_random_bool()
    # print('t_to_draw={}, b_to_draw={}, l_to_draw={}, r_to_draw={}'.format(t_to_draw, b_to_draw, l_to_draw, r_to_draw))
    # Note, for namedtuple, cannot set atribute value, override is the only option
    return Single_Block_With_Four_Borders(
        Single_BlockBorder(block_param.t.x_b, block_param.t.y_b, block_param.t.x_e, block_param.t.y_e, t_to_draw),
        Single_BlockBorder(block_param.b.x_b, block_param.b.y_b, block_param.b.x_e, block_param.b.y_e, b_to_draw),
        Single_BlockBorder(block_param.l.x_b, block_param.l.y_b, block_param.l.x_e, block_param.l.y_e, l_to_draw),
        Single_BlockBorder(block_param.r.x_b, block_param.r.y_b, block_param.r.x_e, block_param.r.y_e, r_to_draw))


def set_maze_to_draw_random(maze_param):
    for i in range(total_rows):
        for j in range(total_cols):
            maze_param[i][j] = set_block_borders_random(maze_param[i][j], i, j)


def get_random_bool():
    list = [1,2,3,4,5,6,7,8,9,10]
    if random.choice(list) > 5:
        return True
    return False


def reset_maxe_path_and_maze_path_text(maze_path_param, maze_path_text_param):
    if print_func_name:
        print('function: {}'.format(sys._getframe().f_code.co_name))

    # reset all blocks in maze_path_param to 0, i.e. not included in any path
    # and maze_path_text_param to 'X'
    for i in range(total_rows):
        for j in range(total_cols):
            maze_path_param[i][j] = 0
            maze_path_text_param[i][j] = 'X'


def get_blocks_in_path_percentage(maze_path_param):
    if print_func_name:
        print('function: {}'.format(sys._getframe().f_code.co_name))

    # check all points of the mase included in a randomly generated path
    in_path_count = 0
    for i in range(total_rows):
        for j in range(total_cols):
            if maze_path_param[i][j]> 0:
                in_path_count += 1
    in_path_percentage = in_path_count/(total_rows * total_cols)
    return in_path_percentage


def create_path(start_block_index_param: Block_Index, path_id_param, special_rules_for_path_param,
                maze_param, maze_path_param, maze_path_text_param):
    if print_func_name:
        print('function: {}'.format(sys._getframe().f_code.co_name))

    # when setting maze path:
    # 1. randomly generate a path from entance to exit, give it a path_ID, i.e. 1
    # 2. link as many blocks as possible to the path, i.e. mark the block in maze_path array to path_ID,
    #    this is to ensure that all points connect to the entrance, when exhausted, question here is,
    #    should we link a path ID to a block? and all other points on the path too?
    # 3. randomly generate a new path, starting from a block on the current path, and, give it a new path ID,
    #    say, current_path_ID+1, and then somehow, check this new path jointed to the path that it span out from,
    #    then merge, how?
    # 4. repeat step 2~3

    # note, for this aplication, perhaps not suitable to use recursive functions,
    # because the results are not incemental, basically, the strategy is to define a new start block
    # start a new path, the step that repeatedly creating a path is done in main
    # go_recursive = False

    path_index_list = list()
    if (maze_path_param[start_block_index_param.i][start_block_index_param.j] == 0):
        maze_path_param[start_block_index_param.i][start_block_index_param.j] = path_id_param
        path_index_list.append(start_block_index_param)

    current_block_index = start_block_index_param
    # note, do not get the block_neighbors in the while loop, because the next block on the path
    # may change the property, so get the neighbor properties after the path has been constructed
    while True:
        # go_recursive = False
        move_direction = get_move_direction(current_block_index, path_id_param, special_rules_for_path_param,
                                            maze_param, maze_path_param)
        print('move_direction={}'.format(move_direction))
        # cannot move, exit
        # if move_direction == 'N/A':
        #     return None, maze_param, maze_path_param, maze_path_text_param

        block_text = get_block_text(move_direction)
        next_block_index = get_next_block_index(current_block_index, move_direction)
        if ((next_block_index.i == current_block_index.i and next_block_index.j == current_block_index.j) or
            (next_block_index.i == entrance.i and next_block_index.j == entrance.j)):
            maze_path_param[current_block_index.i][current_block_index.j] = path_id_param
            maze_path_text_param[current_block_index.i][current_block_index.j] = block_text
            # go_recursive = True
            break
        elif (next_block_index.i == exit.i and next_block_index.j == exit.j):
            maze_path_param[current_block_index.i][current_block_index.j] = path_id_param
            maze_path_text_param[current_block_index.i][current_block_index.j] = block_text
            # we come to the end, update the next block path_id too as it's used to determine if the text gets drawn
            maze_path_param[next_block_index.i][next_block_index.j] = path_id_param
            # no need to update the next block text, keep it as 'X', it will be drawn as we have set the path_id
            update_to_draw_for_current_and_next_block(current_block_index, next_block_index, maze_param)
            if current_block_index not in path_index_list:
                path_index_list.append(current_block_index)
            break
        else:
            maze_path_param[current_block_index.i][current_block_index.j] = path_id_param
            maze_path_text_param[current_block_index.i][current_block_index.j] = block_text
            # search continue, no need to update path_id for next block as it will become current block
            update_to_draw_for_current_and_next_block(current_block_index, next_block_index, maze_param)
            if current_block_index not in path_index_list:
                path_index_list.append(current_block_index)
        current_block_index = Block_Index(next_block_index.i, next_block_index.j)

    # if len(path_index_list) == 0:
    #     return None, maze_param, maze_path_param, maze_path_text_param

    # Now we can loop through the path_index_list and get the neighbor properties
    path_block_index_neighborpaths_pairs = list()
    for index in path_index_list:
        block_neighborpaths = get_block_neighbor_paths(index, maze_path_param)
        path_block_index_neighborpaths_pairs.append(Block_Index_NeighborPaths_Pair(
            index, block_neighborpaths))
    print('created path {}, path_block_index_neighborpaths_pairs={}'.format(
        path_id_param, path_block_index_neighborpaths_pairs))
    return path_block_index_neighborpaths_pairs, maze_param, maze_path_param, maze_path_text_param


def get_block_neighbor_paths(current_block_index_param, maze_path_param):
    if print_func_name:
        print('function: {}'.format(sys._getframe().f_code.co_name))

    t_p = 0
    b_p = 0
    l_p = 0
    r_p = 0
    if current_block_index_param.i == 0:
        t_p = -1
    else:
        t_p = maze_path_param[current_block_index_param.i-1][current_block_index_param.j]
    if current_block_index_param.i == total_rows - 1:
        b_p = -1
    else:
        b_p = maze_path_param[current_block_index_param.i+1][current_block_index_param.j]
    if current_block_index_param.j == 0:
        l_p = -1
    else:
        l_p = maze_path_param[current_block_index_param.i][current_block_index_param.j-1]
    if current_block_index_param.j == total_cols - 1:
        r_p = -1
    else:
        r_p = maze_path_param[current_block_index_param.i][current_block_index_param.j+1]

    return Block_NeighborPaths(t_p, b_p, l_p, r_p)


def get_block_text(move_direction):
    if print_func_name:
        print('function: {}'.format(sys._getframe().f_code.co_name))

    block_text = 'X'
    if move_direction == 'L':
        block_text = '<'
    elif move_direction == 'R':
        block_text = '>'
    elif move_direction == 'U':
        block_text = '^'
    elif move_direction == 'D':
        block_text = 'V'
    return block_text


def get_move_direction(current_block_index_param: Block_Index, path_id_param, special_rules_for_path_param,
                       maze_param, maze_path_param):
    if print_func_name:
        print('function: {}'.format(sys._getframe().f_code.co_name))

    # Note, for first path, i.e. path 1 (0 value in maze_path for a block refer to the block is not in any path,
    # to be consistent, path ID starting from 1),
    # todo: as we are setting out the maze, we can have rule that for path 1, only move down and right, 
    #  question is, can we ensure all blocks are linked to the entrance if we do this?
    possible_moves = list()
    if path_id_param == 1 and special_rule_for_path1:
        if (current_block_index_param.i+1 < total_rows and
                # the block down is not assigned to any path, add 'D'
                maze_path_param[current_block_index_param.i+1][current_block_index_param.j] == 0):
            possible_moves.append('D')
        if (current_block_index_param.j+1 < total_cols and
                # the block to the right is not assigned to any path, add 'R'
                maze_path_param[current_block_index_param.i][current_block_index_param.j+1] == 0):
            possible_moves.append('R')
    else:
        if (current_block_index_param.i-1 >= 0 and
                # the block down is not assigned to any path, and it only has two not_to_draw borders, add 'U'
                maze_path_param[current_block_index_param.i-1][current_block_index_param.j] == 0 and
                'U' in special_rules_for_path_param):
                possible_moves.append('U')
        if (current_block_index_param.i+1 < total_rows and
                # the block down is not assigned to any path, and it only has two not_to_draw borders, add 'D'
                maze_path_param[current_block_index_param.i+1][current_block_index_param.j] == 0 and
                'D' in special_rules_for_path_param):
                possible_moves.append('D')
        if (current_block_index_param.j-1 >= 0 and
                # the block to the right is not assigned to any path, and it only has two not_to_draw borders, add 'L'
                maze_path_param[current_block_index_param.i][current_block_index_param.j-1] == 0 and
                'L' in special_rules_for_path_param):
                possible_moves.append('L')
        if (current_block_index_param.j+1 < total_cols and
                # the block to the right is not assigned to any path, and it only has two not_to_draw borders, add 'R'
                maze_path_param[current_block_index_param.i][current_block_index_param.j+1] == 0 and
                'R' in special_rules_for_path_param):
                possible_moves.append('R')
    print('possible_moves={}'.format(possible_moves))

    # randomly choose a move direction from the possible moves list
    move = 'N/A'
    if (len(possible_moves) > 1):
        move = get_randomized_value_from_possible_values(possible_moves)
    elif len(possible_moves) == 1:
        move = possible_moves[0]

    return move


def get_randomized_value_from_possible_values(possible_values_param):
    if print_func_name:
        print('function: {}'.format(sys._getframe().f_code.co_name))

    # print('possible_moves={}'.format(possible_moves))
    random_array_range = 50
    total_possible_values = len(possible_values_param)
    # print('total_possible_moves={}'.format(total_possible_moves))
    interval = int(random_array_range/total_possible_values)
    intervals = list()
    # print('interval={}'.format(interval))
    for i in range(total_possible_values):
        start = int(i*interval)
        end = int((i+1)*interval)
        intervals.append((start,end))
    # print('intervals={}'.format(intervals))
    list_to_randomise = list(range(1, random_array_range))
    # print('list_to_randomise={}'.format(list_to_randomise))
    randomised_value = random.choice(list_to_randomise)
    print('randomised_value={}'.format(randomised_value))
    ret_value = None
    for i in range(total_possible_values):
        current_interval = list(intervals[i])
        print('i={}, current_interval={}'.format(i, current_interval))
        start = current_interval[0]
        end = current_interval[1]
        # the following is to avoid the situation that randomised_value = 49, and last interval is [36, 48]
        if i == total_possible_values-1:
            end = random_array_range-1
        if start <= randomised_value and randomised_value <= end:
            ret_value = possible_values_param[i]
            break
    return ret_value


def get_next_block_index(current_block_index_param, move_direction_param):
    if print_func_name:
        print('function: {}'.format(sys._getframe().f_code.co_name))

    # get next block index
    next_block_index = None
    if move_direction_param == 'L':
        next_block_index = Block_Index(current_block_index_param.i, current_block_index_param.j-1)
    elif move_direction_param == 'R':
        next_block_index = Block_Index(current_block_index_param.i, current_block_index_param.j+1)
    elif move_direction_param == 'U':
        next_block_index = Block_Index(current_block_index_param.i-1, current_block_index_param.j)
    elif move_direction_param == 'D':
        next_block_index = Block_Index(current_block_index_param.i+1, current_block_index_param.j)
    else:   # move == 'N/A'
        next_block_index = Block_Index(current_block_index_param.i, current_block_index_param.j)
    
    return next_block_index


def update_to_draw_for_current_and_next_block(current_block_index_param, next_block_index_param, maze_param):
    if print_func_name:
        print('function: {}'.format(sys._getframe().f_code.co_name))

    # initialise to_draw for current and next block
    current_block_t_to_draw = maze_param[current_block_index_param.i][current_block_index_param.j].t.to_draw
    current_block_b_to_draw = maze_param[current_block_index_param.i][current_block_index_param.j].b.to_draw
    current_block_l_to_draw = maze_param[current_block_index_param.i][current_block_index_param.j].l.to_draw
    current_block_r_to_draw = maze_param[current_block_index_param.i][current_block_index_param.j].r.to_draw
    next_block_t_to_draw = maze_param[next_block_index_param.i][next_block_index_param.j].t.to_draw
    next_block_b_to_draw = maze_param[next_block_index_param.i][next_block_index_param.j].b.to_draw
    next_block_l_to_draw = maze_param[next_block_index_param.i][next_block_index_param.j].l.to_draw
    next_block_r_to_draw = maze_param[next_block_index_param.i][next_block_index_param.j].r.to_draw

    move_direction = ''
    if current_block_index_param.i == next_block_index_param.i and \
            current_block_index_param.j > next_block_index_param.j:
        current_block_l_to_draw = 0     # moving left, left border of the current block set not to draw
        next_block_r_to_draw = 0        # moving left, right border of the next block set not to draw
    elif current_block_index_param.i == next_block_index_param.i and \
            current_block_index_param.j < next_block_index_param.j:
        current_block_r_to_draw = 0     # moving right, right border of the current block set not to draw
        next_block_l_to_draw = 0        # moving right, left border to the next block set not to draw
    elif current_block_index_param.i > next_block_index_param.i and \
            current_block_index_param.j == next_block_index_param.j:
        current_block_t_to_draw = 0     # moving up, top border of the current block set not to draw
        next_block_b_to_draw = 0        # moving up, bottom border to the next block set not to draw
    elif current_block_index_param.i < next_block_index_param.i and \
            current_block_index_param.j == next_block_index_param.j:
        current_block_b_to_draw = 0     # moving down, bottom border of the current block set not to draw
        next_block_t_to_draw = 0        # moving down, top corder of the next block set not to draw

    # # todo, the following clause of code need refacturing, because if we know the current index and the next index
    # #  we do not need to know move_direction_param
    #
    # set current and next block
    maze[current_block_index_param.i][current_block_index_param.j] = Single_Block_With_Four_Borders(
        Single_BlockBorder(maze[current_block_index_param.i][current_block_index_param.j].t.x_b,
                           maze[current_block_index_param.i][current_block_index_param.j].t.y_b,
                           maze[current_block_index_param.i][current_block_index_param.j].t.x_e,
                           maze[current_block_index_param.i][current_block_index_param.j].t.y_e,
                           current_block_t_to_draw),
        Single_BlockBorder(maze[current_block_index_param.i][current_block_index_param.j].b.x_b,
                           maze[current_block_index_param.i][current_block_index_param.j].b.y_b,
                           maze[current_block_index_param.i][current_block_index_param.j].b.x_e,
                           maze[current_block_index_param.i][current_block_index_param.j].b.y_e,
                           current_block_b_to_draw),
        Single_BlockBorder(maze[current_block_index_param.i][current_block_index_param.j].l.x_b,
                           maze[current_block_index_param.i][current_block_index_param.j].l.y_b,
                           maze[current_block_index_param.i][current_block_index_param.j].l.x_e,
                           maze[current_block_index_param.i][current_block_index_param.j].l.y_e,
                           current_block_l_to_draw),
        Single_BlockBorder(maze[current_block_index_param.i][current_block_index_param.j].r.x_b,
                           maze[current_block_index_param.i][current_block_index_param.j].r.y_b,
                           maze[current_block_index_param.i][current_block_index_param.j].r.x_e,
                           maze[current_block_index_param.i][current_block_index_param.j].r.y_e,
                           current_block_r_to_draw))
    maze[next_block_index_param.i][next_block_index_param.j] = Single_Block_With_Four_Borders(
        Single_BlockBorder(maze[next_block_index_param.i][next_block_index_param.j].t.x_b,
                           maze[next_block_index_param.i][next_block_index_param.j].t.y_b,
                           maze[next_block_index_param.i][next_block_index_param.j].t.x_e,
                           maze[next_block_index_param.i][next_block_index_param.j].t.y_e,
                           next_block_t_to_draw),
        Single_BlockBorder(maze[next_block_index_param.i][next_block_index_param.j].b.x_b,
                           maze[next_block_index_param.i][next_block_index_param.j].b.y_b,
                           maze[next_block_index_param.i][next_block_index_param.j].b.x_e,
                           maze[next_block_index_param.i][next_block_index_param.j].b.y_e,
                           next_block_b_to_draw),
        Single_BlockBorder(maze[next_block_index_param.i][next_block_index_param.j].l.x_b,
                           maze[next_block_index_param.i][next_block_index_param.j].l.y_b,
                           maze[next_block_index_param.i][next_block_index_param.j].l.x_e,
                           maze[next_block_index_param.i][next_block_index_param.j].l.y_e,
                           next_block_l_to_draw),
        Single_BlockBorder(maze[next_block_index_param.i][next_block_index_param.j].r.x_b,
                           maze[next_block_index_param.i][next_block_index_param.j].r.y_b,
                           maze[next_block_index_param.i][next_block_index_param.j].r.x_e,
                           maze[next_block_index_param.i][next_block_index_param.j].r.y_e,
                           next_block_r_to_draw))


def get_next_start_block(created_paths_param: dict, current_path_id_param, prioritise_current_path_param,
                         maze_param, maze_path_param):
    if print_func_name:
        print('function: {}'.format(sys._getframe().f_code.co_name))

    global total_rows
    global total_cols
    not_spanoff_pairs = list()

    # if prioritise_current_path_param:
    #     block_index_neighborpaths_pairs = created_paths_param[current_path_id_param]
    #     not_spanoff_pairs = get_not_spanoff_pair(block_index_neighborpaths_pairs)

    if len(not_spanoff_pairs) == 0:
        for k, v in created_paths_param.items():
            not_spanoff_pairs = get_not_spanoff_pair(v)
            if len(not_spanoff_pairs) > 0:
                break

    # pick a block on the path to span off if available, otherwise, pick another block in the field
    candidate_spanoff_block_index = None
    new_start = None
    if len(not_spanoff_pairs) > 0:
        list_to_randomise = list(range(len(not_spanoff_pairs)))
        candidate_pair = not_spanoff_pairs[random.choice(list_to_randomise)]
        candidate_spanoff_block_index = Block_Index(candidate_pair.block_index.i, candidate_pair.block_index.j)
        new_start = get_randomized_new_start_index(candidate_pair)
        print('just calculated start index for the next path, start index = {}, about to break'.format(new_start))

    # didn't find a new start from existing paths, randomly pick one that hasn't been asigned
    if new_start == None:
        not_asigned_block_list = list()
        # exhausted the blocks on all paths, and all span off, randomly pick one from blocks that
        # haven't been asgined to a path yet
        found = False
        for i in range(total_rows):
            for j in range(total_cols):
                if maze_path_param[i][j] == 0:
                    not_asigned_block_list.append(Block_Index(i, j))
        print('not_asigned_block_list={}'.format(not_asigned_block_list))
        block_index_list_to_randomise = list(range(len(not_asigned_block_list)))
        print('block_index_list_to_randomise={}'.format(block_index_list_to_randomise))
        new_start = not_asigned_block_list[random.choice(block_index_list_to_randomise)]
        print('new_start={}'.format(new_start))

        # check the four nrighbor to see if they aveh been asigned to a path
        possible_borders_to_open = list()
        if new_start.i-1 >= 0 and \
            maze_path_param[new_start.i-1][new_start.j] > 0 and \
            maze_param[new_start.i-1][new_start.j].b.to_draw == 1 and \
            maze_param[new_start.i][new_start.j].t.to_draw == 1:
                possible_borders_to_open.append('t')
        elif new_start.i+1 < total_rows and \
            maze_path_param[new_start.i+1][new_start.j] > 0 and \
            maze_param[new_start.i+1][new_start.j].t.to_draw == 1 and \
            maze_param[new_start.i][new_start.j].b.to_draw == 1:
                possible_borders_to_open.append('b')
        elif new_start.j-1 >= 0 and \
            maze_path_param[new_start.i][new_start.j-1] > 0 and \
            maze_param[new_start.i][new_start.j-1].r.to_draw == 1 and \
            maze_param[new_start.i][new_start.j].l.to_draw == 1:
                possible_borders_to_open.append('l')
        elif new_start.j+1 < total_cols and \
            maze_path_param[new_start.i][new_start.j+1] > 0 and \
            maze_param[new_start.i][new_start.j+1].l.to_draw == 1 and \
            maze_param[new_start.i][new_start.j].r.to_draw == 1:
                possible_borders_to_open.append('r')

        # if all four neighbors are assigned to a apth, no need to start a walk, just open a border
        if len(possible_borders_to_open) == 4:
            border_to_open = get_randomized_value_from_possible_values(possible_borders_to_open)
            maze_param, maze_path_param = update_border(new_start, border_to_open, maze_param, maze_path_param)
            # done, no need to carry on the current walk
            return None, None, maze_param, maze_path_param

    # return the candidate_spanoff_block_index from which the new_start span off because we would want
    # the border between the two blocks set not to draw,
    # note, if we randomly pick one that is not in a path, NO need to check if any neighbor of the freshely
    # picked one is included in a path, because in the code above, we first exhaust all the blocks on any path
    # before randomly picking one
    return new_start, candidate_spanoff_block_index, maze_param, maze_path_param


def update_border(new_start_param, border_to_open_param, maze_param, maze_path_param):
    if border_to_open_param == 't':
        maze_param[new_start_param.i][new_start_param.j].t.to_draw = 0
        maze_param[new_start_param.i-1][new_start_param.j].b.to_draw = 0
        maze_path_param[new_start_param.i][new_start_param.j] = \
            maze_path_param[new_start_param.i - 1][new_start_param.j]
    elif border_to_open_param == 'b':
        maze_param[new_start_param.i][new_start_param.j].b.to_draw = 0
        maze_param[new_start_param.i+1][new_start_param.j].t.to_draw = 0
        maze_path_param[new_start_param.i][new_start_param.j] = \
            maze_path_param[new_start_param.i+1][new_start_param.j]
    elif border_to_open_param == 'l':
        maze_param[new_start_param.i][new_start_param.j].l.to_draw = 0
        maze_param[new_start_param.i][new_start_param.j-1].r.to_draw = 0
        maze_path_param[new_start_param.i][new_start_param.j] = \
            maze_path_param[new_start_param.i][new_start_param.j-1]
    elif border_to_open_param == 'r':
        maze_param[new_start_param.i][new_start_param.j].r.to_draw = 0
        maze_param[new_start_param.i][new_start_param.j+1].l.to_draw = 0
        maze_path_param[new_start_param.i][new_start_param.j] = \
            maze_path_param[new_start_param.i][new_start_param.j+1]
    return maze_param, maze_path_param


def get_not_spanoff_pair(block_index_neighborpaths_pairs_param):
    if print_func_name:
        print('function: {}'.format(sys._getframe().f_code.co_name))

    not_span_off_pairs = list()
    for pair in block_index_neighborpaths_pairs_param:
        if pair.block_neighborpaths.t_p == 0 or \
                pair.block_neighborpaths.b_p == 0 or \
                pair.block_neighborpaths.l_p == 0 or \
                pair.block_neighborpaths.r_p == 0:
            not_span_off_pairs.append(pair)

    return not_span_off_pairs


def get_randomized_new_start_index(candidate_pair_param: Block_Index_NeighborPaths_Pair):
    if print_func_name:
        print('function: {}'.format(sys._getframe().f_code.co_name))

    possible_moves = list()

    # note if the neighbor path value == -1, edge block
    if candidate_pair_param.block_neighborpaths.t_p == 0:
        possible_moves.append('U')
    if candidate_pair_param.block_neighborpaths.b_p == 0:
        possible_moves.append('D')
    if candidate_pair_param.block_neighborpaths.l_p == 0:
        possible_moves.append('L')
    if candidate_pair_param.block_neighborpaths.r_p == 0:
        possible_moves.append('R')

    # randomly choose a move direction from the possible moves list
    move = None
    if (len(possible_moves) > 1):
        move = get_randomized_value_from_possible_values(possible_moves)
    elif len(possible_moves) == 1:
        move = possible_moves[0]

    new_start = None
    if move:
        if move == 'U':
            new_start = Block_Index(candidate_pair_param.block_index.i-1, candidate_pair_param.block_index.j)
        elif move == 'D':
            new_start = Block_Index(candidate_pair_param.block_index.i+1, candidate_pair_param.block_index.j)
        elif move == 'L':
            new_start = Block_Index(candidate_pair_param.block_index.i, candidate_pair_param.block_index.j-1)
        elif move == 'R':
            new_start = Block_Index(candidate_pair_param.block_index.i, candidate_pair_param.block_index.j+1)

    return new_start


def init_tkinter(root_geometry_str_param, root_width_param, root_height_param):
    if print_func_name:
        print('function: {}'.format(sys._getframe().f_code.co_name))

    root = Tk()
    root.geometry(root_geometry_str_param)

    frame = Frame(root, width=root_width_param, height=root_height_param, background="bisque")
    frame.pack(fill=None, expand=True)
    # the following example line doesn't seem to take any effect?
    # frame.place(relx=.5, rely=.5, anchor="c")

    canvas = Canvas(frame, width=root_width_param, height=root_height_param)
    canvas.pack()

    return root, frame, canvas


def main():
    # set globally randomize always generate same results
    if create_same_randomised_array:
        random.seed(1)

    root, frame, canvas = init_tkinter(root_geometry_str, root_width, root_height)
    global maze
    global maze_path
    global maze_path_text

    reset_maze_properties(maze, w)
    reset_maxe_path_and_maze_path_text(maze_path, maze_path_text)

    # set_maze_to_draw_random(maze)
    to_creat_path_id = 1
    prev_path_id = 1
    created_paths = dict()
    blocks_in_path_percentage = 0.0
    created_path_block_index_neighborpaths_pairs, maze, maze_path, maze_path_text = \
        create_path(entrance, to_creat_path_id, special_rules_for_path, maze, maze_path, maze_path_text)
    # if created_path_block_index_neighborpaths_pairs:
    created_paths[to_creat_path_id] = created_path_block_index_neighborpaths_pairs
    blocks_in_path_percentage = get_blocks_in_path_percentage(maze_path)
    print('Just created the first path, \nblocks_in_path_percentage = {}'.format(blocks_in_path_percentage))
    while blocks_in_path_percentage < block_in_path_percentage_threshold:
        # Note, get_next_start_block cralwing through all the generated paths
        # randomly pick a block that has NOT been span off to form a new path,
        # and use it as the new starting block for a new path, and when all of
        # those blocks are exhausted, then randomly chose one that has not been
        # asignned to a path, also check if all its neighobr blocks have a path_id
        # do not start a new path, just simply randomly? choose a border to open
        new_start, current_spanoff_block_index, maze, maze_path = get_next_start_block(
            created_paths, prev_path_id, global_prioritise_current_path, maze, maze_path)
        if new_start:
            to_creat_path_id += 1
            print('just before creating the next path, new_start index = {}, to_creat_path_id={}'.format(
                new_start, to_creat_path_id))
            created_path_block_index_neighborpaths_pairs, maze, maze_path, maze_path_text = \
                create_path(new_start, to_creat_path_id, special_rules_for_path, maze, maze_path, maze_path_text)
            # if created_path_block_index_neighborpaths_pairs:
            created_paths[to_creat_path_id] = created_path_block_index_neighborpaths_pairs
            blocks_in_path_percentage = get_blocks_in_path_percentage(maze_path)
            print('blocks_in_path_percentage={}'.format(blocks_in_path_percentage))
            prev_path_id = to_creat_path_id
            # note, we have successfully span off a path, not connecting the two paths by removing the border
            # between the new_start block and the block that it has been span off from
            if current_spanoff_block_index:
                update_to_draw_for_current_and_next_block(current_spanoff_block_index, new_start, maze)
        # else:
        #     print('Bah, cannot find the next starting point, give up....')

    if draw_block:
        print('maze_path_text={}'.format(maze_path_text))
        draw_maze_use_block(canvas, maze, maze_path, maze_path_text, text_shift)
    else:
        line_container = get_lines(maze)
        draw_maze_use_line(canvas, line_container)

    root.mainloop()


if __name__ == '__main__':
    main()
