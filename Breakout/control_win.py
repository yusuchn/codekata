# !/usr/bin/env python

'''
https://stackoverflow.com/questions/4688855/whats-the-difference-between-streams-and-datagrams-in-network-programming

QUOTE:
A long time ago I read a great analogy for explaining the difference between the two.
I don't remember where I read it so unfortunately I can't credit the author for the idea,
but I've also added a lot of my own knowledge to the core analogy anyway. So here goes:

A stream socket is like a phone call -- one side places the call, the other answers,
you say hello to each other (SYN/ACK in TCP), and then you exchange information.
Once you are done, you say goodbye (FIN/ACK in TCP). If one side doesn't hear a goodbye,
they will usually call the other back since this is an unexpected event;
usually the client will reconnect to the server.
There is a guarantee that data will not arrive in a different order than you sent it,
and there is a reasonable guarantee that data will not be damaged.

A datagram socket is like passing a note in class.
Consider the case where you are not directly next to the person you are passing the note to;
the note will travel from person to person. It may not reach its destination,
and it may be modified by the time it gets there. If you pass two notes to the same person,
they may arrive in an order you didn't intend, since the route the notes take through the classroom may not be the same,
one person might not pass a note as fast as another, etc.

So you use a stream socket when having information in order and intact is important.
File transfer protocols are a good example here. You don't want to download some file with its contents randomly
shuffled around and damaged!

You'd use a datagram socket when order is less important than timely delivery (think VoIP or game protocols),
when you don't want the higher overhead of a stream (this is why DNS is primarily a datagram protocol,
so that servers can respond to many, many requests at once very quickly), or when you don't care too much
if the data ever reaches its destination.

To expand on the VoIP/game case, such protocols include their own data-ordering mechanism.
But if one packet is damaged or lost, you don't want to wait on the stream protocol (usually TCP)
to issue a re-send request -- you need to recover quickly. TCP can take up to some number of minutes to recover,
and for realtime protocols like gaming or VoIP even three seconds may be unacceptable!
Using a datagram protocol like UDP allows the software to recover from such an event extremely quickly,
by simply ignoring the lost data or re-requesting it sooner than TCP would.

VoIP is a good candidate for simply ignoring the lost data -- one party would just hear a short gap,
similar to what happens when talking to someone on a cell phone when they have poor reception.
Gaming protocols are often a little more complex, but the actions taken will usually be to either ignore
the missing data (if subsequently-received data supercedes the data that was lost), re-request the missing data,
or request a complete state update to ensure that the client's state is in sync with the server's.
'''

import socket
import socketserver
from PIL import Image, ImageDraw, ImageFont, ImageColor
import pygame

import os
import io
# import imageio
import sys

import tkinter
import matplotlib
from generaltools import display_all_images_in_plot, matplot_display_setup, get_rgb_list
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
# For implementing the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import numpy as np
import time

import copy
from collections import namedtuple


def scan_line_for_objects(rgb_list_param, line_index_to_scan_param, image_scan_direction_param,
                          object_colour, background_colour):
    object_positions = list()
    rgb_h = len(rgb_list_param)
    rgb_w = len(rgb_list_param[0])
    # note, the rgb_list is also flopped as it directly from pix, but,
    # scan_direction_param here references to image direction not rgb_list
    scan_range = 0
    if image_scan_direction_param == 'v':
        scan_range = rgb_w
    elif image_scan_direction_param == 'h':
        scan_range = rgb_h
    # scan through the line, column or row
    search_object = ''
    if object_colour == (255, 0, 0):
        search_object = 'bricks'
    elif object_colour == (0, 255, 0):
        search_object = 'ball'
    elif object_colour == (0, 0, 255):
        search_object = 'bat'
    print('scan_line_for_objects searching for {}, line_index_to_scan_param={}, \n'
          'image_scan_direction_param={}, \n'
          'object_colour={}, \n'
          'background_colour={}, \n'
          'scan_range={}'.format(search_object, line_index_to_scan_param, image_scan_direction_param,
                                 object_colour, background_colour, scan_range))
    object_position = dict()
    for i in range(scan_range):
        # note, rgb_list is flopped
        rgb_row_index = 0
        rgb_col_index = 0
        if image_scan_direction_param == 'v':  # referencing scan in image vertical direction
            rgb_row_index = line_index_to_scan_param
            rgb_col_index = i
        elif image_scan_direction_param == 'h':  # referencing scan in image horizontal direction
            rgb_row_index = i
            rgb_col_index = line_index_to_scan_param
        if object_colour == (255, 0, 0):
            print('rgb_list_param[{}][{}]={}'.format(rgb_row_index, rgb_col_index,
                rgb_list_param[rgb_row_index][rgb_col_index]))
        if rgb_list_param[rgb_row_index][rgb_col_index] == object_colour:  # (255, 0, 0):
            if object_colour == (255, 0, 0):
                print("Colour match")
            if len(object_position) == 0:
                object_position['start'] = i
        elif rgb_list_param[rgb_row_index][rgb_col_index] == background_colour:  #(255, 255, 255):
            if len(object_position) == 1:
                object_position['end'] = i - 1
                # the following needs to be tested out as we may be able to get away by not copying
                object_position_copy = copy.deepcopy(object_position)
                print('object_position={}, object_position_copy={}\n'.format(object_position, object_position_copy))
                object_positions.append(object_position_copy)
                object_position.clear()
    return object_positions

