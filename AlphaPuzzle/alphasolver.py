from generaltools import *
import string
import copy
import pprint


letters = string.ascii_uppercase[:26]
default_letter_for_board = '*'


def load_data(game_files):
    try:
        with open(game_files['puzzle_file'], 'r') as read_file:
            puzzle = json.load(read_file)
            print(puzzle)
        lines = open(game_files['wordlist_file'])
        word_list = get_word_list(lines)
        print('total number of words read {}'.format(len(word_list)))
        return True, puzzle, word_list
    except:
        print("No file exists")
        return False, None, None


def save_data_into_json(file_name_param, array):
    with open(file_name_param, 'w', encoding='utf-8') as write_file:
        parsed = array      #json.loads(array)     #json.loads(str(array))
        json.dump(parsed, write_file, ensure_ascii=False, indent=4)


def get_word_list(lines_param):
    word_list = list()
    for j, line in enumerate(lines_param):
        word_list.append(line.strip().lower())
    return word_list


def get_element(json_obj_param, element_name_param):
    element = json_obj_param[element_name_param]
    return element


def get_fixed_number_letters(json_letters_element_param):
    # NOTE, json 'LETTERS' element has strings for numbers, convert them to numbers for convenience
    output_dict_number_letter = dict()
    for k, v in json_letters_element_param.items():
        output_dict_number_letter[int(k)] = v
    return output_dict_number_letter


# def get_floating_letters(fixed_number_letters_param):
#     global letters
#     return [letter for letter in letters if letter not in fixed_number_letters_param.values()]


def get_board_floating_number_letters(board_param, fixed_number_letters_param):
    board_floating_number_letters = dict()
    for row in board_param:
        for col in row:
            if col != 0 and col not in fixed_number_letters_param.keys():
                board_floating_number_letters[col] = default_letter_for_board
    return board_floating_number_letters


def generate_letter_board(board_param, floating_number_letters_param, fixed_number_letters_param):
    total_row = len(board_param)
    total_col = len(board_param[0])
    letter_board = [[default_letter_for_board] * total_col for m in range(total_row)]
    return update_letter_board(letter_board, board_param, floating_number_letters_param, fixed_number_letters_param)


def update_letter_board(letter_board_param, board_param, floating_number_letters_param, fixed_number_letters_param):
    total_row = len(board_param)
    total_col = len(board_param[0])
    # NOTE, floating_number_letters_param can be either solved or unsolved,
    board_number_letters = {**fixed_number_letters_param, **floating_number_letters_param}
    # always add an element keyed on zero as it is neither in fixed_number_letters_param
    # nor in floating_number_letters_param
    board_number_letters[0] = '-'
    copy_letter_board = copy.deepcopy(letter_board_param)
    for i in range(total_row):
        for j in range(total_col):
            copy_letter_board[i][j] = board_number_letters[board_param[i][j]]
    return copy_letter_board


def get_total_row_total_col(board_param):
    total_row = 0
    total_col = 0
    if board_param:
        total_row = len(board_param)
        total_col = len(board_param[0])
    return total_row, total_col


def string_list_to_number_list(string_list_param):
    int_list = list()
    for element in string_list_param:
        int_list.append(int(element))
    return int_list


def letter_list_to_word(letter_list_param):
    word = ''
    for char in letter_list_param:
        word += char
    return word


def append_letter_or_number_list(letter_or_number_list_param, ret_list_param, is_number_board):
    # if number board, convert strings in the list to back numbers before adding to output,
    # else convert strings, each of which is a letter, back to a word before adding to output
    if is_number_board:
        ret_list_param.append(string_list_to_number_list(letter_or_number_list_param))
    else:
        ret_list_param.append(letter_list_to_word(letter_or_number_list_param))
    return ret_list_param


def extract_list_of_word_numbers(board_param, is_number_board):
    ret_list = []
    ret_list = extract_list_of_word_numbers_horizontal(board_param, ret_list, is_number_board)
    ret_list = extract_list_of_word_numbers_vertical(board_param, ret_list, is_number_board)
    return ret_list


