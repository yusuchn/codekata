#! python

import numpy as np
import matplotlib.pyplot as plt
#import tkinter as tk


# example plot
#H = np.array([[1, 2, 3, 4, 5],
#              [6, 7, 8, 9, 10],
#              [11, 12, 13, 14, 15],
#              [16, 17, 18, 19, 20],
#              [21, 22, 23, 24, 25]])  # added some commas and array creation code

#fig = plt.figure(figsize=(6, 3.2))

#ax = fig.add_subplot(111)
#ax.set_title('colorMap')
#plt.imshow(H)
#ax.set_aspect('equal')

#cax = fig.add_axes([0.12, 0.1, 0.78, 0.8])
#cax.get_xaxis().set_visible(False)
#cax.get_yaxis().set_visible(False)
#cax.patch.set_alpha(0)
#cax.set_frame_on(False)
#plt.colorbar(orientation='vertical')
#plt.show()


from tkinter import *
#from tkinter import Tk, Canvas, Frame, BOTH

# if not copy tkSimpleDialog to the project folder, need to uncomment following, but doesn't seem to work?
# import sys
# # sys.path.append('C:\suyu\CodeKatas\Python-2.7.3-master\Python-2.7.3-master\Lib\lib-tk')
# sys.path.insert(0, 'C:\suyu\CodeKatas\Python-2.7.3-master\Python-2.7.3-master\Lib\lib-tk')
# print(sys.path)

# copy necessary files to project folder ,
import tkSimpleDialog


# game board
total_row = 6
total_col = 6
grid = [[1] * total_col for n in range(total_row)]
w = 100
image_shift = (100-64)/2

# players
current_player = 'none'
cell_colours = {'me_human':'SteelBlue1', 'me_computer':'SteelBlue4', 'another_human':'DarkOrange1', 'another_computer':'DarkOrange4', 'another_remote':'DarkOliveGreen3', 'neutron':'white smoke', 'board':'blue', 'invalid':'none'}
cell_images = {'me_human':'Circle.gif', 'me_computer':'Circle.gif', 'another_human':'Cross.gif', 'another_computer':'Cross.gif', 'another_remote':'Cross.gif', 'neutron':'Star.gif', 'board':'none', 'invalid':'none'}
grid_colours_old = [[cell_colours['board']] * total_col for m in range(total_row)]

# steps
step_completed_me = 0
step_completed_another = 0
# when use the extended steps the cell_colours, and cell_image, need to be updated for corresponding steps too
# steps = {0:'invalid', 1:'neutron_piece_selected', 2:'neutron_piece_dropped', 3:'player_piece_selected', 4:'player_piece_dropped'}
steps = {0:'invalid', 1:'neutron', 2:'player'}

# step result
# E: row_index_change = 0, col_index_change > 0
# NE: row_index_change < 0, col_index_change > 0
# N: row_index_change < 0, col_index_change = 0
# NW: row_index_change < 0, col_index_change < 0
# W: row_index_change = 0, col_index_change < 0
# SW: row_index_change > 0, col_index_change < 0
# S: row_index_change > 0, col_index_change = 0
# SE: row_index_change > 0, col_index_change > 0
move_direction_list = {'E', 'NE', 'N', 'NW', 'W', 'SW', 'S', 'SE'}
old_row_index_me = -1
old_col_index_me = -1
row_index_change_me = -1
col_index_change_me = -1
last_move_me = 'none'

old_row_index_another = -1
old_col_index_another = -1
row_index_change_another = -1
col_index_change_another = -1
last_move_another = 'none'


# game result
# start position: grid.row_0 is another player
# start position: grid.row_total_row is me
# if pieces[1], neutron is moved to grid.row_0,
# either 'you won' for me, or, 'you lost' for me, no other options
game_result = 'none'
draw_starting_board = False

print(grid)
print(grid_colours_old)
print('cell size = {}. image size = 64, image shift = {}'.format(w, image_shift))


# test example class
class DrawLines(Frame):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.master.title("Lines")
        self.pack(fill=BOTH, expand=1)

        canvas = Canvas(self)
        canvas.create_line(15, 25, 200, 25)
        canvas.create_line(300, 35, 300, 200, dash=(4, 2))
        canvas.create_line(55, 85, 155, 85, 105, 180, 55, 85)

        canvas.pack(fill=BOTH, expand=1)


# test example class
class DrawColourRects(Frame):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.master.title("ColourRects")
        self.pack(fill=BOTH, expand=1)

        canvas = Canvas(self)
        canvas.create_rectangle(30, 10, 120, 80,
                                outline="#fb0", fill="#fb0") #yellow
        canvas.create_rectangle(150, 10, 240, 80,
                                outline="#f50", fill="#f50") #red
        canvas.create_rectangle(270, 10, 370, 80,
                                outline="#05f", fill="#05f") #blue
        canvas.pack(fill=BOTH, expand=1)


