from generaltools import *
import pprint
import copy
from PIL import Image


score_dict = {'F': 10, 'W': 0, 'M': 100, "G": 1, "V": -1}
villege_letter = 'V'
villege_rgb = (54, 61, 0)
do_break = False


def load_from_image(map_jpag_filename):
    try:
        im = Image.open(map_jpag_filename)  # Can be many different formats, but, currently only working on jpg
        print('image size = {}'.format(im.size))  # Get the width and hight of the image for iterating over
        rgb_list, pix = get_rgb_list(im)
        # return im and pix for updating pixel values and saving modified image,
        # note, pix is a PixeAccess Class, and it doesn't has size attribute, so,
        # returning im for: 1. access the image size, 2. save any modification to the image
        return True, rgb_list, im, pix
    except:
        print("No image map file exists")
        return False, None, None, None


def get_rgb_list(im_param):
    pix = im_param.load()  # load pixel RGB value of the image
    rgb_list = [[(0, 0, 0)] * im_param.size[1] for n in range(im_param.size[0])]
    for i in range(im_param.size[0]):
        for j in range(im_param.size[1]):
            rgb_list[i][j] = pix[i, j]
    return rgb_list, pix  # return pix for updating pixel values


def load_from_text(map_txt_filename):
    try:
        lines = open(map_txt_filename)
        letter_list = get_letter_list(lines)
        return True, letter_list
    except:
        print("No text map file exists")
        return False, None


def get_letter_list(lines_param):
    letter_list = list()
    for i, line in enumerate(lines_param):
        line_letter_list = list()
        for j, letter in enumerate(line.strip()):
            line_letter_list.append(letter)
        letter_list.append(line_letter_list)
    return letter_list


def find_village(list_param, is_letter_list=True):
    global villege_letter  # villege_letter = 'V'
    global villege_rgb  # villege_rgb = (54, 61, 0):
    total_row = len(list_param)
    total_col = len(list_param[0])
    for i in range(total_row):
        for j in range(total_col):
            if( (is_letter_list and list_param[i][j] == villege_letter)
                or (not is_letter_list and list_param[i][j] == villege_rgb) ):
                return (i, j), total_row, total_col


def build_cost_list(letter_list_param):
    global score_dict  # score_dict = {'F': '10', 'W': 0, 'M': 100, "G": 1, "V": -1}
    total_row = len(letter_list_param)
    total_col = len(letter_list_param[0])
    cost_list = [[0] * total_col for n in range(total_row)]
    for i in range(total_row):
        for j in range(total_col):
            cost_list[i][j] = score_dict[letter_list_param[i][j]]
    return cost_list


def generate_wall_list(map_list_param):
    total_row = len(map_list_param)
    total_col = len(map_list_param[0])
    # original value = 0, no wall, grassland
    # update to 1 if wall
    # update to -1 if water
    wall_list = [[0] * total_col for n in range(total_row)]
    return wall_list


def find_starting_grass_contour(villege_pos_param, letter_list_param, wall_list_param):
    wall_list_param = find_starting_grass_contour_horizaontal(villege_pos_param, letter_list_param, wall_list_param)
    wall_list_param = find_starting_grass_contour_vertical(villege_pos_param, letter_list_param, wall_list_param)
    return wall_list_param


def find_starting_grass_contour_horizaontal(villege_pos_param, letter_list_param, wall_list_param):
    total_row = len(letter_list_param)
    total_col = len(letter_list_param[0])
    v_row_idx, v_col_idx = villege_pos_param
    for i in range(total_row):
        # note, we are not starting from the villege cell now, start_col_idx differs
        e_start_col_idx = v_col_idx
        w_start_col_idx = v_col_idx-1
        if i == v_row_idx:
            e_start_col_idx = v_col_idx + 1
        for j in range(e_start_col_idx, total_col, 1):
            wall_value, grass_on_left = get_wall_list_from_grassland_horizontal(i, j, letter_list_param)
            if wall_value == 0:
                continue
            update_wall_list_horizontal(wall_list_param, i, j, wall_value, grass_on_left)
            if do_break:
                break
        for j in range(w_start_col_idx, -1, -1):
            wall_value, grass_on_left = get_wall_list_from_grassland_horizontal(i, j, letter_list_param)
            if wall_value == 0:
                continue
            update_wall_list_horizontal(wall_list_param, i, j, wall_value, grass_on_left)
            if do_break:
                break
    return wall_list_param


def update_wall_list_horizontal(wall_list_param, current_pixel_row_index_param, current_pixel_col_index_param,
                     wall_value_param, grass_on_left_param):
    shift = 0
    if grass_on_left_param == True:
        shift = -1
    elif grass_on_left_param == False:
        shift = 1
    if wall_value_param == 1:
        wall_list_param[current_pixel_row_index_param][current_pixel_col_index_param + shift] = wall_value_param
    elif wall_value_param == -1:
        wall_list_param[current_pixel_row_index_param][current_pixel_col_index_param] = wall_value_param


