from minesweeper_solver import *
from MyDialog import *
from tkinter import messagebox


def on_left_mouse_click(event, mine_arg, grid_arg, grid_text_arg, canvas_arg, text_shift_arg, x_offset_arg, y_offset_arg):
    # note the arg here is the grid that we have just generated, a 2d array of blocks
    total_rows = len(grid_arg)
    total_cols = len(grid_arg)
    w = grid_arg[0][0].t.x_e - grid_arg[0][0].t.x_b

    x, y = event.x, event.y
    # note, the '+2' is because we start the grid 2 unit off the edge, ref. reset_grid_properties
    row_index = int((y+y_offset_arg)/w)
    col_index = int((x+x_offset_arg)/w)
    block_index = Block_Index(row_index, col_index)
    if row_index > total_rows-1 or col_index > total_cols-1:
        print('row index {} or col index {} out of range'.format(row_index, col_index))
    else:
        grid_text_arg = mine_sweeping(block_index, mine_arg, grid_text_arg)
        print('grid_text_arg={}'.format(grid_text_arg))
        if grid_text_arg[row_index][col_index] == '#':
            if messagebox.askyesno("Results", 'Game over, try gain?'):
                reset_grid_text('?', grid_text_arg)
        draw_grid_use_block(canvas_arg, grid_arg, grid_text_arg, text_shift_arg)


def mine_sweeping(block_index_param, mine_param, grid_text_param):
    hit = mine_param[block_index_param.i][block_index_param.j]
    mine_count = 0

    total_rows = len(grid_param)
    total_cols = len(grid_param[0])

    if hit != '#':
        if (block_index_param.i-1 >= 0 and block_index_param.j-1 >= 0 and
                mine_param[block_index_param.i-1][block_index_param.j-1] == '#'):
            mine_count += 1
        if block_index_param.i-1 >= 0  and \
                mine_param[block_index_param.i-1][block_index_param.j] == '#':
            mine_count += 1
        if (block_index_param.i-1 >= 0 and block_index_param.j+1 < total_cols and
                mine_param[block_index_param.i-1][block_index_param.j+1] == '#'):
            mine_count += 1
        if (block_index_param.j+1 < total_cols and
                mine_param[block_index_param.i][block_index_param.j+1] == '#'):
            mine_count += 1
        if (block_index_param.i+1 < total_rows and block_index_param.j+1 < total_cols and
                mine_param[block_index_param.i+1][block_index_param.j+1] == '#'):
            mine_count += 1
        if (block_index_param.i+1 < total_rows and
                mine_param[block_index_param.i+1][block_index_param.j] == '#'):
            mine_count += 1
        if (block_index_param.i+1 < total_rows and block_index_param.j-1 >= 0 and
                mine_param[block_index_param.i+1][block_index_param.j-1] == '#'):
            mine_count += 1
        if (block_index_param.j-1 >= 0 and
                mine_param[block_index_param.i][block_index_param.j-1] == '#'):
            mine_count += 1
        hit = str(mine_count)

    grid_text_param[block_index_param.i][block_index_param.j] = hit

    return grid_text_param


def on_right_mouse_click(event, grid_arg, grid_text_arg, canvas_arg, text_shift_arg):
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
        w = 30
        print('total_rows={}, total_cols={}, w={}'.format(total_rows, total_cols, w))
        grid, x_offset, y_offset = reset_grid_properties(total_rows, total_cols, w, 0)
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
                           mine_arg=mine,
                           grid_arg=grid,
                           grid_text_arg=grid_text,
                           canvas_arg=canvas, text_shift_arg=text_shift,
                           x_offset_arg=x_offset,
                           y_offset_arg=y_offset:
                    on_left_mouse_click(event, mine_arg, grid_arg, grid_text_arg, canvas_arg, text_shift_arg,
                                        x_offset_arg, y_offset_arg))
        canvas.bind('<Button-3>',
                    lambda event,
                           grid_arg=grid,
                           grid_text_arg=grid_text,
                           canvas_arg=canvas, text_shift_arg=text_shift:
                    on_right_mouse_click(event, grid_arg, grid_text_arg, canvas_arg, text_shift_arg))

    root.mainloop()


if __name__ == '__main__':
    main()