class MyDialog(tkSimpleDialog.Dialog):

    def body(self, master):
        # Label is a module in tkinter
        Label(master, text="First:").grid(row=0)
        Label(master, text="Second:").grid(row=1)

        self.e1 = Entry(master)
        self.e2 = Entry(master)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        return self.e1  # initial focus

    def apply(self):
        first = int(self.e1.get())
        second = int(self.e2.get())
        print('First: {}, Second: {}'.format(first, second))


def DrawGameBoard(canvas, step_completed):
    global draw_starting_board
    # need to create as global, cannot be in the if cell_image != 'none' statement, because if not declear as global
    # as soon as PhotoImage is completed the reference is lost, and the cavas.create_image wouldn't find the reference
    global photo_Cross
    global photo_Circle
    global photo_Star
    photo_Cross=PhotoImage(file="Cross_s.png")
    photo_Circle = PhotoImage(file="Circle_s.png")
    photo_Star = PhotoImage(file="Star_s.png")
    canvas.delete('all')
    x, y = 0, 0
    for row in grid:
        for col in row:
            cell_colour = 'none'
            cell_image = 'none'
            if col == -1:
                cell_colour = DetermineCellColour(current_player, step_completed)
                cell_image = DetermineCellImage(current_player, step_completed)
            else:
                cell_colour = cell_colours['board']
                cell_image = 'none'
            # the following is for testing
            print('cell_colour={}, cell_image={}'.format(cell_colour,cell_image))
            if cell_colour != 'none':
                canvas.create_rectangle(x, y, x+w, y+w,
                                       outline="black",fill=cell_colour)
            if cell_image != 'none':
                # import os
                # print(os.path.exists("Cross.gif"))
                image_x = x + image_shift
                image_y = y + image_shift
                if cell_image.find("Cross") != -1:
                    canvas.create_image(image_x, image_y, anchor=NW, image=photo_Cross)
                elif cell_image.find("Circle") != -1:
                    canvas.create_image(image_x, image_y, anchor=NW, image=photo_Circle)
                elif cell_image.find("Star") != -1:
                    canvas.create_image(image_x, image_y, anchor=NW, image=photo_Star)
            x = x + w
        y = y + w
        x = 0
    canvas.pack(fill=BOTH, expand=1)


def DetermineCellColour(current_player, step_completed):
    step = steps[step_completed]
    if step == 'player':
        cell_colour = cell_colours[current_player]
    elif step == 'neutron':
        cell_colour = cell_colours['neutron']
    else:
        cell_colour = cell_colours[step]
    return cell_colour


def DetermineCellImage(current_player, step_completed):
    step = steps[step_completed]
    if step == 'player':
        cell_image = cell_images[current_player]
    elif step == 'neutron':
        cell_image = cell_images['neutron']
    else:
        cell_image = cell_images[step]
    return cell_image


def DetermineStepResults(current_row_index, old_row_index, current_col_index, old_col_index):
    row_index_change = current_row_index - old_row_index
    col_index_change = current_col_index - old_col_index
    if row_index_change == 0 and col_index_change > 0:
        step_result = 'E'
    elif row_index_change < 0 and col_index_change > 0:
        step_result = 'NE'
    elif row_index_change < 0 and col_index_change == 0:
        step_result = 'N'
    elif row_index_change < 0 and col_index_change < 0:
        step_result = 'NW'
    elif row_index_change == 0 and col_index_change < 0:
        step_result = 'W'
    elif row_index_change > 0 and col_index_change < 0:
        step_result = 'SW'
    elif row_index_change > 0 and col_index_change == 0:
        step_result = 'S'
    elif row_index_change > 0 and col_index_change > 0:
        step_result = 'SE'
    else:
        step_result = 'none'
    return step_result


def IsValidMove(current_row_index, old_row_index, current_col_index, old_col_index):
    # for checking not jumping pieces
    global grid_colours_old
    row_index_change = current_row_index - old_row_index
    col_index_change = current_col_index - old_col_index
    valid = True
    if row_index_change == 0 and col_index_change == 0:
        valid = False
        print('Each move of a piece must move to a new cell')
    else:
        valid = row_index_change == 0 or col_index_change or abs(row_index_change) == abs(col_index_change)
        if not valid:
            print('Each move of a piece must move that piece in one of the eight straight lines '
                  '(forward/back/left/right/4 diagonals)')
    # TODO, check not jumping over pieces, There is no capturing; pieces cannot exist on the same square of the board;
    #       pieces cannot jump over other pieces; pieces cannot go beyond the edge of the board.
    # TODO, check the move went as far as possible, Each move of a piece must move that piece as far as possible
    return valid


def CheckGameResult():
    global game_result
    # the following is just for testing - mimick game over - need to be removed once done
    game_result = 'you won'

    # TODO, check the gameboard, colour and position of the neutron piece and player piece, ref. kata website
    # for n in range[total_col]
    #    if grid