def get_wall_list_from_grassland_horizontal(row_index_param, col_index_param, letter_list_param):
    if letter_list_param[row_index_param][col_index_param] == 'V':
        return 0, None
    elif letter_list_param[row_index_param][col_index_param] == 'W':
        return -1, None
    # only set wall if the cell is neighboring a grass cell
    elif letter_list_param[row_index_param][col_index_param] != 'G':
        is_grass_edge, grass_on_left = \
            pixel_is_grass_edge_horizontal(row_index_param, col_index_param, letter_list_param)
        if is_grass_edge:
            return 1, grass_on_left
    return 0, None


def pixel_is_grass_edge_horizontal(row_index_param, col_index_param, letter_list_param):
    total_row = len(letter_list_param)
    total_col = len(letter_list_param[0])
    if  (row_index_param+1>=total_row or row_index_param-1<0 or
        col_index_param+1>=total_col or col_index_param-1<0):
        return False, None
    if letter_list_param[row_index_param][col_index_param - 1] == 'G':
        return True, True   # second True = grass on left
    elif letter_list_param[row_index_param][col_index_param + 1] == 'G':
        return True, False  # second False = grass on left
    else:
        return False, None


def find_starting_grass_contour_vertical(villege_pos_param, letter_list_param, wall_list_param):
    total_row = len(letter_list_param)
    total_col = len(letter_list_param[0])
    v_row_idx, v_col_idx = villege_pos_param
    for j in range (total_col):
        # note, we are not starting from the villege cell now, start_col_idx differs
        s_start_row_idx = v_row_idx
        # s_start_row_idx = v_row_idx+1
        n_start_row_idx = v_row_idx-1
        if j == v_col_idx:
            s_start_row_idx = v_row_idx + 1
        for i in range(s_start_row_idx, total_row, 1):
            wall_value, grass_on_top = get_wall_list_from_grassland_vertical(i, j, letter_list_param)
            if wall_value == 0:
                continue
            update_wall_list_vertical(wall_list_param, i, j, wall_value, grass_on_top)
            if do_break:
                break
        for i in range(n_start_row_idx, -1, -1):
            wall_value, grass_on_top = get_wall_list_from_grassland_vertical(i, j, letter_list_param)
            if wall_value == 0:
                continue
            update_wall_list_vertical(wall_list_param, i, j, wall_value, grass_on_top)
            if do_break:
                break
    return wall_list_param


def update_wall_list_vertical(wall_list_param, current_pixel_row_index_param, current_pixel_col_index_param,
                     wall_value_param, grass_on_top_param):
    shift = 0
    if grass_on_top_param == True:
        shift = -1
    elif grass_on_top_param == False:
        shift = 1
    if wall_value_param == 1:
        wall_list_param[current_pixel_row_index_param + shift][current_pixel_col_index_param ] = wall_value_param
    elif wall_value_param == -1:
        wall_list_param[current_pixel_row_index_param][current_pixel_col_index_param] = wall_value_param


def get_wall_list_from_grassland_vertical(row_index_param, col_index_param, letter_list_param):
    if letter_list_param[row_index_param][col_index_param] == 'V':
        return 0, None
    if letter_list_param[row_index_param][col_index_param] == 'W':
        return -1, None
    # only set wall if the cell is neighboring a grass cell, and not on the edge,
    elif letter_list_param[row_index_param][col_index_param] != 'G':
        is_grass_edge, grass_on_top = \
            pixel_is_grass_edge_vertical(row_index_param, col_index_param, letter_list_param)
        if is_grass_edge:
            return 1, grass_on_top
    return 0, None


def pixel_is_grass_edge_vertical(row_index_param, col_index_param, letter_list_param):
    total_row = len(letter_list_param)
    total_col = len(letter_list_param[0])
    if  (row_index_param+1>=total_row or row_index_param-1<0 or
        col_index_param+1>=total_col or col_index_param-1<0):
        return False, None
    if letter_list_param[row_index_param - 1][col_index_param] == 'G':
        return True, True   # second True = grass on top
    elif letter_list_param[row_index_param + 1][col_index_param] == 'G':
        return True, False  # second False = grass on top
    else:
        return False, None


