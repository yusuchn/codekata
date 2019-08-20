from performance_eveluation import *


permitted_characters = ['C', 'R', 'C', 'E', 'I', 'N', 'E', 'C', 'T']
print('puzzle = {}'.format(permitted_characters))
permitted_characters_len = len(permitted_characters)
print('permitted_characters_len={}'.format(permitted_characters_len))
permitted_characters_unique_len = len(set(permitted_characters))
print('permitted_characters_unique_len={}'.format(permitted_characters_unique_len))

number_of_words_per_line = 15


def print_result(words, count):
    print('words found = {}'.format(words))
    print('number of words found = {}'.format(count))


def update_results(count, print_new_line_count, words, word):
    global number_of_words_per_line
    count += 1
    print_new_line_count += 1
    if (print_new_line_count > number_of_words_per_line):
        words += word + ", \n"
        print_new_line_count = 0
    else:
        words += word + ", "
    return count, print_new_line_count, words


def find_word_without_check_dup():
    global permitted_characters_len
    count = 0
    print_new_line_count = 0
    words = ""
    for word in open('words_alpha.txt'):
        word = (word.strip().upper())
        if (len(word) > 4 and
            "I" in word and
            set(word) <= set(permitted_characters)):
            count, print_new_line_count, words = \
                update_results(count, print_new_line_count, words, word)
    print_result(words, count)


def find_word_with_check_dup_set():
    count = 0
    print_new_line_count = 0
    words = ""
    for word in open('words_alpha.txt'):
        word = (word.strip().upper())
        if (len(word) > 4 and
            "I" in word and
            set(word) <= set(permitted_characters) and
            not check_dup_set(word)):
            count, print_new_line_count, words = \
                update_results(count, print_new_line_count, words, word)
    print_result(words, count)


def find_word_with_check_dup_counter():
    count = 0
    print_new_line_count = 0
    words = ""
    for word in open('words_alpha.txt'):
        word = (word.strip().upper())
        if (len(word) > 4 and
            "I" in word and
            set(word) <= set(permitted_characters) and
            not check_dup_counter(word)):
            count, print_new_line_count, words = \
                update_results(count, print_new_line_count, words, word)
    print_result(words, count)


def find_word_with_check_dup_dict():
    count = 0
    print_new_line_count = 0
    words = ""
    for word in open('words_alpha.txt'):
        word = (word.strip().upper())
        if (len(word) > 4 and
            "I" in word and
            set(word) <= set(permitted_characters) and
            not check_dup_dict(word)):
            count, print_new_line_count, words = \
                update_results(count, print_new_line_count, words, word)
    print_result(words, count)


def find_word_with_check_dup_sort():
    count = 0
    print_new_line_count = 0
    words = ""
    for word in open('words_alpha.txt'):
        word = (word.strip().upper())
        if (len(word) > 4 and
            "I" in word and
            set(word) <= set(permitted_characters) and
            not check_dup_sort(word)):
            count, print_new_line_count, words = \
                update_results(count, print_new_line_count, words, word)
    print_result(words, count)


import sys, timeit
print ('sys.version={}'.format(sys.version + "\n"))
fns = [p for name, p in globals().items() if name.startswith('find_word')]
for fn in fns:
    print ('%50s %.5f \n' % (fn, timeit.timeit(lambda: fn(), number=1)))