def extract_list_of_word_numbers_horizontal(board_param, ret_list_param, is_number_board):
    letter_or_number_list = list()
    total_row, total_col = get_total_row_total_col(board_param)
    for i in range(total_row):
        for j in range (total_col):
            element = str(board_param[i][j])
            if element != '0' and element != '-' and element != '*':
                letter_or_number_list.append(element)
            else:
                if len(letter_or_number_list) >= 2:
                    ret_list_param = \
                        append_letter_or_number_list(letter_or_number_list, ret_list_param, is_number_board)
                letter_or_number_list = list()
        if len(letter_or_number_list) >= 2:
            ret_list_param = \
                append_letter_or_number_list(letter_or_number_list, ret_list_param, is_number_board)
        letter_or_number_list = list()
    if len(letter_or_number_list) >= 2:
        ret_list_param = \
            append_letter_or_number_list(letter_or_number_list, ret_list_param, is_number_board)
    return ret_list_param


def extract_list_of_word_numbers_vertical(board_param, ret_list_param, is_number_board):
    letter_or_number_list = list()
    total_row, total_col = get_total_row_total_col(board_param)
    for i in range(total_col):
        for j in range (total_row):
            element = str(board_param[j][i])
            if element != '0' and element != '-' and element != '*':
                letter_or_number_list.append(element)
            else:
                if len(letter_or_number_list) >= 2:
                    ret_list_param = \
                        append_letter_or_number_list(letter_or_number_list, ret_list_param, is_number_board)
                letter_or_number_list = list()
        if len(letter_or_number_list) >= 2:
            ret_list_param = \
                append_letter_or_number_list(letter_or_number_list, ret_list_param, is_number_board)
        letter_or_number_list = list()
    if len(letter_or_number_list) >= 2:
        ret_list_param = \
            append_letter_or_number_list(letter_or_number_list, ret_list_param, is_number_board)
    return ret_list_param


# # function below is only useful if solution is letter based, if word base solution, obsolete
# def solved(letter_board_param, dictionary_param):
#     board_word_list = extract_list_of_word_numbers(letter_board_param, is_number_board=False)
#     pprint.pprint('board_word_list = \n{}'.format(board_word_list))
#
#     # check if the words accumulated in the english_word list
#     solved = True
#     words_not_in_dictionary = list()
#     for word in board_word_list:
#         # word = 'build'  # set a known word for testing
#         if word not in dictionary_param:
#             words_not_in_dictionary.append(word)
#             if solved:      # only need to set to false if it's still True
#                 solved = False
#             # break         # do not break, accumulate the words that are not in the dictionary
#     print('solved = {}, number of words not in the english_word_list = {}'.format(
#         solved, len(words_not_in_dictionary)))
#     return solved
#
#     # TODO: words_alpha.txt may not be exhaustive of english words, and some harder puzzles may have
#     #  difficult words that are not included in words_alpha.txt, in which case, adam's approach in
#     #  swift is to generate a API to do a google search, with the quotation mark around the word,
#     #  to do that, he would need to determine which word out of the puzzle that is not in words_alpha.txt,
#     #  which in itself is an interesting question


def get_ordered_list_of_word_numbers_by_prob(board_param, fixed_number_letters_param):
    list_of_word_numbers = extract_list_of_word_numbers(board_param, is_number_board=True)
    board_floating_number_letters = get_board_floating_number_letters(board_param, fixed_number_letters_param)
    number_floating_letters = len(board_floating_number_letters)
    if number_floating_letters == 0:
        return
    prob_dict = dict()
    ordered_list_of_word_numbers = list()
    # calculate probability for each word_number_list, and paired with indexes
    for i in range(len(list_of_word_numbers)):
        number_of_fixed_letters = 0
        for number in list_of_word_numbers[i]:
            if(number in fixed_number_letters_param):
                number_of_fixed_letters += 1
        # when calculating probability, number of fixed letters takes priority, hence the real numder,
        # length of the word treated as a fraction against the total number of floating letters, so,
        # it doesn't compete with number of fixed letters, note, shorter word has higher probability
        prob = number_of_fixed_letters + \
               (number_floating_letters - len(list_of_word_numbers[i])) / number_floating_letters
        prob_dict[i] = prob
    # sort the probability list by the probability values in descending order
    sorted_prob_dict = sort_dict(prob_dict, sort_by_key_param=False, reverse_param=True)
    # reorder the original lost of word numbers by the
    for element in sorted_prob_dict:
        ordered_list_of_word_numbers.append(list_of_word_numbers[element[0]])
    return ordered_list_of_word_numbers