# def pixel_is_neighbouring_grassland(row_index_param, col_index_param, letter_list_param):
#     total_row = len(letter_list_param)
#     total_col = len(letter_list_param[0])
#
#     above_neighboring_grass = False
#     if (row_index_param-1 >= 0 and
#         letter_list_param[row_index_param-1][col_index_param] == 'G'):
#         above_neighboring_grassl = True
#     below_neighboring_grass = False
#     if (row_index_param+1 < total_row and
#         letter_list_param[row_index_param+1][col_index_param] == 'G'):
#         below_neighboring_grass = True
#     left_neighboring_grass = False
#     if (col_index_param-1 >= 0 and
#         letter_list_param[row_index_param][col_index_param-1] == 'G'):
#         left_neighboring_grass = True
#     right_neighboring_grass = False
#     if (col_index_param+1 < total_col and
#         letter_list_param[row_index_param][col_index_param+1] == 'G'):
#         right_neighboring_grass = True
#     above_left_neighboring_grass = False
#     if (row_index_param-1 >= 0 and col_index_param-1 >= 0 and
#         letter_list_param[row_index_param-1][col_index_param-1] == 'G'):
#         above_left_neighboring_grass = True
#     above_right_neighboring_grass = False
#     if (row_index_param-1 >= 0 and col_index_param+1 < total_col and
#         letter_list_param[row_index_param-1][col_index_param+1] == 'G'):
#         above_right_neighboring_grass = True
#     below_left_neighboring_grass = False
#     if (row_index_param+1 < total_row and col_index_param-1 >= 0 and
#         letter_list_param[row_index_param+1][col_index_param-1] == 'G'):
#         below_left_neighboring_grass = True
#     below_right_neighboring_grass = False
#     if (row_index_param+1 < total_row and col_index_param+1 < total_col and
#         letter_list_param[row_index_param+1][col_index_param+1] == 'G'):
#         below_right_neighboring_grass = True
#
#     if (above_neighboring_grass or below_neighboring_grass or
#      left_neighboring_grass or right_neighboring_grass or
#      above_left_neighboring_grass or above_right_neighboring_grass or
#      below_left_neighboring_grass or below_right_neighboring_grass):
#         return True
#     else:
#         return False


# def pixel_is_not_neighbouring_wall(row_index_param, col_index_param, wall_list_param):
#     total_row = len(wall_list_param)
#     total_col = len(wall_list_param[0])
#     if  (row_index_param+1>=total_row or row_index_param-1<0 or
#         col_index_param+1>=total_col or col_index_param-1<0):
#         return False  # NOTE, return False so the current pixel is not set to wall
#     if (wall_list_param[row_index_param - 1][col_index_param] != 1 and
#      wall_list_param[row_index_param + 1][col_index_param] != 1 and
#      wall_list_param[row_index_param][col_index_param - 1] != 1 and
#      wall_list_param[row_index_param][col_index_param + 1] != 1 and
#      wall_list_param[row_index_param - 1][col_index_param - 1] != 1 and
#      wall_list_param[row_index_param - 1][col_index_param + 1] != 1 and
#      wall_list_param[row_index_param + 1][col_index_param - 1] != 1 and
#      wall_list_param[row_index_param + 1][col_index_param + 1] != 1):
#         return True  # NOTE, return True so the current pixel can be set to wall
#     else:
#         return False


def clear_single_wall_cell(wall_list_param, original_wall_list_param):
    total_row = len(wall_list_param)
    total_col = len(wall_list_param[0])
    for i in range(total_row):
        for j in range(total_col):
            if (wall_list_param[i][j] == 1 and is_single_wall_pixel(i, j, wall_list_param)):
                wall_list_param[i][j] = original_wall_list_param[i][j]
    return wall_list_param


def is_single_wall_pixel(row_index_param, col_index_param, wall_list_param):
    total_row = len(wall_list_param)
    total_col = len(wall_list_param[0])

    above_not_wall_cell = False
    if (row_index_param-1 >= 0 and
        wall_list_param[row_index_param-1][col_index_param] != 1):
        above_not_wall_cell = True
    below_not_wall_cell = False
    if (row_index_param+1 < total_row and
        wall_list_param[row_index_param+1][col_index_param] != 1):
        below_not_wall_cell = True
    left_not_wall_cell = False
    if (col_index_param-1 >= 0 and
        wall_list_param[row_index_param][col_index_param-1] != 1):
        left_not_wall_cell = True
    right_not_wall_cell = False
    if (col_index_param+1 < total_col and
        wall_list_param[row_index_param][col_index_param+1] != 1):
        right_not_wall_cell = True
    above_left_not_wall_cell = False
    if (row_index_param-1 >= 0 and col_index_param-1 >= 0 and
        wall_list_param[row_index_param-1][col_index_param-1] != 1):
        above_left_not_wall_cell = True
    above_right_not_wall_cell = False
    if (row_index_param-1 >= 0 and col_index_param+1 < total_col and
        wall_list_param[row_index_param-1][col_index_param+1] != 1):
        above_right_not_wall_cell = True
    below_left_not_wall_cell = False
    if (row_index_param+1 < total_row and col_index_param-1 >= 0 and
        wall_list_param[row_index_param+1][col_index_param-1] != 1):
        below_left_not_wall_cell = True
    below_right_not_wall_cell = False
    if (row_index_param+1 < total_row and col_index_param+1 < total_col and
        wall_list_param[row_index_param+1][col_index_param+1] != 1):
        below_right_not_wall_cell = True

    if (above_not_wall_cell and below_not_wall_cell and
     left_not_wall_cell and right_not_wall_cell and
     above_left_not_wall_cell and above_right_not_wall_cell and
     below_left_not_wall_cell and below_right_not_wall_cell):
        return True
    else:
        return False


