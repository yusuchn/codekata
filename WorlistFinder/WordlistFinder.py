#! python

import tkinter
from nsw_2 import *
from MyDialog import *

root = Tk()
root.withdraw()     # hide the little root window

def main():
    d = MyDialog_GogenFiles(root, "Wordlist Finger")
    game_files = d.result

    if game_files:
        print('\ngame files are: {}\n'.format(game_files))
        import sys, timeit
        print('sys.version={}'.format(sys.version + "\n"))
        load_success, word_list, permitted_characters, center_character = load_data(game_files)
        fns = [p for name, p in globals().items() if name.startswith('find_word')]
        for fn in fns:
            print('%50s %.5f' % (fn, timeit.timeit(lambda: fn(word_list, permitted_characters, center_character), number=1)))

    root.mainloop()


if __name__ == '__main__':
    main()


