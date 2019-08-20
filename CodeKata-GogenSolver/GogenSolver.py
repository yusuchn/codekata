#! python

import tkinter
from gogen_2 import *
from MyDialog import *

ui_size_devider = 2
w = int(100/ui_size_devider)
r = int(30/ui_size_devider)
circle_shift = int(50/ui_size_devider)
text_shift = int(50/ui_size_devider)
print_drawing_debug = False
total_row = 5
total_col = 5
grid_default = [['-'] * total_row for i in range(total_col)]
geometry_w = int(500/ui_size_devider)
geometry_h = int(500/ui_size_devider)
font_size = int(24/ui_size_devider)
line_width = int(2/ui_size_devider)
circle_width = int(2/ui_size_devider)


root = Tk()
# root.geometry("500x500")
root.geometry("{}x{}".format(geometry_w,geometry_h))
root.wm_title("Gogen Solver")

canvas = Canvas(root, width=500, height=500, borderwidth=0, highlightthickness=0, bg="white smoke")
# canvas.grid()
canvas.pack()


def create_circle(canvas, x, y, r, **kwargs):
    return canvas.create_oval(x-r, y-r, x+r, y+r, **kwargs)


def create_circle_arc(canvas, x, y, r, **kwargs):
    if "start" in kwargs and "end" in kwargs:
        kwargs["extent"] = kwargs["end"] - kwargs["start"]
        del kwargs["end"]
    return canvas.create_arc(x-r, y-r, x+r, y+r, **kwargs)


def draw_grid(canvas, grid):
    print('function: {}'.format(sys._getframe().f_code.co_name))

    global w
    global r
    global circle_shift
    global text_shift
    global draw_debug
    global total_row
    global total_col
    global font_size
    global line_width
    global circle_width

    canvas.delete('all')
    x, y = 0, 0
    for row in grid:
        for col in row:
            row_index = int(y / w)
            col_index = int(x / w)
            letter = grid[row_index][col_index]
            if print_drawing_debug:
                print('row_index={}, col_index={}, letter={}'.format(row_index, col_index, letter))
            circle_x = x + circle_shift
            circle_y = y + circle_shift
            text_x = x + text_shift
            text_y = y + text_shift
            if row_index < total_row-1 and col_index < total_col-1:
                canvas.create_line(circle_x, circle_y, circle_x+w, circle_y, fill="black", width=line_width)
                canvas.create_line(circle_x+w, circle_y, circle_x+w, circle_y+w, fill="black", width=line_width)
                canvas.create_line(circle_x, circle_y, circle_x, circle_y+w, fill="black", width=line_width)
                canvas.create_line(circle_x, circle_y+w, circle_x+w, circle_y+w, fill="black", width=line_width)
                canvas.create_line(circle_x, circle_y, circle_x+w, circle_y+w, fill="black", width=line_width)
                canvas.create_line(circle_x, circle_y+w, circle_x+w, circle_y, fill="black", width=line_width)
            create_circle(canvas, circle_x, circle_y, r, fill="white smoke", outline="black", width=circle_width)
            canvas.create_text(text_x, text_y, font="Arial {} bold".format(font_size), text=letter)
            x = x + w
        y = y + w
        x = 0
    canvas.pack(fill=BOTH, expand=1)

    print('Exit {} function'.format(sys._getframe().f_code.co_name))


def click(event):
    print('function: {}'.format(sys._getframe().f_code.co_name))

    d = MyDialog_GogenFiles(root, "Gogen Solver")
    gogen_files = d.result
    if gogen_files:
        print('\ngogen files are: {}'.format(gogen_files))
        positions, adjacencies = load_data(gogen_files)
        print('positions = {}\nadjacencies = {}'.format(positions, adjacencies))
        positions_grid = get_grid(positions)
        print('positions_grid = {}'.format(positions_grid))
        draw_grid(canvas, positions_grid)
        if messageBox.askyesno('Gogen Solver', 'Continue to find solution?'):
            # solution = find_solution(positions, adjacencies)
            solution = find_solution_order_of_two(positions, adjacencies)
            solution_grid = get_grid(solution)
            print('solution_grid = {}'.format(solution_grid))
            draw_grid(canvas, solution_grid)

    print('Exit {} function'.format(sys._getframe().f_code.co_name))


def main():
    global grid_default
    global canvas

    draw_grid(canvas, grid_default)
    canvas.bind('<Button-1>', click)
    messageBox.showinfo('Gogen Solver', 'Click on the board to start a game',
                           icon="info", parent=root)
    root.mainloop()


if __name__ == '__main__':
    main()