def clear_ingrass_wall(wall_list_param, letter_list_param,
                       candidate_wall_cells_to_reset,
                       original_wall_list_param,
                       check_grass_cell_between_neighbors):
    candidate_wall_cells_to_reset = clear_ingrass_wall_horizaontal(wall_list_param, letter_list_param,
                                                                   candidate_wall_cells_to_reset,
                                                                   check_grass_cell_between_neighbors)
    candidate_wall_cells_to_reset = clear_ingrass_wall_vertical(wall_list_param, letter_list_param,
                                                                candidate_wall_cells_to_reset,
                                                                check_grass_cell_between_neighbors)
    for k, v in candidate_wall_cells_to_reset.items():
        if len(v) > 1:      # i.e. value = ['h', 'v'], ingrass both horizaontally and vertically
            i, j = k
            wall_list_param[i][j] = original_wall_list_param[i][j]
    return wall_list_param


def clear_ingrass_wall_horizaontal(wall_list_param, letter_list_param,
                                   candidate_wall_cells_to_reset,
                                   check_grass_cell_between_neighbors):
    total_row = len(wall_list_param)
    total_col = len(wall_list_param[0])
    for i in range(total_row):
        for j in range(total_col):
            if wall_list_param[i][j] == 1:
                # check if the wall cell has grass neighbors on both sides horizontally
                # if yes, then check if all cells between the wall cell and each of the
                # nearest grass neihgbors have grass neighbors on either side vertically,
                # if yes, then add the wall cell in the candidate to reset list, with a value 'h',
                # then go through the candidate to reset list, if the cell's value = ['h', 'v'],
                # then reset, which is done in clear_ingrass_wall after having checked horizontally too
                e_start_col_idx = j + 1
                w_start_col_idx = j - 1
                e_grass_neighbor = False
                w_grass_neighbor = False
                e_grass_neighbor_index = set()
                w_grass_neighbor_index = set()
                for col in range(e_start_col_idx, total_col, 1):
                    # NOTE, as a wall cell already initialised on a grass cell
                    # so, we do not check the immediately grass neighbor as we
                    # want to check if the neighboring non-grass structure wholely ingrass
                    if letter_list_param[i][col] == 'G' and col != e_start_col_idx:
                        e_grass_neighbor = True
                        e_grass_neighbor_index = (i, col)
                        break
                for col in range(w_start_col_idx, -1, -1):
                    # NOTE, as a wall cell already initialised on a grass cell
                    # so, we do not check the immediately grass neighbor as we
                    # want to check if the neighboring non-grass structure wholely ingrass
                    if letter_list_param[i][col] == 'G' and col != w_start_col_idx:
                        w_grass_neighbor = True
                        w_grass_neighbor_index = (i, col)
                        break
                # check all non-grass cells between the current wall cell and the nearest grass cell
                # to both east and west also have north and south grass neighbors, this ensures the wall cell
                # is around an ingrass structure
                # NOTE, south_grass_cell_col = north_grass_cell_col = j, they are here just for unpacking
                east_all_in_grass_to_south = True
                east_all_in_grass_to_north = True
                west_all_in_grass_to_south = True
                west_all_in_grass_to_north = True
                if e_grass_neighbor and w_grass_neighbor and check_grass_cell_between_neighbors:
                    east_all_in_grass_to_south, east_all_in_grass_to_north, \
                    west_all_in_grass_to_south, west_all_in_grass_to_north = \
                        check_cells_inbtween_ingrass_horizontal(letter_list_param, i, j,
                                                                e_grass_neighbor_index, w_grass_neighbor_index)
                #########################################################
                if (e_grass_neighbor and w_grass_neighbor and
                    east_all_in_grass_to_south and
                    east_all_in_grass_to_north and
                    west_all_in_grass_to_south and
                    west_all_in_grass_to_north):
                    values = [v for k, v in candidate_wall_cells_to_reset.items() if k == (i, j)]
                    if len(values) == 0:
                        candidate_wall_cells_to_reset[(i, j)] = ['h']
                    else:
                        candidate_wall_cells_to_reset[(i, j)].append('h')
    return candidate_wall_cells_to_reset