# NOTE, only use get_bricks_positions once when game started,
# update brick_states to mark which brick is knocked out if needed
def get_bricks_positions(im_param):
    im_w = im_param.size[0]
    im_h = im_param.size[1]
    print('get_bricks_positions - im_h={}, im_w={}'.format(im_h, im_w))
    rgb_list, pix = get_rgb_list(im_param)

    # Note, the original image has 10 brick width in a row, the middle is a gap, and,
    # the ball originally sits right below the bricks, just slightly off the center
    # this can be explored to identify horizontal position of each brick, horizontal
    # padding, as well as the ball size, use the same col_to_scan for bricks and ball
    # note, rgb_list is also flopped as it's directly from pix
    col_to_scan = int(im_w / 2) - 10
    # print('get_bricks_positions - col_to_scan={}, \nrgb_list={}'.format(col_to_scan, rgb_list[0]))
    print('get_bricks_positions - col_to_scan={}'.format(col_to_scan))
    brick_vertical_positions = scan_line_for_objects(rgb_list, col_to_scan, 'v', (255, 0, 0), (255, 255, 255))
    print('get_bricks_positions - brick_vertical_positions=\n{}'.format(brick_vertical_positions))

    row_to_scan = brick_vertical_positions[0]['start'] + \
                  int((brick_vertical_positions[0]['end'] - brick_vertical_positions[0]['start'])/2)
    # print('get_bricks_positions - row_to_scan={}, \nrgb_list={}'.format(row_to_scan, rgb_list[0]))
    print('get_bricks_positions - row_to_scan={}'.format(row_to_scan))
    brick_horizontal_positions = scan_line_for_objects(rgb_list, row_to_scan, 'h', (255, 0, 0), (255, 255, 255))
    print('get_bricks_positions - brick_horizontal_positions=\n{}'.format(brick_horizontal_positions))
    if len(brick_horizontal_positions) > 0 and len(brick_vertical_positions) > 0:
        return True, brick_horizontal_positions, brick_vertical_positions
    else:
        return False, None, None

def get_brick_size_and_padding(brick_horizontal_positions, brick_vertical_positions):
    brick_w = brick_horizontal_positions[0]['end'] - brick_horizontal_positions[0]['start']
    brick_h = brick_vertical_positions[0]['end'] - brick_vertical_positions[0]['start']
    brick_x_pad = brick_horizontal_positions[1]['start'] - brick_horizontal_positions[0]['end']
    brick_y_pad = brick_vertical_positions[1]['start'] - brick_vertical_positions[0]['end']
    return brick_w, brick_h, brick_x_pad, brick_y_pad

