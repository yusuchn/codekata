#! python


run_requests_api = True
run_swagger_client_api = True
run_graphics = True

#region Test Requests Web API
if run_requests_api:
    import requests
    # NOTE, 9000 is battleShips port
    games = requests.get('http://10.44.37.98:9000/games/')
    print(games.json())


    gameids = requests.get('http://10.44.37.98:9000/games/140401855626936/')
    print(gameids.json())
#endregion


#region Test Swagger_Client Web API
if run_swagger_client_api:
    # default get start code from nsw yaml
    # from __future__ import print_function
    import sys  # for using print('function: {}'.format(sys._getframe().f_code.co_name))
    import time
    import swagger_client
    from swagger_client.rest import ApiException
    from swagger_client import configuration
    from pprint import pprint

    # create an instance of the API class
    # api_instance = swagger_client.DefaultApi(swagger_client.ApiClient(configuration))
    api_instance = swagger_client.DefaultApi(swagger_client.ApiClient())
    game_id = 'game_id_example'  # str | The ID of the game to return

    try:
        # Delete the given game
        api_instance.games_game_id_delete(game_id)
    except ApiException as e:
        print("Exception when calling DefaultApi->games_game_id_delete: %s\n" % e)
#endregion


#region Graphic Drawing
if run_graphics:
    from generaltools import *
    from MyDialog import MyDialog_DefineGameID

    # game board
    number_of_cells = 11
    w = 20
    font_szie = 12

    # default properties
    grid_texts_default = [
        ['none','A',    'B',    'C',    'D',    'E',    'F',    'G',    'H',    'I',    'J'],
        ['1',   'Hit',    'Hit',  'Hit',  'Hit',  'Hit',  'Hit',  'Hit',  'Hit',  'Hit',  'Hit'],
        ['2',   'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none'],
        ['3',   'none', 'none', 'Miss', 'none', 'none', 'none', 'none', 'none', 'none', 'none'],
        ['4',   'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none'],
        ['5',   'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none'],
        ['6',   'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none'],
        ['7',   'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none'],
        ['8',   'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none'],
        ['9',   'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none'],
        ['10',  '?',    '?',    '?',    '?',    '?',    '?',    '?',    '?',    '?',    '?']]
    grid_colours_default = [
        ['grey','grey', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey'],
        ['grey','white','white','white','white','white','white','white','white','white','white'],
        ['grey','white','white','white','white','white','white','white','white','white','white'],
        ['grey','white','white','white','white','white','white','white','white','white','white'],
        ['grey','white','white','white','white','white','white','white','white','white','white'],
        ['grey','white','white','white','white','white','white','white','white','white','white'],
        ['grey','white','white','white','white','white','white','white','white','white','white'],
        ['grey','white','white','white','white','white','white','white','white','white','white'],
        ['grey','white','white','white','white','white','white','white','white','white','white'],
        ['grey','white','white','white','white','white','white','white','white','white','white'],
        ['grey','white','white','white','white','white','white','white','white','white','white']]


    root = tkinter.Tk()
    root.wm_title("Embedding in Tk")
    root.withdraw()     # hide the little root window

    global_total_rows_in_plot = 1

    fig = Figure(figsize=(6, 3), dpi=100)  # set figure size

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

    def update_plot(number_of_cells, font_szie, w, total_rows_in_plot_param, fig_param, plot_canvas_param,
                    grid_texts_default_param, grid_colours_default_param, game):
        # player1_knowledge_param, player2_knowledge_param):
        grid_texts_1, grid_colours_1 = update_grid_text_and_color(
            grid_texts_default_param, grid_colours_default_param, game.player1.knowledge)
        grid_texts_2, grid_colours_2 = update_grid_text_and_color(
            grid_texts_default_param, grid_colours_default_param, game.player2.knowledge)
        image_1 = draw_game_board_on_image(number_of_cells, w, font_szie, grid_texts_1, grid_colours_1, draw_debug=False)
        image_title_1 = game.player1.name     # "player1"
        image_2 = draw_game_board_on_image(number_of_cells, w, font_szie, grid_texts_2, grid_colours_2, draw_debug=False)
        image_title_2 = game.player2.name     # "player2"
        pairs = dict()
        pairs[image_title_1] = image_1
        pairs[image_title_2] = image_2
        display_all_images_in_plot(total_rows_in_plot_param, pairs, fig_param, plot_canvas_param)


    def get_random_move_without_player_knowledge(int_list, chr_val_list):
        random.shuffle(int_list)
        # NOTE, always use first number in the shuffled int_list as index to grid number, i.e. 0
        # and use the last number in the shuffled int_list as the index to chr_val_list, i.e. len(int_list)-1
        # NOTE, numbers in int_list are one-based because top row is used for labelling,
        # when used for indexing chr_val_list, it has to be converted to zero-based
        grid_ref = chr(chr_val_list[int_list[len(int_list) - 1] - 1]) + str(int_list[0])
        return grid_ref


    def get_random_move_with_player_knowledge(int_list, chr_val_list, game):
        knowledge = list()
        if game.move == game.player1.name:
            knowledge = game.player1.knowledge
        elif game.move == game.player2.name:
            knowledge = game.player2.knowledge
        print('knowledge={}'.format(knowledge))
        candidate_hit_list = list()
        # NOTE, based on game.move, determine from which player's knoowledge to generate candidate hit list
        # and, based on that player's knowledge, if a cell already hit, ie. 'X', or Miss, i.e. '.'
        # don't add in the candidate hit list, only add if cell = '.'
        # The, randomly pick a hit from the candidate hit list
        for i in range(len(knowledge)):
            for j, char in enumerate(knowledge[i]):
                if char != '?':
                    continue

                letter = chr(chr_val_list[j])
                int_str = str(int_list[i])
                grid_ref = letter + int_str
                candidate_hit_list.append(grid_ref)
        print('candidate_hit_list={}'.format(candidate_hit_list))
        # NOTE, candidate_hit_list is already a list of grid_ref strings,
        # doesn't really matter which one to sue, so, always use the first one
        random.shuffle(candidate_hit_list)
        grid_ref = candidate_hit_list[0]
        print('randomly generated grid_ref={}'.format(grid_ref))
        return grid_ref


    display_players = True
    display_graphic = False
    with_player_knowledge = True


    def main():
        if display_players:
            # getting board information from the server
            # from __future__ import print_function
            import sys  # for using print('function: {}'.format(sys._getframe().f_code.co_name))
            import time
            import swagger_client
            from swagger_client.rest import ApiException
            from swagger_client import configuration
            from pprint import pprint
            import swagger_client
            from swagger_client.models import GetGame, Move, Player

            # default_game_id = '140401813622008'
            default_game_id = '140401813386912'
            d = MyDialog_DefineGameID(root, "Default Game ID: {}".format(default_game_id))
            game_id_def = d.result

            game_id = ''
            if game_id_def:
                game_id = game_id_def['game_id']
            else:
                game_id = default_game_id

            print('\ngame_id: {}\n'.format(game_id))

            api_instance_1 = swagger_client.DefaultApi(swagger_client.ApiClient())
            games = api_instance_1.games_get()  # 'http://10.44.37.98:9000/games/')
            print('games=\n{}'.format(games))
            game = api_instance_1.games_game_id_get(game_id)
            # drawing graphics based on information from the server
            # NOTE, number range from 1 to 11, as last 11 is excluded,
            # chr value range from A to K, as last K is exlcluded
            # and top row and left col are for labelling
            int_list = list(range(1, 11))
            chr_val_list = list(range(ord('A'), ord('K')))
            print('int_list={}, chr_val_list={}'.format(int_list, chr_val_list))
            grid_ref = ''
            while (game.winner == ""):
                game = api_instance_1.games_game_id_get(game_id)
                print('game=\n{}'.format(game))
                if with_player_knowledge:
                    grid_ref = get_random_move_with_player_knowledge(int_list, chr_val_list, game)
                else:
                    grid_ref = get_random_move_without_player_knowledge(int_list, chr_val_list)
                print('game_id={}, grid_ref={}'.format(game_id,grid_ref))

                move_result = api_instance_1.games_game_id_grid_ref_put(game_id, grid_ref, body=Move(game.move))
                print('grid_ref={}\nmove_result=\n{}'.format(grid_ref, move_result))
                game = api_instance_1.games_game_id_get(game_id)
                print('game_id={}\ngame=\n{}'.format(game_id, game))
                update_plot(number_of_cells, font_szie, w, global_total_rows_in_plot, fig, plotCanvas,
                            grid_texts_default, grid_colours_default, game)
        elif display_graphic:
            test_realtime_display_graphics(number_of_cells, font_szie, w, global_total_rows_in_plot, fig,
                                           plotCanvas,
                                           grid_texts_default, grid_colours_default, sleep_param=0.5)
        else:
            test_title_img_pairs_list = generate_test_title_img_pairs_list()
            print('test_title_img_pairs_list = \n{}'.format(test_title_img_pairs_list))

            # draw_game_board(number_of_cells, w, font_szie, grid_texts_default, grid_colours_default)
            test_realtime_display_group_of_images(global_total_rows_in_plot, test_title_img_pairs_list, fig, plotCanvas)

        root.mainloop()

    if __name__ == '__main__':
        main()
#endregion