def check_cells_inbtween_ingrass_horizontal(letter_list_param, current_wall_cell_row, current_wall_cell_col,
                                 e_grass_neighbor_index, w_grass_neighbor_index):
    total_row = len(letter_list_param)
    total_col = len(letter_list_param[0])
    east_grass_cell_row, east_grass_cell_col = e_grass_neighbor_index
    east_all_in_grass_to_south = True
    east_all_in_grass_to_north = True
    for col in range(current_wall_cell_col+1, east_grass_cell_col, 1):
        cell_has_south_neighbor = False
        cell_has_north_neighbor = False
        for row in range(current_wall_cell_row+1, total_row, 1):
            if letter_list_param[row][col] == 'G':
                cell_has_south_neighbor = True
                break
        for row in range(current_wall_cell_row-1, -1, -1):
            if letter_list_param[row][col] == 'G':
                cell_has_north_neighbor = True
                break
        if not cell_has_south_neighbor:
            east_all_in_grass_to_south = False
            break
        if not cell_has_north_neighbor:
            east_all_in_grass_to_north = False
            break
    west_grass_cell_row, west_grass_cell_col = w_grass_neighbor_index
    west_all_in_grass_to_south = True
    west_all_in_grass_to_north = True
    for col in range(current_wall_cell_col-1, west_grass_cell_col, -1):
        cell_has_south_neighbor = False
        cell_has_north_neighbor = False
        for row in range(current_wall_cell_row+1, total_row, 1):
            if letter_list_param[row][col] == 'G':
                cell_has_south_neighbor = True
                break
        for row in range(current_wall_cell_row-1, -1, -1):
            if letter_list_param[row][col] == 'G':
                cell_has_north_neighbor = True
                break
        if not cell_has_south_neighbor:
            west_all_in_grass_to_south = False
            break
        if not cell_has_north_neighbor:
            west_all_in_grass_to_north = False
            break
    return east_all_in_grass_to_south, east_all_in_grass_to_north, \
           west_all_in_grass_to_south, west_all_in_grass_to_north


def clear_ingrass_wall_vertical(wall_list_param, letter_list_param,
                                candidate_wall_cells_to_reset,
                                check_grass_cell_between_neighbors):
    total_row = len(wall_list_param)
    total_col = len(wall_list_param[0])
    for j in range(total_col):
        for i in range(total_row):
            if wall_list_param[i][j] == 1:
                # check if the wall cell has grass neighbors on both sides vertically
                # if yes, then check if all cells between the wall cell and each of the
                # nearest grass neihgbors have grass neighbors on either side horizontally,
                # if yes, then add the wall cell in the candidate to reset list, with a value 'v',
                # then go through the candidate to reset list, if the cell's value = ['h', 'v'],
                # then reset, which is done in clear_ingrass_wall after having checked horizontally too
                s_start_row_idx = i + 1
                n_start_row_idx = i - 1
                s_grass_neighbor = False
                n_grass_neighbor = False
                s_grass_neighbor_index = set()
                n_grass_neighbor_index = set()
                for row in range(s_start_row_idx, total_row, 1):
                    # NOTE, as a wall cell already initialised on a grass cell
                    # so, we do not check the immediately grass neighbor as we
                    # want to check if the neighboring non-grass structure wholely ingrass
                    if letter_list_param[row][j] == 'G' and row != s_start_row_idx:
                        s_grass_neighbor = True
                        s_grass_neighbor_index = (row, j)
                        break
                for row in range(n_start_row_idx, -1, -1):
                    # NOTE, as a wall cell already initialised on a grass cell
                    # so, we do not check the immediately grass neighbor as we
                    # want to check if the neighboring non-grass structure wholely ingrass
                    if letter_list_param[row][j] == 'G' and row != n_start_row_idx:
                        n_grass_neighbor = True
                        n_grass_neighbor_index = (row, j)
                        break
                # check all non-grass cells between the current wall cell and the nearest grass cell
                # to both south and north also have west and east grass neighbors, this ensures the wall cell
                # is around an ingrass structure
                # NOTE, south_grass_cell_col = north_grass_cell_col = j, they are here just for unpacking
                south_all_in_grass_to_east = True
                south_all_in_grass_to_west = True
                north_all_in_grass_to_east = True
                north_all_in_grass_to_west = True
                if s_grass_neighbor and n_grass_neighbor and check_grass_cell_between_neighbors:
                    south_all_in_grass_to_east, south_all_in_grass_to_west, \
                    north_all_in_grass_to_east, north_all_in_grass_to_west = \
                        check_cells_inbtween_ingrass_vertical(letter_list_param, i, j,
                                                     s_grass_neighbor_index, n_grass_neighbor_index)
                #########################################################
                if (s_grass_neighbor and n_grass_neighbor and
                    south_all_in_grass_to_east and
                    south_all_in_grass_to_west and
                    north_all_in_grass_to_east and
                    north_all_in_grass_to_west):
                    values = [v for k, v in candidate_wall_cells_to_reset.items() if k == (i, j)]
                    if len(values) == 0:
                        candidate_wall_cells_to_reset[(i, j)] = ['v']
                    else:
                        candidate_wall_cells_to_reset[(i, j)].append('v')
    return candidate_wall_cells_to_reset