# note, allocate_bricks sets the initial bracks, and the initial brick_states,
# bricks always has initial bricks layout, sets brick_states to reflect if a brick is knocked out
def get_bricks(im_param):
    success, brick_horizontal_positions, brick_vertical_positions = get_bricks_positions(im_param)
    if not success:
        return False, None, None
    brick_w, brick_h, brick_x_pad, brick_y_pad = \
        get_brick_size_and_padding(brick_horizontal_positions, brick_vertical_positions)
    bricks = [[pygame.Rect(0, 0, brick_w, brick_h)] *
              len(brick_horizontal_positions) for n in range(len(brick_vertical_positions))]
    brick_states = [[1] * len(brick_horizontal_positions) for n in range(len(brick_vertical_positions))]
    for i, vertical_pos in enumerate(brick_vertical_positions):
        for j, horizontal_pos in enumerate(brick_horizontal_positions):
            bricks[i][j] = pygame.Rect(horizontal_pos['start'], vertical_pos['start'], brick_w, brick_h)
            brick_states[i][j] = 1  # 1: available, 0: knocked out
    return True, bricks, brick_states

def update_brick_states(im_param, bricks, brick_states):
    rgb_list, pix = get_rgb_list(im_param)
    # note, rgb_list is also flopped as it's directly from pix
    states_changed = False
    state_changed_brick = None
    for i in range(len(bricks)):
        for j in range(len(bricks[0])):
            prev_state = brick_states[i][j]
            # only need to check the top-left pixel to see if the color changed i.e. if the brick is knocked out
            if rgb_list[bricks[i][j].y][bricks[i][j].x] != (255, 0, 0):
                brick_states[i][j] = 0
                if brick_states[i][j] != prev_state:
                    states_changed = True
                    state_changed_brick = bricks[i][j]
                    # note, only one brick gets knocked out at one time, so break
                    break
    return states_changed, brick_states, state_changed_brick

def reset_brick_states(brick_states):
    for i in range(len(brick_states)):
        for j in range(len(brick_states[0])):
            brick_states[i][j] = 1

def get_bat(im_param):
    im_w = im_param.size[0]
    im_h = im_param.size[1]
    print('get_bat - im_h={}, im_w={}'.format(im_h, im_w))
    rgb_list, pix = get_rgb_list(im_param)
    # bat is at the bottom of the image, with a small padding, ref. game.py
    row_to_scan = im_h - 10
    bat_horizontal_positions = scan_line_for_objects(rgb_list, row_to_scan, 'h', (0, 0, 255), (255, 255, 255))
    print('get_bat - row_to_scan={}, \nbat_horizontal_positions={}'.format(row_to_scan, bat_horizontal_positions))
    # chose a position within the first bat width as the column to scan,
    # this guarantee we won't hit a gap, note there is only one bat
    col_to_scan = bat_horizontal_positions[0]['start'] + 10
    bat_vertical_positions = scan_line_for_objects(rgb_list, col_to_scan, 'v', (0, 0, 255), (255, 255, 255))
    print('get_bat - col_to_scan={}, \nbat_vertical_positions={}'.format(col_to_scan, bat_vertical_positions))
    # note, there is only one bat, so we return bat position, note, position returned is top-left corner
    if len(bat_horizontal_positions) > 0 and len(bat_vertical_positions) > 0:
        bat_x = bat_horizontal_positions[0]['start']
        bat_y = bat_vertical_positions[0]['start']
        bat_w = bat_horizontal_positions[0]['end'] - bat_horizontal_positions[0]['start']
        bat_h = bat_vertical_positions[0]['end'] - bat_vertical_positions[0]['start']
        return True, pygame.Rect(bat_x, bat_y, bat_w, bat_h)
    else:
        return False, None

BallSquare = namedtuple('BallSquare', ['ball_left', 'ball_right', 'ball_top', 'ball_bottom'])
BallCenter = namedtuple('BallCenter', ['x', 'y'])


