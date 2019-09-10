from Defense import *
from MyDialog import *
from plot_maps import *


root = Tk()
root.withdraw()     # hide the little root window


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

        display_map_images(staged_image_list, staged_cost_list)


    root.mainloop()


if __name__ == '__main__':
    main()





