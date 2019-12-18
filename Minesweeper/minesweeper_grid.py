from minesweeper_solver import *
from MyDialog import *
from tkinter import messagebox


def on_left_mouse_click(event, grid_arg, grid_text_arg, canvas_arg, text_shift_arg, x_offset_arg, y_offset_arg):
    # note the arg here is the grid that we have just generated, a 2d array of blocks
    total_rows = len(grid_arg)
    total_cols = len(grid_arg)
    w = grid_arg[0][0].t.x_e - grid_arg[0][0].t.x_b

    x, y = event.x, event.y
    # note, the '+2' is because we start the grid 2 unit off the edge, ref. reset_grid_properties
    row_index = int((y+y_offset_arg)/w)
    col_index = int((x+x_offset_arg)/w)
    if row_index > total_rows-1 or col_index > total_cols-1:
        print('row index {} or col index {} out of range'.format(row_index, col_index))
    else:
        hit = '#'    # mine_sweeping(row_index, col_index)
        if hit == '#':
            if messagebox.askyesno("Results", 'Game over, try gain?'):
                reset_grid_text('?', grid_text_arg)
                draw_grid_use_block(canvas_arg, grid_arg, grid_text_arg, text_shift_arg)


def on_right_mouse_click(event, grid_arg, grid_text_arg, canvas_arg, text_shift_arg):
    # todo, give up anyway, restart the game
    if messagebox.askyesno("Game", 'Restart?'):
        reset_grid_text('?', grid_text_arg)
        draw_grid_use_block(canvas_arg, grid_arg, grid_text_arg, text_shift_arg)


root = Tk()
root.withdraw()     # hide the little root window


def main():
    d = MyDialog_GameFiles(None, "Game Files")
    game_files = d.result

    if game_files:
        print('\ngame files are: {}\n'.format(game_files))

        # load data from files
        load_success, game = load_data(game_files)

        # parse data
        mine = get_element(game, 'mine_grid')
        expected_results = get_element(game, 'expected_results')
        print('mine={}\nexpected_results={}'.format(mine, expected_results))

        total_rows = len(mine)
        total_cols = len(mine[0])
        w = 15
        print('total_rows={}, total_cols={}, w={}'.format(total_rows, total_cols, w))
        grid, x_offset, y_offset = reset_grid_properties(total_rows, total_cols, w)
        grid_text = initialise_grid_text('?', total_rows, total_cols)
        grid_text_default = copy.deepcopy(grid_text)

        text_shift = int(w / 2)
        root_width = w * total_cols + 6
        root_height = w * total_rows + 6
        root_geometry_str = '{}x{}'.format(root_width, root_height)

        root, frame, canvas = init_tkinter(root_geometry_str, root_width, root_height)
        draw_grid_use_block(canvas, grid, grid_text, text_shift)

        canvas.bind('<Button-1>',
                    lambda event,
                           grid_arg=grid,
                           grid_text_arg=grid_text,
                           canvas_arg=canvas, text_shift_arg=text_shift,
                           x_offset_arg=x_offset,
                           y_offset_arg=y_offset:
                    on_left_mouse_click(event, grid_arg, grid_text_arg, canvas_arg, text_shift_arg,
                                        x_offset_arg, y_offset_arg))
        canvas.bind('<Button-3>',
                    lambda event,
                           grid_arg=grid,
                           grid_text_arg=grid_text,
                           canvas_arg=canvas, text_shift_arg=text_shift:
                    on_right_mouse_click(event, grid_arg, grid_text_arg, canvas_arg, text_shift_arg))

        # fixed_number_letters = get_fixed_number_letters(letters)
        #
        # board_floating_number_letters = get_board_floating_number_letters(board, fixed_number_letters)
        # original_letter_board = generate_letter_board(board, board_floating_number_letters, fixed_number_letters)
        # nparray_board = np.array(board)
        # nparray_original_letter_board = np.array(original_letter_board)
        #
        # print('puzzle = \n{}'.format(puzzle))
        # print('fixed_number_letters = {}'.format(fixed_number_letters))
        # pprint.pprint('board = \n{}'.format(board))
        # print('nparray_board = \n{}'.format(nparray_board))
        # print('nparray_original_letter_board = \n{}'.format(nparray_original_letter_board))
        #
        # solved, new_fixed_number_letters, solved_letter_board = solve_puzzle(0, board, fixed_number_letters, dictionary)
        # if solved:
        #     # for some reason, the returning value of new_fixed_number_letters doesn't give the correct value
        #     # uncomment the following line to see the phenomena
        #     # pprint.pprint('fixed_number_letters = \n{}'.format(new_fixed_number_letters))
        #     nparray_solved_letter_board = np.array(solved_letter_board)
        #     print('nparray_solved_letter_board = \n{}'.format(nparray_solved_letter_board))

    root.mainloop()


if __name__ == '__main__':
    main()