def check_cells_inbtween_ingrass_vertical(letter_list_param, current_wall_cell_row, current_wall_cell_col,
                                 s_grass_neighbor_index, n_grass_neighbor_index):
    total_row = len(letter_list_param)
    total_col = len(letter_list_param[0])
    south_grass_cell_row, south_grass_cell_col = s_grass_neighbor_index
    south_all_in_grass_to_east = True
    south_all_in_grass_to_west = True
    for row in range(current_wall_cell_row+1, south_grass_cell_row, 1):
        cell_has_east_neighbor = False
        cell_has_west_neighbor = False
        for col in range(current_wall_cell_col+1, total_col, 1):
            if letter_list_param[row][col] == 'G':
                cell_has_east_neighbor = True
                break
        for col in range(current_wall_cell_col-1, -1, -1):
            if letter_list_param[row][col] == 'G':
                cell_has_west_neighbor = True
                break
        if not cell_has_east_neighbor:
            south_all_in_grass_to_east = False
            break
        if not cell_has_west_neighbor:
            south_all_in_grass_to_west = False
            break
    north_grass_cell_row, north_grass_cell_col = n_grass_neighbor_index
    north_all_in_grass_to_east = True
    north_all_in_grass_to_west = True
    for row in range(current_wall_cell_row-1, north_grass_cell_row, -1):
        cell_has_east_neighbor = False
        cell_has_west_neighbor = False
        for col in range(current_wall_cell_col+1, total_col, 1):
            if letter_list_param[row][col] == 'G':
                cell_has_east_neighbor = True
                break
        for col in range(current_wall_cell_col-1, -1, -1):
            if letter_list_param[row][col] == 'G':
                cell_has_west_neighbor = True
                break
        if not cell_has_east_neighbor:
            north_all_in_grass_to_east = False
            break
        if not cell_has_west_neighbor:
            north_all_in_grass_to_west = False
            break
    return south_all_in_grass_to_east, south_all_in_grass_to_west, \
           north_all_in_grass_to_east, north_all_in_grass_to_west


def join_wall_pixels(wall_list_param):
    total_row = len(wall_list_param)
    total_col = len(wall_list_param[0])
    for i in range(total_row):
        for j in range(total_col):
            if wall_list_param[i][j] == 1:
                search_directions = determine_search_directions(wall_list_param, i, j)
                # Instead of returning the dict, directly update cells in wall_list
                # which are inbetween the current pixel and the next wall pixel
                # so that when come to search for the next wall cell in the wall_list,
                # we do not have to duplicate the effort
                #TODO: search and update the wall_list_param cells

    pass


def determine_search_directions(wall_list_param, row_index_param, col_index_param):
    search_directions = dict()
    reset_search_directions(search_directions)
    adjacent_wall_cells = 0

    if wall_list_param[row_index_param - 1][col_index_param] == 1:
        search_directions['search_upper'] = False
        adjacent_wall_cells += 1
    if wall_list_param[row_index_param + 1][col_index_param] == 1:
        search_directions['search_lower'] = False
        adjacent_wall_cells += 1
    if wall_list_param[row_index_param][col_index_param - 1] == 1:
        search_directions['search_left'] = False
        adjacent_wall_cells += 1
    if wall_list_param[row_index_param][col_index_param + 1] == 1:
        search_directions['search_right'] = False
        adjacent_wall_cells += 1
    if wall_list_param[row_index_param - 1][col_index_param - 1] == 1:
        search_directions['search_upperleft'] = False
        search_directions['search_upper'] = False
        search_directions['search_left'] = False
        adjacent_wall_cells += 1
    if wall_list_param[row_index_param - 1][col_index_param + 1] == 1:
        search_directions['search_upperright'] = False
        search_directions['search_upper'] = False
        search_directions['search_right'] = False
        adjacent_wall_cells += 1
    if wall_list_param[row_index_param + 1][col_index_param - 1] == 1:
        search_directions['search_lowerleft'] = False
        search_directions['search_lower'] = False
        search_directions['search_left'] = False
        adjacent_wall_cells += 1
    if wall_list_param[row_index_param + 1][col_index_param + 1] == 1:
        search_directions['search_lowerright'] = False
        search_directions['search_lower'] = False
        search_directions['search_right'] = False
        adjacent_wall_cells += 1

    if adjacent_wall_cells > 1:
        reset_search_directions(search_directions)

    return search_directions