def ResetGame():
    global game_result
    # the following is just for testing - reset to keep the game going - need to be removed once done
    # print('game over {}, reset to start game'.format(game_result))
    d = MyDialog(root)
    print(d.result)
    game_result = 'none'

    # TODO: display pop up window say 'game over + game_results'


# test example callback
def motion(event):
    x, y = event.x, event.y
    print('{}, {}'.format(x/w, y/w))


root = Tk()
root.geometry("600x600")

frame = Frame(root, width=600, height=600, background="bisque")
frame.pack(fill=None, expand=True)
# the following example line doesn't seem to take any effect?
#frame.place(relx=.5, rely=.5, anchor="c")

canvas = Canvas(frame, width=600, height=600)
canvas.pack()

def click_me(event):
    global row_index_change_me
    global col_index_change_me
    global old_row_index_me
    global old_col_index_me
    global current_player
    global step_completed_me
    global step_completed_another
    global game_result
    your_turn = step_completed_another == 0 or step_completed_another == len(steps.keys())-1
    if game_result != 'none':
        ResetGame()
    elif not your_turn:
        print('the other player has not yet completed their move, please wait')
    else:
        x, y = event.x, event.y
        row_index = int(y/w)
        col_index = int(x/w)
        if row_index > total_row-1 or col_index > total_col-1:
            print('row index {} or col index {} out of range'.format(row_index,col_index))
        else:
            if IsValidMove(row_index, old_row_index_me, col_index, old_col_index_me):
                row_index_change_me = row_index - old_row_index_me
                col_index_change_me = col_index - old_col_index_me
                step_completed_me += 1
                # Note, the following line needs to be here to determin correct colour based on updated step_completed,
                # see DeterminCellColour
                current_player = 'me_computer'
                grid[row_index][col_index] = grid[row_index][col_index] * -1
                DrawGameBoard(canvas, step_completed_me)
                print('{} moved to row {}, col {}'.format(current_player,row_index, col_index))
                old_row_index_me = row_index
                old_col_index_me = col_index
        # now we have drawn the board, reset step_completed reached completion
        # Note, reset when euqal to 4 when the selected colour to be used
        if step_completed_me == 2: # 4:
            step_completed_me = 0
            CheckGameResult()


def click_another(event):
    global row_index_change_another
    global col_index_change_another
    global old_row_index_another
    global old_col_index_another
    global current_player
    global step_completed_me
    global step_completed_another
    global game_result
    your_turn = step_completed_me == 0 or step_completed_me == len(steps.keys())-1
    if game_result != 'none':
        ResetGame()
    elif not your_turn:
        print('the other player has not yet completed their move, please wait')
    else:
        x, y = event.x, event.y
        row_index = int(y/w)
        col_index = int(x/w)
        if row_index > total_row-1 or col_index > total_col-1:
            print('row index {} or col index {} out of range'.format(row_index,col_index))
        else:
            if IsValidMove(row_index, old_row_index_another, col_index, old_col_index_another):
                row_index_change_another = row_index - old_row_index_another
                col_index_change_another = col_index - old_col_index_another
                step_completed_another += 1
                # Note, the following line needs to be here to determin correct colour based on updated step_completed,
                # see DeterminCellColour
                current_player = 'another_computer'
                grid[row_index][col_index] = grid[row_index][col_index] * -1
                DrawGameBoard(canvas, step_completed_another)
                print('{} moved to row {}, col {}'.format(current_player, row_index, col_index))
                old_row_index_another = row_index
                old_col_index_another = col_index
        # now we have drawn the board, reset step_completed reached completion
        # Note, reset when euqal to 4 when the selected colour to be used
        if step_completed_another == 2: # 4:
            step_completed_another = 0
            CheckGameResult()


def main():
    # Note, to initialise the board, pass a hard coded zero to draw the board cell in blue
    DrawGameBoard(canvas, 0)
    canvas.bind('<Button-1>', click_me) # left mouse click is always me - can be human or computer
    canvas.bind('<Button-3>', click_another) # right mouse click is always another player - can be human or computer
    root.mainloop()


    # root = Tk()
    # #draw = DrawLines()
    # #draw = DrawColourRects()
    # #draw = DrawGameBoard()
    # #root.geometry("400x250+300+300")
    # root.geometry("800x600")
    # #root.bind('<Motion>', motion)
    # root.bind('<Button-1>', click)
    # root.mainloop()


    # root.geometry("500x900")
    # canvas = Canvas(root, width=550, height=820)
    # canvas.pack()
    # #png = PhotoImage(file = r'example.png') # Just an example
    # #canvas.create_image(0, 0, image = png, anchor = "nw")
    #
    # a = canvas.create_rectangle(50, 0, 100, 50, fill='red')
    # canvas.move(a, 20, 20)


if __name__ == '__main__':
    main()