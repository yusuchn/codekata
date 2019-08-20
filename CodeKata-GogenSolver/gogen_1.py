import string
from itertools import product
import functools as ft
import sys
from random import shuffle
import copy

letters = string.ascii_uppercase[:25]  # no Z!
WIDTH, HEIGHT = 5, 5


def load_data(gogen_files):
    print('function: {}'.format(sys._getframe().f_code.co_name))

    words = []
    lines = []
    adjacencies = {}
    # Using try in case user types in unknown file or closes without choosing a file.
    try:
        print('Opening {}'.format(gogen_files['wordlist_file']))
        with open(gogen_files['wordlist_file'], 'r') as f:
            words = f.read().split()
        print('words = {}'.format(words))
        adjacencies = get_adjacencies(words)

        print('Opening {}'.format(gogen_files['grid_file']))
        with open(gogen_files['grid_file'], 'r') as f:
            lines = f.readlines()
        fixed_letters = get_fixed_letters(lines)
        floating_letters = get_floating_letters(fixed_letters)
        print('fixed_letters = {}, \nfloating_letters = {}'.format(fixed_letters, floating_letters))
        # return dict(fixed_letters.items() + floating_letters.items()), adjacencies

        print('Exit {} function'.format(sys._getframe().f_code.co_name))
        return {**fixed_letters, **floating_letters}, adjacencies
    except:
        print("No file exists")

        print('Exit {} function'.format(sys._getframe().f_code.co_name))
        return None


def get_adjacencies(words):
    """Return adjacency lists from input words
    """
    print('function: {}'.format(sys._getframe().f_code.co_name))

    adj = {letter: [] for letter in letters}
    for word in words:
        for n in range(len(word) - 1):
            first_letter, second_letter = word[n], word[n + 1]
            adj[first_letter].append(second_letter)
            adj[second_letter].append(first_letter)

    print('Exit {} function'.format(sys._getframe().f_code.co_name))
    return adj


def get_fixed_letters(lines):
    print('function: {}'.format(sys._getframe().f_code.co_name))

    fixed_letters = {}
    for j, line in enumerate(lines):
        for i, letter in enumerate(line.strip().replace(' ', '')):
            if not letter == '-':
                fixed_letters[letter] = {(i, j)}

    print('Exit {} function'.format(sys._getframe().f_code.co_name))
    return fixed_letters


def get_floating_letters(fixed_letters):
    print('function: {}'.format(sys._getframe().f_code.co_name))

    fixed_places = ft.reduce(set.union, fixed_letters.values())
    # all_places = set((x, y) for x in range(WIDTH) for y in range(HEIGHT))     # equivalent to line below
    all_places = set(product(range(WIDTH), range(HEIGHT)))
    available_places = all_places - fixed_places
    print('available_places = {}'.format(available_places))
    unsolved = {L: available_places for L in letters if L not in fixed_letters}

    print('Exit {} function'.format(sys._getframe().f_code.co_name))
    return unsolved


def print_result(positions):
    print('function: {}'.format(sys._getframe().f_code.co_name))

    inv_map = {list(v)[0]: k for k, v in positions.items()}
    for j in range(HEIGHT):
        print ([inv_map[(i, j)] for i in range(WIDTH)])

    print('Exit {} function'.format(sys._getframe().f_code.co_name))


def get_grid(positions):
    print('function: {}'.format(sys._getframe().f_code.co_name))

    grid = [['-'] * WIDTH for i in range(HEIGHT)]

    for k, v in positions.items():
        # only update the default "-" character in the grid if it's a letter with a fixed index in the positions param
        # because other letters in positions's key may have a set of possible indices
        if len(v) == 1:
            index_pair = list(v)[0]
            row_index = index_pair[1]
            col_index = index_pair[0]
            grid[row_index][col_index] = k

    print('Exit {} function'.format(sys._getframe().f_code.co_name))
    return grid

# ----------------------------------------------------------------------------


def fixed(letter_positions):
    return len(letter_positions) == 1


def floating_letters(positions):
    ret = []
    for k, v in positions.items():
        if len(v) > 1:
            ret.append(k)
    return ret


def floating_letters_with_positions(positions):
    ret = {}
    for k, v in positions.items():
        if len(v) > 1:
            ret[k] = v
    return ret