# for one single number list, say, [11, 14, 14, 24, 9]:
# 1. measure the length, here, len = 5,
# 2. extract the number(s) in [11, 14, 14, 24, 9], that are found in fixed_number_letters,
#    say {1: 'D', 14: 'N'}, here, they are [14, 14], paired to [N, N]
# 3. also extract positions (indexes) of these number(s) in the number list, here [1, 2]
# 4. search through dictionary, extract all words that has the same pattern
def extract_candidate_words_from_dictionary(number_list_of_the_word_param, dictionary_param,
                                            fixed_number_letters_param):
    number_list_len = len(number_list_of_the_word_param)
    candidate_word_list = list()
    # NOTE, do not use dict to pair the index and letter because there may be duplicated number/letters in a word
    # fixed_letter_index_in_word and fixed_letter_letter_in_word should be of equal length
    fixed_letter_index_in_word = list()
    fixed_letter_letter_in_word = list()
    for i in range(number_list_len):
        if number_list_of_the_word_param[i] in fixed_number_letters_param:
            fixed_letter_index_in_word.append(i)
            fixed_letter_letter_in_word.append(fixed_number_letters_param[number_list_of_the_word_param[i]])
    for word in dictionary_param:
        if len(word) == number_list_len:
            is_candidate = True
            for j in range(len(fixed_letter_index_in_word)):
                if word[fixed_letter_index_in_word[j]] != fixed_letter_letter_in_word[j].lower():
                    is_candidate = False
                    break
            if(is_candidate):
                candidate_word_list.append(word)
    return candidate_word_list


# NOTE, this is a recursive function, board_floating_number_letters_param and fixed_number_letters_param,
# are recursively being updated, ordered_list_of_word_numbers_param and dictionary_param are constant
def solve_puzzle(iteration, board_param, fixed_number_letters_param, dictionary_param):
    board_floating_number_letters = get_board_floating_number_letters(board_param, fixed_number_letters_param)
    ordered_list_of_word_numbers = get_ordered_list_of_word_numbers_by_prob(board_param, fixed_number_letters_param)

    # if( not ordered_list_of_word_numbers or
    #     len(ordered_list_of_word_numbers) == 0 ):
    if len(board_floating_number_letters) == 0:
        print('solver, iteration {}: for testing, len(board_floating_number_letters) = 0, returning: \n '
              'True, fixed_number_letters_param = {}'.format(iteration, fixed_number_letters_param))
        letter_borad = generate_letter_board(board_param, board_floating_number_letters, fixed_number_letters_param)
        return True, fixed_number_letters_param, letter_borad

    to_iterate = False
    number_list_to_iterate = list()
    for number_list_of_the_word in ordered_list_of_word_numbers:
        for i, number in enumerate(number_list_of_the_word):
            if number not in fixed_number_letters_param:
                number_list_to_iterate = number_list_of_the_word
                to_iterate = True
                break
        if to_iterate:
            break

    if not to_iterate:
        letter_borad = generate_letter_board(board_param, board_floating_number_letters, fixed_number_letters_param)
        return True, fixed_number_letters_param, letter_borad

    candidate_words = extract_candidate_words_from_dictionary(
        number_list_to_iterate, dictionary_param, fixed_number_letters_param)

    fixed_number_letters_param_copy = copy.deepcopy(fixed_number_letters_param)
    letter_borad = generate_letter_board(board_param, board_floating_number_letters, fixed_number_letters_param)
    for word in candidate_words:
        fixed_number_letters_param_copy = copy.deepcopy(fixed_number_letters_param)
        for i, letter in enumerate(word):
            if (letter in fixed_number_letters_param_copy.values()):
                continue
            fixed_number_letters_param_copy[number_list_to_iterate[i]] = letter.upper()

        print('solver, iteration {}: fixed_number_letters_param_copy = {}'.format(iteration, fixed_number_letters_param_copy))

        if iteration > 50: # debuging, stop going into infinite loop
            return True, fixed_number_letters_param_copy, letter_borad
        iteration += 1
        solved, fixed_number_letters_paramc_copy, letter_borad = solve_puzzle(iteration, board_param,
                                                                              fixed_number_letters_param_copy,
                                                                              dictionary_param)
        if solved:
            return solved, fixed_number_letters_param_copy, letter_borad

    return False, fixed_number_letters_param_copy, letter_borad








