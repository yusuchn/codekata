from generaltools import *
import string
import copy
import pprint
from PIL import Image


score_dict = {'F': '10', 'W': 0, 'M': 100, "G": 1}
villege_letter = 'V'
villege_rgb = (54, 61, 0)


def load_from_image(map_jpag_filename):
    try:
        im_rgb_list = list()
        im = Image.open(map_jpag_filename)    # (map_jpag_filename)  # Can be many different formats.
        print('image size = {}'.format(im.size))  # Get the width and hight of the image for iterating over
        pix = im.load()     # pixel RGB value of the image
        for i in range(im.size[0]):
            row_rgb_list = list()
            for j in range(im.size[1]):
                row_rgb_list.append(pix[i, j])
                # if pix[i, j] == (0, 67, 154):
                #     pix[i, j] = (0, 0, 0)     # modify pixel rgb value
            im_rgb_list.append(row_rgb_list)
        # im.save('modified_im.png')  # Save the modified pixels as .png
        return True, im_rgb_list
    except:
        print("No image map file exists")
        return False, None


def load_from_text(map_txt_filename):
    try:
        lines = open(map_txt_filename)     # (map_txt_filename)    #
        map_letter_list = get_letter_list(lines)
        return True, map_letter_list
    except:
        print("No text map file exists")
        return False, None


def get_letter_list(lines_param):
    letter_list = list()
    for j, line in enumerate(lines_param):
        line_letter_list = list()
        for letter in line.strip():
            line_letter_list.append(letter)
        letter_list.append(line_letter_list)
    return letter_list


def find_village_from_letter_map(letter_map_param):
    total_row = len(letter_map_param)
    total_col = len(letter_map_param[0])
    for i in range(total_row):
        for j in range(total_col):
            if letter_map_param[i][j] == villege_letter:        # 'V':
                return (i, j), total_row, total_col


def find_village_from_rgb_map(rgb_map_param):
    global villege_letter
    total_row = len(rgb_map_param)
    total_col = len(rgb_map_param[0])
    for i in range(total_row):
        for j in range(total_col):
            if rgb_map_param[i][j] == villege_rgb:
                return (i, j), total_row, total_col


loaded, text_loaded_map = load_from_text('map.txt')
nparray_text_loaded_map = np.array(text_loaded_map)
v, total_row, total_col = find_village_from_letter_map(text_loaded_map)
print('v={}, total_row={}, total_col={}'.format(v, total_row, total_col))
# pprint.pprint('text_loaded_map=\n{}'.format(text_loaded_map))
print('nparray_text_loaded_map=\n{}'.format(nparray_text_loaded_map))

loaded_im, rgb_loaded_map = load_from_image('Defense.jpg')
nparray_rgb_loaded_map = np.array(rgb_loaded_map)
v, total_row, total_col = find_village_from_rgb_map(rgb_loaded_map)
print('v={}, total_row={}, total_col={}'.format(v, total_row, total_col))
# pprint.pprint('rgb_loaded_map = {}'.format(rgb_loaded_map))
print('nparray_rgb_loaded_map=\n{}'.format(nparray_rgb_loaded_map))


