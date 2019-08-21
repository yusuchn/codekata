from alphasolver import *
from MyDialog import *


root = Tk()
root.withdraw()     # hide the little root window


def main():
    d = MyDialog_GameFiles(root, "Game Files")
    game_files = d.result

    if game_files:
        print('\ngame files are: {}\n'.format(game_files))

        # load data from files
        load_success, puzzle, dictionary = load_data(game_files)

        # parse data
        board = get_element(puzzle, 'board')
        letters = get_element(puzzle, 'letters')
        fixed_number_letters = get_fixed_number_letters(letters)

        board_floating_number_letters = get_board_floating_number_letters(board, fixed_number_letters)
        original_letter_board = generate_letter_board(board, board_floating_number_letters, fixed_number_letters)
        nparray_board = np.array(board)
        nparray_original_letter_board = np.array(original_letter_board)

        print('puzzle = \n{}'.format(puzzle))
        print('fixed_number_letters = {}'.format(fixed_number_letters))
        pprint.pprint('board = \n{}'.format(board))
        print('nparray_board = \n{}'.format(nparray_board))
        print('nparray_original_letter_board = \n{}'.format(nparray_original_letter_board))

        solved, new_fixed_number_letters, solved_letter_board = solve_puzzle(0, board, fixed_number_letters, dictionary)
        if solved:
            # for some reason, the returning value of new_fixed_number_letters doesn't give the correct value
            # uncomment the following line to see the phenomena
            # pprint.pprint('fixed_number_letters = \n{}'.format(new_fixed_number_letters))
            nparray_solved_letter_board = np.array(solved_letter_board)
            print('nparray_solved_letter_board = \n{}'.format(nparray_solved_letter_board))

    root.mainloop()


if __name__ == '__main__':
    main()