# as we only get the original ball center, so instead of randomly trying a col to scan,
# passing the bricks locations, knowing the ball original just a few pixel below, and start
# scan horizontally for the ball first instead of vertically
def get_original_ball_center_and_size(im_param, bricks):
    im_w = im_param.size[0]
    im_h = im_param.size[1]
    print('get_original_ball_center_and_size - im_h={}, im_w={}'.format(im_h, im_w))
    rgb_list, pix = get_rgb_list(im_param)

    total_brick_rows = len(bricks)
    brick_ref = bricks[total_brick_rows-1][0]

    # the original image shows that the ball originally is about a brick height below the last row of bricks,
    # use that knowledge to set the start row to scan for the ball
    ball_row_to_scan = brick_ref.y + brick_ref.h
    ball_horizontal_positions = scan_line_for_objects(rgb_list, ball_row_to_scan, 'h', (0, 255, 0), (255, 255, 255))
    print('get_original_ball_center_and_size - ball_row_to_scan = {}\nball_horizontal_positions = {}'.format(
        ball_row_to_scan, ball_horizontal_positions))
    while (len(ball_horizontal_positions) == 0 and ball_row_to_scan < im_h):
        ball_row_to_scan += 1
        ball_horizontal_positions = scan_line_for_objects(rgb_list, ball_row_to_scan, 'h', (0, 255, 0), (255, 255, 255))
        print('get_original_ball_center_and_size - ball_row_to_scan = {}\nball_horizontal_positions = {}'.format(
            ball_row_to_scan, ball_horizontal_positions))

    if len(ball_horizontal_positions) == 0:
        return False, None, None

    # ball_col_to_scan = int(im_w / 2)
    ball_col_to_scan = ball_horizontal_positions[0]['start'] + \
                       int((ball_horizontal_positions[0]['end']-ball_horizontal_positions[0]['start'])/2)
    ball_vertical_positions = scan_line_for_objects(rgb_list, ball_col_to_scan, 'v', (0, 255, 0), (255, 255, 255))
    print('get_original_ball_center_and_size - ball_col_to_scan = {}\nball_vertical_positions = {}'.format(
        ball_col_to_scan, ball_vertical_positions))

    # # there is only one ball, use the middle of the ball vertical positions to determin the row to scan
    # # to determine ball size
    # ball_row_to_scan = ball_vertical_positions[0]['start'] + \
    #                    int((ball_vertical_positions[0]['end'] - ball_vertical_positions[0]['start']) / 2)
    # ball_horizontal_positions = scan_line_for_objects(rgb_list, ball_row_to_scan, 'h', (0, 255, 0), (255, 255, 255))
    # print('get_original_ball_center_and_size - ball_row_to_scan = {}\nball_horizontal_positions = {}'.format(
    #     ball_row_to_scan, ball_horizontal_positions))

    # note, there is only one ball, position returned is the center of the ball
    if len(ball_horizontal_positions) > 0 and len(ball_vertical_positions) > 0:
        ball_r = int((ball_vertical_positions[0]['end'] - ball_vertical_positions[0]['start'])/2)
        ball_center_y = ball_vertical_positions[0]['start'] + ball_r
        ball_center_x = ball_horizontal_positions[0]['start'] +\
                        int((ball_horizontal_positions[0]['end']-ball_horizontal_positions[0]['start'])/2)
        return True, BallCenter(ball_center_x, ball_center_y), ball_r
    else:
        return False, None, None

BallRelativePositionToBrick = \
    namedtuple('BallRelativePositionToBrick', ['below_brick', 'above_brick', 'right_of_brick', 'left_of_brick'])

def get_relative_position_to_brick(ball_square, brick:pygame):
    below_brick = False
    above_brick = False
    right_of_brick = False
    left_of_brick = False
    # bounced_from_bottom, bounced_from_top, bounced_from_right, and bounced_from_left
    # mark the edges the ball bounced off from, and, needed to draw the trajectory
    # following are straight forward bounced off regions
    if ball_square.ball_top > brick.y + brick.h:
        below_brick = True
    if ball_square.ball_bottom < brick.y:
        above_brick = True
    if ball_square.ball_left > brick.x + brick.w:
        right_of_brick = True
    if ball_square.ball_right < brick.x:
        left_of_brick = True
    return BallRelativePositionToBrick(below_brick, above_brick, right_of_brick, left_of_brick)