def reset_search_directions(search_directions_param):
    search_directions_param['search_upper'] = True
    search_directions_param['search_lower'] = True
    search_directions_param['search_left'] = True
    search_directions_param['search_right'] = True
    search_directions_param['search_upperleft'] = True
    search_directions_param['search_upperright'] = True
    search_directions_param['search_lowerleft'] = True
    search_directions_param['search_lowerright'] = True


# NOTE, pix_param should be the one that loaded from im_param
def update_image(pix_param, wall_list_param, im_param, new_image_filename_param):
    total_row = len(wall_list_param)
    total_col = len(wall_list_param[0])
    for i in range(total_row):
        for j in range(total_col):
            if wall_list_param[i][j] == 1:
                # NOTE, pix has flopped indexing, here, correct one is [j, i]
                pix_param[j, i] = (255, 255, 255)
    # im_param.show()
    im_param.save(new_image_filename_param, quality=100)  # Save the modified pixels as .png


def get_cost(wall_list_param, cost_list_param):
    global score_dict  # = {'F': '10', 'W': 0, 'M': 100, "G": 1, "V": -1}
    total_row_wall = len(wall_list_param)
    total_col_wall = len(wall_list_param[0])
    total_row_cost = len(cost_list_param)
    total_col_cost = len(cost_list_param[0])
    if (not ((total_row_wall == total_row_cost) and (total_col_wall == total_col_cost))):
        print('Error, wall_list, cost_list should be equal size')
        return None
    else:
        total_cost = 0
        for i in range(total_row_cost):
            for j in range(total_col_cost):
                if wall_list_param[i][j] == 1:
                    total_cost += cost_list_param[i][j]
        return total_cost


# NOTE, flopped has the correct indexing, note pix indexing is flopped from the list
def test_update_image_flopped(pix_param, letter_list_param, im_param):
    total_row = len(letter_list_param)
    total_col = len(letter_list_param[0])
    for i in range(total_row):
        for j in range(total_col):
            if letter_list_param[i][j] == 'F':
                pix_param[j, i] = (0, 125, 0)
            elif letter_list_param[i][j] == 'G':
                pix_param[j, i] = (0, 125, 125)
            elif letter_list_param[i][j] == 'W':
                pix_param[j, i] = (0, 0, 125)
            elif letter_list_param[i][j] == 'M':
                pix_param[j, i] = (125, 125, 125)
            elif letter_list_param[i][j] == 'V':
                pix_param[j, i] = (255, 0, 0)
    im_param.save('test_modified_map_flopped.png', quality=100)  # Save the modified pixels as .png


def impose_map_letters_on_map_iamge(image_file_param, letter_list_param):
    resize_ratio = 10
    resized_nearest, resized_map_filename_nearest = resize_image(image_file_param, resize_ratio, 'nearest', '_map')

    background_image_filename = resized_map_filename_nearest
    indexes_texts_pair_dict = dict()
    font_filename = 'ITCKRIST.TTF'
    font_size = 8
    text_color = 'rgb(0, 0, 0)'  # black color

    indexes_texts_pair = dict()
    total_row = len(letter_list_param)
    total_col = len(letter_list_param[0])

    for i in range(total_row):
        for j in range(total_col):
            # indexing for the text need to be flopped
            indexes_texts_pair[(j * resize_ratio, i * resize_ratio)] = letter_list_param[i][j]
    print('indexes_texts_pair={}'.format(indexes_texts_pair))
    resized_name, ext = os.path.splitext(resized_map_filename_nearest)
    letters_imposed_map_image_filename = resized_name + '_with_lettters' + '.png'
    impose_text_on_image(background_image_filename, indexes_texts_pair,
                         font_filename, font_size, text_color, letters_imposed_map_image_filename)
    return letters_imposed_map_image_filename


