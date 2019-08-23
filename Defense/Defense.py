from generaltools import *
import pprint
from PIL import Image


score_dict = {'F': '10', 'W': 0, 'M': 100, "G": 1, "V": -1}
villege_letter = 'V'
villege_rgb = (54, 61, 0)


def load_from_image(map_jpag_filename):
    try:
        im = Image.open(map_jpag_filename)    # (map_jpag_filename)  # Can be many different formats.
        print('image size = {}'.format(im.size))  # Get the width and hight of the image for iterating over
        rgb_list = get_rgb_list(im)
        return True, rgb_list
    except:
        print("No image map file exists")
        return False, None


def get_rgb_list(im_param):
    pix = im_param.load()  # pixel RGB value of the image
    rgb_list = [[(0, 0, 0)] * im_param.size[1] for n in range(im_param.size[0])]
    for i in range(im_param.size[0]):
        for j in range(im_param.size[1]):
            rgb_list[i][j] = pix[i, j]
            # if pix[i, j] == (0, 67, 154):
            #     pix[i, j] = (0, 0, 0)     # modify pixel rgb value
    # im.save('modified_im.png')  # Save the modified pixels as .png
    return rgb_list


def load_from_text(map_txt_filename):
    try:
        lines = open(map_txt_filename)     # (map_txt_filename)    #
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


def find_village_from_letter_list(letter_list_param):
    global villege_letter
    total_row = len(letter_list_param)
    total_col = len(letter_list_param[0])
    for i in range(total_row):
        for j in range(total_col):
            if letter_list_param[i][j] == villege_letter:        # 'V':
                return (i, j), total_row, total_col


def find_village_from_rgb_list(rgb_list_param):
    global villege_rgb
    total_row = len(rgb_list_param)
    total_col = len(rgb_list_param[0])
    for i in range(total_row):
        for j in range(total_col):
            if rgb_list_param[i][j] == villege_rgb:
                return (i, j), total_row, total_col


def build_cost_list(letter_list_param):
    global score_dict       # = {'F': '10', 'W': 0, 'M': 100, "G": 1, "V": -1}
    total_row = len(letter_list_param)
    total_col = len(letter_list_param[0])
    cost_list = [[0] * total_col for n in range(total_row)]
    for i in range(total_row):
        for j in range(total_col):
            cost_list[i][j] = score_dict[letter_list_param[i][j]]
    return cost_list


loaded, letter_list = load_from_text('map.txt')
nparray_letter_list = np.array(letter_list)
v, total_row, total_col = find_village_from_letter_list(letter_list)
print('v={}, total_row={}, total_col={}'.format(v, total_row, total_col))
# pprint.pprint('letter_list=\n{}'.format(letter_list))
print('nparray_letter_list=\n{}'.format(nparray_letter_list))

loaded_im, rgb_list = load_from_image('Defense.jpg')
nparray_rgb_list = np.array(rgb_list)
v, total_row, total_col = find_village_from_rgb_list(rgb_list)
print('v={}, total_row={}, total_col={}'.format(v, total_row, total_col))
# pprint.pprint('rgb_list = {}'.format(rgb_list))
print('nparray_rgb_list=\n{}'.format(nparray_rgb_list))

cost_list = build_cost_list(letter_list)
nparray_cost_list = np.array(cost_list)
# pprint.pprint('cost_list = {}'.format(cost_list))
print('nparray_cost_list=\n{}'.format(nparray_cost_list))