def get_ball_center_square(ball_x_min, ball_x_max, ball_y_min, ball_y_max, ball_r, search_area):
    # search_area refer when we find the ball, we are search below/left_to/right_to/above the knocked out brick
    if search_area == 'below':
        ball_center = BallCenter((ball_x_min+ball_x_max)/2, ball_y_max-ball_r)
    elif search_area == 'left':
        ball_center = BallCenter(ball_x_min+ball_r, (ball_y_min+ball_y_max)/2)
    elif search_area == 'right':
        ball_center = BallCenter(ball_x_max-ball_r, (ball_y_min+ball_y_max)/2)
    elif search_area == 'above':
        ball_center = BallCenter((ball_x_min+ball_x_max)/2, ball_y_min+ball_r)
    else:
        print('please specifiy the search area, valid values: below, left_to, right_to, above')
        return None, None
    ball_square = BallSquare(ball_center.x-ball_r, ball_center.x+ball_r,
                             ball_center.y-ball_r, ball_center.y+ball_r)
    return ball_center, ball_square

# image analysis to get the command, 'L', 'R', or '.', or maybe the positions
def get_predicted_position(curr_image, prev_image, bricks, brick_states):
    # for i in range(im_param.size[0]):
    #     for j in range(im_param.size[1]):
    brick_states_changed, brick_states, state_changed_brick = \
        update_brick_states(curr_image, bricks, brick_states)
    bat_success, bat_x, bat_y, bat_w, bat_h = get_bat(curr_image)

    return 'L'

def search_for_ball(search_area, search_margin, ball_r,
                    state_changed_brick: pygame.Rect, rgb_list, image_w, image_h):
    ball_x_min = 0  # state_changed_brick.x
    ball_x_max = 0  # state_changed_brick.x
    ball_y_min = 0  # state_changed_brick.y
    ball_y_max = 0  # state_changed_brick.y
    start_y = 0
    end_y = 0
    start_x = 0
    end_x = 0
    do_not_search = False
    if search_area == 'below':
        start_y = state_changed_brick.y + state_changed_brick.h
        end_y = state_changed_brick.y + state_changed_brick.h + search_margin
        start_x = state_changed_brick.x - search_margin
        end_x = state_changed_brick.x + state_changed_brick.w + search_margin
    elif search_area == 'right':
        start_y = state_changed_brick.y - search_margin
        end_y = state_changed_brick.y + state_changed_brick.h
        start_x = state_changed_brick.x + state_changed_brick.w
        end_x = state_changed_brick.x + state_changed_brick.w + search_margin
    elif search_area == 'left':
        start_y = state_changed_brick.y - search_margin
        end_y = state_changed_brick.y + state_changed_brick.h
        start_x = state_changed_brick.x - search_margin
        end_x = state_changed_brick.x
    elif search_area == 'above':
        start_y = state_changed_brick.y - search_margin
        end_y = state_changed_brick.y
        start_x = state_changed_brick.x
        end_x = state_changed_brick.x + state_changed_brick.w

    if start_y < 0 and end_y > 0:
        start_y = 0
    if start_y > image_h:
        do_not_search = True
    if end_y < 0:
        do_not_search = True
    if end_y > image_h:
        end_y = image_h

    if start_x < 0 and end_x > 0:
        start_x = 0
    if start_x > image_w:
        do_not_search = True
    if end_x < 0:
        do_not_search = True
    if end_x > image_w:
        end_x = image_w

    if do_not_search:
        return False, None, None

    for i in range(start_y, end_y):
        for j in range(start_x, end_x):
            if rgb_list[j][i] != (0, 255, 0):
                ball_x_min = min(i, ball_x_min)
                ball_x_max = max(i, ball_x_max)
                ball_y_min = min(j, ball_y_min)
                ball_y_max = max(j, ball_y_max)
    if ball_x_min != 0 or ball_x_max != 0 or ball_y_min != 0 or ball_y_max != 0:
        ball_center, ball_square = get_ball_center_square(ball_x_min, ball_x_max, ball_y_min, ball_y_max,
                                                          ball_r, search_area)
        return True, ball_center, ball_square
    else:
        return False, None, None


def get_command_message(curr_bat: pygame.Rect, predicted_ball_landing_position):
    if ((curr_bat.x < predicted_ball_landing_position) and
            (predicted_ball_landing_position < (curr_bat.x + curr_bat.w))):
        command_message = '.'
    elif ((curr_bat.x + curr_bat.w) < predicted_ball_landing_position):
        command_message = 'R'
    elif (predicted_ball_landing_position < curr_bat.x):
        command_message = 'L'