def generate_map_data(map_files, check_grass_cell_between_neighbors):
    text_file = map_files['text_file']
    load_success, letter_list = load_from_text(text_file)
    print('letter_list={}'.format(letter_list))

    # upsample the image 10 times, so we can impose the map letters
    image_file = map_files['image_file']
    iamge_file_name = os.path.basename(image_file)

    staged_image_list = dict()
    staged_cost_list = dict()
    staged_cost_list['orginal_map'] = 0
    staged_image_list['orginal_map'] = iamge_file_name

    letter_imposed_map_file = impose_map_letters_on_map_iamge(image_file, letter_list)
    letter_imposed_map_file_name = os.path.basename(letter_imposed_map_file)
    staged_cost_list['letters_imposed_map'] = 0
    staged_image_list['letters_imposed_map'] = letter_imposed_map_file_name

    v, total_row, total_col = find_village(letter_list)
    cost_list = build_cost_list(letter_list)
    original_wall_list = generate_wall_list(letter_list)

    uncleaned_map_image_filename = 'uncleaned_map.png'
    wall_list_unclean_up = generate_wall_list(letter_list)
    wall_list_unclean_up = \
        find_starting_grass_contour(v, letter_list, wall_list_unclean_up)
    loaded_im_unclean_up, rgb_list_unclean_up, im_unclean_up, pix_unclean_up = \
        load_from_image(image_file)
    update_image(pix_unclean_up, wall_list_unclean_up, im_unclean_up,
                 uncleaned_map_image_filename)
    total_cost_unclean_up = get_cost(wall_list_unclean_up, cost_list)
    print('total_cost_unclean_up = {}'.format(total_cost_unclean_up))
    staged_cost_list['uncleaned_map'] = total_cost_unclean_up
    staged_image_list['uncleaned_map'] = uncleaned_map_image_filename

    cleaned_single_cell_map_image_filename = 'cleaned_single_cell_map.png'
    wall_list_clean_up_single_cell = generate_wall_list(letter_list)
    wall_list_clean_up_single_cell = \
        find_starting_grass_contour(v, letter_list, wall_list_clean_up_single_cell)
    wall_list_clean_up_single_cell = \
        clear_single_wall_cell(wall_list_clean_up_single_cell, original_wall_list)
    loaded_im_clean_up_single_cell, rgb_list_clean_up_single_cell, im_clean_up_single_cell, pix_clean_up_single_cell = \
        load_from_image(image_file)
    update_image(pix_clean_up_single_cell, wall_list_clean_up_single_cell, im_clean_up_single_cell,
                 cleaned_single_cell_map_image_filename)
    total_cost_clean_up_single_cell = get_cost(wall_list_clean_up_single_cell, cost_list)
    print('total_cost_clean_up_single_cell = {}'.format(total_cost_clean_up_single_cell))
    staged_cost_list['cleaned_single_cell_map'] = total_cost_clean_up_single_cell
    staged_image_list['cleaned_single_cell_map'] = cleaned_single_cell_map_image_filename

    cleaned_single_cell_and_ingrass_wall_map_image_filename = 'cleaned_single_cell_and_ingrass_wall_map.png'
    wall_list_clean_up_single_cell_and_ingrass_wall = generate_wall_list(letter_list)
    wall_list_clean_up_single_cell_and_ingrass_wall = \
        find_starting_grass_contour(v, letter_list, wall_list_clean_up_single_cell_and_ingrass_wall)
    wall_list_clean_up_single_cell_and_ingrass_wall = \
        clear_single_wall_cell(wall_list_clean_up_single_cell_and_ingrass_wall, original_wall_list)
    candidate_wall_cells_to_reset = dict()
    wall_list_clean_up_single_cell_and_ingrass_wall = \
        clear_ingrass_wall(wall_list_clean_up_single_cell_and_ingrass_wall, letter_list,
                           candidate_wall_cells_to_reset, original_wall_list, check_grass_cell_between_neighbors)
    loaded_im_clean_up_single_cell_and_ingrass_wall, rgb_list_clean_up_single_cell_and_ingrass_wall, \
        im_clean_up_single_cell_and_ingrass_wall, pix_clean_up_single_cell_and_ingrass_wall = \
        load_from_image(image_file)
    update_image(pix_clean_up_single_cell_and_ingrass_wall, wall_list_clean_up_single_cell_and_ingrass_wall,
                 im_clean_up_single_cell_and_ingrass_wall, cleaned_single_cell_and_ingrass_wall_map_image_filename)
    total_cost_clean_up_single_cell_and_ingrass_wall = \
        get_cost(wall_list_clean_up_single_cell_and_ingrass_wall, cost_list)
    print('total_cost_clean_up_single_cell_and_ingrass_wall = {}'.format(
        total_cost_clean_up_single_cell_and_ingrass_wall))
    staged_cost_list['cleaned_single_cell_and_ingrass_wall_map'] = \
        total_cost_clean_up_single_cell_and_ingrass_wall
    staged_image_list['cleaned_single_cell_and_ingrass_wall_map'] = \
        cleaned_single_cell_and_ingrass_wall_map_image_filename

    return load_success, letter_list, staged_cost_list, staged_image_list

    # test_update_image_flopped(pix, letter_list, im)