def set_neighbourhood(positions, letter):
    # fixed_positions = ft.reduce(set.union,
    #                             (v for v in positions.values() if fixed(v)))
    fixed_positions = set()
    for v in positions.values():
        if len(v) > 0 and fixed(v):
            fixed_positions = set.union(fixed_positions, v)
    # NOTE, unplack each position index pair (col, row) in positions[letter] list using *p,
    # then pass on to neghbourhood as seperate params
    # nhd_union = ft.reduce(set.union,
    #                       [neighbourhood(*p) for p in positions[letter]])
    nhd_union = set()
    for p in positions[letter]:
        nhd = neighbourhood(*p)
        if len(nhd) > 0:
            nhd_union = set.union(nhd_union, nhd)
    return nhd_union - fixed_positions


def neighbourhood(col, row):
    return set(product(range(max(0, col - 1), min(WIDTH, col + 2)),
                       range(max(0, row - 1), min(HEIGHT, row + 2))))


def unsolved_order_of_two(positions):
    # return any(len(v) > 1 for v in positions.values())
    return any(len(v) != 1 for v in positions.values())


def unsolved(positions):
    return any(len(v) > 1 for v in positions.values())
    # return any(len(v) != 1 for v in positions.values())


def find_solution(positions, adjacencies):
    print('function: {}'.format(sys._getframe().f_code.co_name))

    num_adjacent_letter = 0
    for floating_letter in floating_letters(positions):
        num_adjacent_letter += len(adjacencies[floating_letter])

    count = 0
    # NOTE, count is used to stop being trapped in infinite loop, interestingly:
    # when setting n = 1, puzzle 2 not solved, but, when setting n = 2, puzzle 2 is solved,
    # number n here is completely arbitrary
    n = 50
    while unsolved(positions) and (count < n * num_adjacent_letter):
        floating_letters_list = floating_letters(positions)
        for floating_letter in floating_letters_list:
            adjacencies_list = adjacencies[floating_letter]
            for adjacent_letter in adjacencies_list:
                count += 1
                nhd = set_neighbourhood(positions, adjacent_letter)
                # update the floating letter's positions set with the overlapping set
                # between neighbourhood set and floating letter's current positions set
                positions[floating_letter] = nhd & positions[floating_letter]
                if fixed(positions[floating_letter]):
                    break

    print('Exit {} function'.format(sys._getframe().f_code.co_name))
    return positions


def shuffle_dict(a_dict):
    import random
    l = list(a_dict.keys())
    random.shuffle(l)
    shuffled_a_dict = dict()
    for key in l:
        shuffled_a_dict.update({key: a_dict[key]})      # It's ok, dict.update take a copy not a reference
    print('unsolved_positions={} \nshuffled keys={} \nshuffled_unsolved_positions={}'.format(
        a_dict, l, shuffled_a_dict))

    return shuffled_a_dict


def find_solution_order_of_two(positions, adjacencies):
    print('function: {}'.format(sys._getframe().f_code.co_name))

    num_adjacent_letter = 0
    for floating_letter in floating_letters(positions):
        num_adjacent_letter += len(adjacencies[floating_letter])

    # unsolved_positions = floating_letters_with_positions(find_solution(positions, adjacencies))

    count = 0
    # if there is still unifxed floating letters, iteratively fixed one till all solved
    # NOTE, count is used to stop being trapped in infinite loop, interestingly:
    # when setting n = 1, puzzle 2 not solved, but, when setting n = 2, puzzle 2 is solved,
    # number n here is completely arbitrary
    n = 50
    while unsolved_order_of_two(positions) and (count < n * num_adjacent_letter):
        unsolved_positions = floating_letters_with_positions(find_solution(positions, adjacencies))

        shuffled_unsolved_positions = shuffle_dict(unsolved_positions)
        if len(shuffled_unsolved_positions) > 0:
            for k, v in shuffled_unsolved_positions.items():
                l = list(v)
                # shuffle(l)
                # for c in l:
                count += 1
                positions[k] = {l[0]}
                find_solution(positions, adjacencies)
                if not unsolved(positions):
                    break

        # temp_positions = copy.deepcopy(positions)
        # if len(unsolved_positions) > 0:
        #     for k, v in unsolved_positions.items():
        #         for c in v:
        #             temp_positions[k] = {c}
        #             find_solution(temp_positions, adjacencies)
        #             if not unsolved(temp_positions):
        #                 positions = temp_positions
        #                 break
        #             else:
        #                 temp_positions = copy.deepcopy(positions)

        # the following code generates the same results as the above block, despite passing the copy not the reference
        # if len(unsolved_positions) > 0:
        #     for k, v in unsolved_positions.items():
        #         for c in v:
        #             count += 1
        #             temp_positions[k] = {c}
        #             find_solution(temp_positions, adjacencies)
        #             if not unsolved(temp_positions):
        #                 break

        print('positions = {}'.format(positions))
    print('Exit {} function'.format(sys._getframe().f_code.co_name))
    return positions