def get_predicted_ball_landing_position(curr_ball_relative_postion_to_brick: BallRelativePositionToBrick,
                                        prev_ball_relative_postion_to_brick: BallRelativePositionToBrick,
                                        curr_ball_center: BallCenter,
                                        prev_ball_center: BallCenter,
                                        curr_ball_square: BallSquare, curr_bat: pygame.Rect, image_w, image_h):
    # note, we only caluclate the trajectory if we detect any brick is knocked out,
    # prev_ball must have hit the brick and resulted in the curr_ball position, so,
    # valid to use curr_ball_relative_postion_to_brick and prev_ball_relative_postion_to_brick
    # to predict the landing position, in any case, like nsw method, always keep under the curr_ball
    predicted_ball_landing_x = curr_ball_center.x

    # both prev and curr ball position below the brick, bounced off the bottom
    if (curr_ball_relative_postion_to_brick.below_brick and
        prev_ball_relative_postion_to_brick.below_brick):
        if curr_ball_center.x < prev_ball_center.x:
            predicted_ball_landing_x = curr_ball_center.x-(curr_bat.y-curr_ball_square.ball_bottom)
            if predicted_ball_landing_x < 0:
                # TODO: need to consider if the predicted trajectory hit the left edge of the image
                #       and bounced off again, for now, keep under the ball
                predicted_ball_landing_x = curr_ball_center.x
        elif curr_ball_center.x > prev_ball_center.x:
            predicted_ball_landing_x = curr_ball_center.x+(curr_bat.y-curr_ball_square.ball_bottom)
            if predicted_ball_landing_x > image_w:
                # TODO: need to consider if the predicted trajectory hit the right edge of the image
                #       and bounced off again, for now, keep under the ball
                predicted_ball_landing_x = curr_ball_center.x
    # both prev and curr ball position above the brick, bounced off the top
    elif (curr_ball_relative_postion_to_brick.above_brick and
          prev_ball_relative_postion_to_brick.above_brick):
        # TODO: need to consider if the predicted trajectory hit any bricks or top edge of the image
        #       and bounced off again, for now, keep under the ball
        predicted_ball_landing_x = curr_ball_center.x
    # both prev and curr ball position right of the brick, bounced off the right edge
    elif (curr_ball_relative_postion_to_brick.right_of_brick and
          prev_ball_relative_postion_to_brick.right_of_brick):
        if curr_ball_center.y > prev_ball_center.y:
            predicted_ball_landing_x = curr_ball_center.x + (curr_bat.y - curr_ball_square.ball_bottom)
            if predicted_ball_landing_x > image_w:
                # TODO: need to consider if the predicted trajectory hit the right edge of the image
                #       and bounced off again, for now, keep under the ball
                predicted_ball_landing_x = curr_ball_center.x
        elif curr_ball_center.y < prev_ball_center.y:
            # TODO: need to consider if the predicted trajectory hit any brick or the right edge of the iamge,
            #       and bounced off again, for now, keep under the ball
            predicted_ball_landing_x = curr_ball_center.x
    # both prev and curr ball posiiton left of the brick, bounced off the left
    elif (curr_ball_relative_postion_to_brick.left_of_brick and
          prev_ball_relative_postion_to_brick.left_of_brick):
        if curr_ball_center.y > prev_ball_center.y:
            predicted_ball_landing_x = curr_ball_center.x - (curr_bat.y - curr_ball_square.ball_bottom)
            if predicted_ball_landing_x < 0:
                # TODO: need to consider if the predicted trajectory hit the left edge of the image
                #       and bounced off the image edge, for now, keep under the ball
                predicted_ball_landing_x = curr_ball_center.x
        elif curr_ball_center.y < prev_ball_center.y:
            # TODO: need to consider if the predicted trajectory hit any brick or the left edge of the iamge,
            #       and bounced off again, for now, keep under the ball
            predicted_ball_landing_x = curr_ball_center.x

    return predicted_ball_landing_x


