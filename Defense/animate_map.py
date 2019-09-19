from Defense import *
from MyDialog import *
from plot_maps import *


root = Tk()
# root.withdraw()     # hide the little root window
root.wm_title("Embedding in Tk")

# fig, axes = plt.subplots(nrows=1, ncols=1)
# ax = axes.ravel()

fig = Figure(figsize=(3, 3), dpi=100)  # this allows specify figure size
axes = fig.add_subplot(111)

plotCanvas = FigureCanvasTkAgg(fig, master=root)  # a tk.DrawingArea.
plotCanvas.draw()
plotCanvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

color = "grey"  # "#ffffff"
toolbar = NavigationToolbar2Tk(plotCanvas, root)
toolbar.config(background=color)
toolbar._message_label.config(background=color)
toolbar.update()  # toolbar.pack(side=BOTTOM)
plotCanvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)


def on_key_press(event):
    print("you pressed {}".format(event.key))
    key_press_handler(event, plotCanvas, toolbar)


plotCanvas.mpl_connect("key_press_event", on_key_press)


def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate


button = tkinter.Button(master=root, text="Quit", command=_quit)
button.pack(side=tkinter.BOTTOM)

def main():
    d = MyDialog_MapFiles(root, "Map Files")
    map_files = d.result

    if map_files:
        print('\nmap files are: {}\n'.format(map_files))

        # load data from files
        check_grass_cell_between_neighbors = True
        load_success, letter_list, staged_cost_list, staged_image_list = \
            generate_map_data(map_files, check_grass_cell_between_neighbors)
        print('letter_list = \n{}\nstaged_cost_list = \n{}\nstaged_cost_list = \n{}'.format(
            letter_list, staged_cost_list, staged_image_list))

        # display_map_images(staged_image_list, staged_cost_list)
        realtime_display_animated_map_images(staged_image_list, staged_cost_list, plotCanvas, axes)

    root.mainloop()

if __name__ == '__main__':
    main()





