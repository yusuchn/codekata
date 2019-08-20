from performance_eveluation import *


number_of_words_per_line_for_printing = 15


def load_data(game_files):
    try:
        lines = open(game_files['puzzle_file'])
        permitted_characters, permitted_characters_print, center_character, center_character_print = \
            get_permitted_characters(lines)
        print('permitted_characters = {}, center_character = {}'.format(
            permitted_characters_print, center_character_print))
        lines = open(game_files['wordlist_file'])
        word_list = get_word_list(lines)
        print('total number of words read {}'.format(len(word_list)))
        return True, word_list, permitted_characters, center_character
    except:
        print("No file exists")
        return False, None, None, None


def get_permitted_characters(lines):
    permitted_characters = list()
    permitted_characters_print = list()
    for j, line in enumerate(lines):
        for i, character in enumerate(line.strip().replace(' ', '')):
            permitted_characters_print.append(character)
        for i, character in enumerate(line.strip().lower().replace(' ', '')):
            permitted_characters.append(character)
    center_character_index = int(len(permitted_characters)/2)       # note same index for print
    center_character = permitted_characters[center_character_index]
    center_character_print = permitted_characters_print[center_character_index]
    return permitted_characters, permitted_characters_print, center_character, center_character_print


def get_word_list(lines):
    word_list = list()
    for j, line in enumerate(lines):
        word_list.append(line.strip().lower())
    return word_list


def print_result(words_str, count):
    print('words found = {}'.format(words_str))
    print('number of words found = {}'.format(count))


def update_results(word_count, print_new_line_count, words_str, word_str):
    global number_of_words_per_line_for_printing
    word_count += 1
    print_new_line_count += 1
    if print_new_line_count > number_of_words_per_line_for_printing:
        words_str += word_str + ", \n"
        print_new_line_count = 0
    else:
        words_str += word_str + ", "
    return word_count, print_new_line_count, words_str


def find_word_without_check_dup(word_list_param, permitted_characters_param, center_character):
    count = 0
    print_new_line_count = 0
    words = ''
    for word in word_list_param:
        if (len(word) > 4 and
            center_character in word and
            set(word) <= set(permitted_characters_param)):
            count, print_new_line_count, words = \
                update_results(count, print_new_line_count, words, word)
    print_result(words, count)


def find_word_with_check_dup_set(word_list_param, permitted_characters_param, center_character):
    count = 0
    print_new_line_count = 0
    words = ""
    for word in word_list_param:
        if (len(word) > 4 and
            center_character in word and
            set(word) <= set(permitted_characters_param) and
            not check_dup_set(word)):
            count, print_new_line_count, words = \
                update_results(count, print_new_line_count, words, word)
    print_result(words, count)


def find_word_with_check_dup_counter(word_list_param, permitted_characters_param, center_character):
    count = 0
    print_new_line_count = 0
    words = ""
    for word in word_list_param:
        if (len(word) > 4 and
            center_character in word and
            set(word) <= set(permitted_characters_param) and
            not check_dup_counter(word)):
            count, print_new_line_count, words = \
                update_results(count, print_new_line_count, words, word)
    print_result(words, count)


def find_word_with_check_dup_dict(word_list_param, permitted_characters_param, center_character):
    count = 0
    print_new_line_count = 0
    words = ""
    for word in word_list_param:
        if (len(word) > 4 and
            center_character in word and
            set(word) <= set(permitted_characters_param) and
            not check_dup_dict(word)):
            count, print_new_line_count, words = \
                update_results(count, print_new_line_count, words, word)
    print_result(words, count)


def find_word_with_check_dup_sort(word_list_param, permitted_characters_param, center_character):
    count = 0
    print_new_line_count = 0
    words = ""
    for word in word_list_param:
        if (len(word) > 4 and
            center_character in word and
            set(word) <= set(permitted_characters_param) and
            not check_dup_sort(word)):
            count, print_new_line_count, words = \
                update_results(count, print_new_line_count, words, word)
    print_result(words, count)


# import sys, timeit
# print ('sys.version={}'.format(sys.version + "\n"))
# load_success, word_list, permitted_characters = load_data({'wordlist_file': 'words_alpha.txt', 'puzzle_file': 'puzzle_1.txt'})
# fns = [p for name, p in globals().items() if name.startswith('find_word')]
# for fn in fns:
#     print ('%50s %.5f' % (fn, timeit.timeit(lambda: fn(word_list, permitted_characters, center_character), number=1)))