def set_curr_to_prev(curr_ball_center, curr_ball_square, curr_bat, curr_image):
    return copy.deepcopy(curr_ball_center), \
           copy.deepcopy(curr_ball_square), \
           copy.deepcopy(curr_bat), \
           copy.deepcopy(curr_image)

def get_curr_ball_from_prev_ball(prev_ball_center, ball_r, search_margin, im_param):
    im_w = im_param.size[0]
    im_h = im_param.size[1]
    print('search_for_ball_around_prev_ball - im_h={}, im_w={}'.format(im_h, im_w))
    rgb_list, pix = get_rgb_list(im_param)
    # NOTE, rgb_list is flopped, so rgb_list col is the image row to scan
    for j in range(len(rgb_list[0])):
        scan_line_for_objects(rgb_list, j, 'h', (0, 255, 0), (255, 255, 255))
    return curr_ball_center


root, fig, plot_canvas, toolbar, button = matplot_display_setup(6, 3)
# root.withdraw()     # hide the little root window

def main():
    curr_image = None
    prev_image = None
    curr_image_title = 'current_frame'
    prev_image_title = 'previous_frame'
    image_count = 0
    image_w = None
    image_h = None
    bricks = None
    brick_states = None
    ball_r = None
    # note, this is an artificial number, small enough to reduce search space, but big enough to include the whole ball
    search_margin = 20
    curr_ball_center = None
    curr_ball_square = None
    prev_ball_center = None
    prev_ball_square = None
    curr_bat = None
    prev_bat = None

    while True:
        # for sending command asking for image to return using UDP portocol,
        # simply send, doesn't involve any handshake or received feedback
        # note, this port is more like communication between two computers,
        # not exactly server-client structure
        # UDP_IP = "10.44.121.45"
        # UDP_IP = "10.44.121.31"
        UDP_IP = "127.0.0.1"
        UDP_PORT = 46087
        command_sock = socket.socket(socket.AF_INET,  # Internet
                                     socket.SOCK_DGRAM)  # UDP
        # for receiving image from TCP, IP and the port to receive from is the same as UDP
        # TCP_IP = '10.44.121.45'
        # TCP_IP = '10.44.121.31'
        TCP_IP = '127.0.0.1'
        TCP_PORT = 46087
        BUFFER_SIZE = 1024
        image_sock = socket.socket(socket.AF_INET,  # Internet
                                   socket.SOCK_STREAM)  # TCP
        try:
            # construct and send game command to the server
            command_message = ''

            do_not_increment_image_count = False
            # get command_message to move the bat
            if image_count == 0:
                command_message = 'G'
            # game over, brick_stats already generated, but no image received, restart a game, reset brick_states
            elif not curr_image and brick_states:
                brick_states = reset_brick_states(brick_states)
                command_message = 'R'
            else:
                command_message = '.'   # to be updated by image analysis results
                ball_success = False
                # bricks_success = False
                # bat_success = False
                # got the first iamge back, need to retrieve the bricks layout, only need once for a game
                bat_success, curr_bat = get_bat(curr_image)
                curr_rgb_list = get_rgb_list(curr_image)

                if image_count == 1:
                    bricks_success, bricks, brick_states = get_bricks(curr_image)
                    ball_success, org_ball_center, ball_r = get_original_ball_center_and_size(curr_image, bricks)
                    if ball_success:
                        curr_ball_center = org_ball_center
                        curr_ball_square = BallSquare(curr_ball_center.x-ball_r, curr_ball_center.x-ball_r,
                                                      curr_ball_center.y-ball_r, curr_ball_center.y+ball_r)
                        image_w = curr_image.size[0]
                        image_h = curr_image.size[1]
                        prev_ball_center, prev_ball_square, pre_bat, prev_image = \
                            set_curr_to_prev(curr_ball_center, curr_ball_square, curr_bat, curr_image)
                    else:
                        # if the game has started and the ball has dropped to the floor when we started
                        # running the control window, reset the game
                        do_not_increment_image_count = True
                        command_message = 'R'
                ###########################################################################
                if command_message != 'R':
                    predicted_ball_landing_position = curr_bat.x
                    # image analysis to get the command, 'L', 'R', or '.'
                    brick_states_changed, brick_states, state_changed_brick = \
                        update_brick_states(curr_image, bricks, brick_states)
                    print('brick_states_changed={}, brick_states={}, state_changed_brick={}'.format(
                        brick_states_changed, brick_states, state_changed_brick
                    ))
                    if (brick_states_changed):
                        print('brick_states_changed = True, searching for ball with the following parameters:\n'
                              'search_margin={}, ball_r={}, state_changed_brick={}, \ncurr_rgb_list size=({}, {})\n'.format(
                            search_margin, ball_r, state_changed_brick, len(curr_rgb_list), len(curr_rgb_list[0])
                        ))
                        ball_success, curr_ball_center, curr_ball_square = \
                            search_for_ball('below', search_margin, ball_r, state_changed_brick,
                                            curr_rgb_list, image_w, image_h)
                        if not ball_success:
                            ball_success, curr_ball_center, curr_ball_square = \
                                search_for_ball('right', search_margin, ball_r, state_changed_brick,
                                                curr_rgb_list, image_w, image_h)
                        if not ball_success:
                            ball_success, curr_ball_center, curr_ball_square = \
                                search_for_ball('left', search_margin, ball_r, state_changed_brick,
                                                curr_rgb_list, image_w, image_h)
                        if not ball_success:
                            ball_success, curr_ball_center, curr_ball_square = \
                                search_for_ball('above', search_margin, ball_r, state_changed_brick,
                                                curr_rgb_list, image_w, image_h)
                        if ball_success:
                            # keep under the call by default
                            predicted_ball_landing_position = curr_ball_center.x
                            # if image_count > 1, i.e.we have an prev_image, update predicted_ball_landing_position
                            if image_count > 1:
                                curr_ball_relative_postion_to_brick = \
                                    get_relative_position_to_brick(curr_ball_square, state_changed_brick)
                                prev_ball_relative_postion_to_brick = \
                                    get_relative_position_to_brick(prev_ball_square, state_changed_brick)
                                predicted_ball_landing_position = \
                                    get_predicted_ball_landing_position(
                                        curr_ball_relative_postion_to_brick, prev_ball_relative_postion_to_brick,
                                        curr_ball_center, prev_ball_center, curr_ball_square, curr_bat, image_w, image_h)
                    else:  # if not brick knocked off, just follow the ball
                        curr_ball_center = get_curr_ball_from_prev_ball(prev_ball_center, ball_r, search_margin, curr_image)
                        predicted_ball_landing_position = curr_ball_center.x
                    command_message = get_command_message(curr_bat, predicted_ball_landing_position)
                    # done our calculations, set the curr's to prev's
                    prev_ball_center, prev_ball_square, pre_bat, prev_image = \
                        set_curr_to_prev(curr_ball_center, curr_ball_square, curr_bat, curr_image)
                    ###########################################################################
                    # curr_image = None

            if command_message != '':
                # send the command to the server
                message_bytes_obj = bytearray(command_message, 'utf-8')  # needed by sock.sendto
                command_sock.sendto(message_bytes_obj, (UDP_IP, UDP_PORT))

                # connect to the server to receive image
                image_sock.connect((TCP_IP, TCP_PORT))
                buffer = io.BytesIO()
                while True:
                    data = image_sock.recv(BUFFER_SIZE)
                    if not data:
                        break
                    buffer.write(data)
                curr_image = Image.open(buffer)

                rgb_list, pix = get_rgb_list(curr_image)
                print('current image size={}'.format(curr_image.size))
                if not do_not_increment_image_count:
                    image_count += 1
                print('do_not_increment_image_count = {}, image_count = {}'.format(
                    do_not_increment_image_count, image_count))

                pairs = dict()
                if curr_image:
                    pairs[curr_image_title] = curr_image
                    if not prev_image:
                        prev_image = copy.deepcopy(curr_image)
                        pairs[prev_image_title] = prev_image
                    display_all_images_in_plot(1, pairs, fig, plot_canvas)
                # time.sleep(0.1)
        except ConnectionRefusedError:
            print("Server not running. Waiting.")
            # time.sleep(0.5)
        # finally:
        #     image_sock.close()


if __name__ == '__main__':
    main()




