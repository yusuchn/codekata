#! python


run_requests_api = False
run_swagger_client_api = False
run_graphics = True

#region Test Requests Web API
if run_requests_api:
    import requests
    # NOTE, 9000 is battleShips port
    games = requests.get('http://10.44.37.98:9000/games/')
    print(games.json())


    # gameids = requests.get('http://10.44.37.98:9000/games/140401855626936/')
    # print(gameids.json())
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
    from MyDialog import MyDialog_JoinGameDlg, MyDialog_StartGameDlg

    # game board
    number_of_cells = 11
    w = 20
    font_szie = 12

    # default properties
    grid_texts_default = [
        ['none','1',    '2',    '3',    '4',    '5',    '6',    '7',    '8',    '9',    '10'],
        ['A',   'Hit',    'Hit',  'Hit',  'Hit',  'Hit',  'Hit',  'Hit',  'Hit',  'Hit',  'Hit'],
        ['B',   'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none'],
        ['C',   'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none'],
        ['D',   'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none'],
        ['E',   'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none'],
        ['F',   'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none'],
        ['G',   'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none'],
        ['H',   'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none'],
        ['I',   'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none'],
        ['J',  '?',    '?',    '?',    '?',    '?',    '?',    '?',    '?',    '?',    '?']]
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
        player1_is_winner = False
        player2_is_winner = False
        if game.winner == game.player1.name:
            player1_is_winner = True
            player2_is_winner = False
        elif game.winner == game.player2.name:
            player1_is_winner = False
            player2_is_winner = True
        # player1_knowledge_param, player2_knowledge_param):
        grid_texts_1, grid_colours_1 = update_grid_text_and_color(
            grid_texts_default_param, grid_colours_default_param, game.player1.knowledge)
        grid_texts_2, grid_colours_2 = update_grid_text_and_color(
            grid_texts_default_param, grid_colours_default_param, game.player2.knowledge)
        image_1 = draw_game_board_on_image(number_of_cells, w, font_szie, grid_texts_1, grid_colours_1,
                                           player1_is_winner, draw_debug=False)
        image_title_1 = game.player1.name     # "player1"
        image_2 = draw_game_board_on_image(number_of_cells, w, font_szie, grid_texts_2, grid_colours_2,
                                           player2_is_winner, draw_debug=False)
        image_title_2 = game.player2.name     # "player2"
        pairs = dict()
        pairs[image_title_1] = image_1
        pairs[image_title_2] = image_2
        display_all_images_in_plot(total_rows_in_plot_param, pairs, fig_param, plot_canvas_param)


    # def get_random_move_without_player_knowledge(int_list, chr_val_list):
    #     random.shuffle(int_list)
    #     # NOTE, always use first number in the shuffled int_list as index to grid number, i.e. 0
    #     # and use the last number in the shuffled int_list as the index to chr_val_list, i.e. len(int_list)-1
    #     # NOTE, numbers in int_list are one-based because top row is used for labelling,
    #     # when used for indexing chr_val_list, it has to be converted to zero-based
    #     grid_ref = chr(chr_val_list[int_list[len(int_list) - 1] - 1]) + str(int_list[0])
    #     return grid_ref


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

                letter = chr(chr_val_list[i])
                int_str = str(int_list[j])
                grid_ref = letter + int_str
                candidate_hit_list.append(grid_ref)
        print('candidate_hit_list={}'.format(candidate_hit_list))
        # NOTE, candidate_hit_list is already a list of grid_ref strings,
        # doesn't really matter which one to sue, so, always use the first one

        grid_ref = random.choice(candidate_hit_list)
        print('randomly generated grid_ref={}'.format(grid_ref))
        return grid_ref


    def get_stratigic_move_with_player_knowledge(int_list, chr_val_list, game):
        knowledge = list()
        if game.move == game.player1.name:
            knowledge = game.player1.knowledge
        elif game.move == game.player2.name:
            knowledge = game.player2.knowledge
        print('knowledge={}'.format(knowledge))
        candidate_hit_list = list()
        candicate_hit_list_adjacent_to_hit_cell = list()
        total_rows = len(knowledge)
        total_cols = len(knowledge[0])
        for i in range(len(knowledge)):
            for j, char in enumerate(knowledge[i]):
                if char == '.':
                    continue
                elif char == 'X':
                    # if encounter a hit cell, check the adjacent cells, if a "?", most likely part of a ship
                    # first check left and right
                    if (j-1) >= 0 and knowledge[i][j-1] == '?':
                        letter = chr(chr_val_list[i])
                        int_str = str(int_list[j-1])
                        grid_ref = letter + int_str
                        candicate_hit_list_adjacent_to_hit_cell.append(grid_ref)
                    elif (j+1) < total_cols and knowledge[i][j+1] == '?':
                        letter = chr(chr_val_list[i])
                        int_str = str(int_list[j+1])
                        grid_ref = letter + int_str
                        candicate_hit_list_adjacent_to_hit_cell.append(grid_ref)
                    # then check upper and lower, note,
                    # do not check upper left and upper right,
                    # nor, lower left and lower right
                    # ship doesn't go diagonal
                    if (i-1) >= 0 and knowledge[i-1][j] == '?':
                        letter = chr(chr_val_list[i-1])
                        int_str = str(int_list[j])
                        grid_ref = letter + int_str
                        candicate_hit_list_adjacent_to_hit_cell.append(grid_ref)
                    elif (i+1) < total_rows and knowledge[i+1][j] == '?':
                        letter = chr(chr_val_list[i+1])
                        int_str = str(int_list[j])
                        grid_ref = letter + int_str
                        candicate_hit_list_adjacent_to_hit_cell.append(grid_ref)
                else:
                    letter = chr(chr_val_list[i])
                    int_str = str(int_list[j])
                    grid_ref = letter + int_str
                    candidate_hit_list.append(grid_ref)
        print('candidate_hit_list={}\ncandicate_hit_list_adjacent_to_hit_cell={}'.format(
            candidate_hit_list, candicate_hit_list_adjacent_to_hit_cell))
        if (len(candicate_hit_list_adjacent_to_hit_cell) != 0):
            grid_ref = candicate_hit_list_adjacent_to_hit_cell[0]
            print('grid_ref={}'.format(grid_ref))
        else:
            grid_ref = random.choice(candidate_hit_list)
            print('no candidate adjacent to the hit cell, randomly generated grid_ref={}'.format(grid_ref))
        return grid_ref


    def get_initial_fleet_state(game):
        import copy

        fleet_state = list()
        for ship in game.fleet:
            ship_state = dict()
            ship_state['name'] = ship.name
            ship_state['size'] = ship.size
            ship_state['occupied_grid_refs'] = []
            print('ship_state = {}'.format(ship_state))
            fleet_state.append(ship_state)

        print('fleet_state = {}'.format(fleet_state))
        return fleet_state


    def get_stratigic_move_with_player_knowledge_enforce_non_adjacent_ships(int_list, chr_val_list, game,
                                                                            player1_fleet_state,
                                                                            player2_fleet_state):
        import copy
        knowledge = list()
        fleet_state = list()
        if game.move == game.player1.name:
            knowledge = game.player1.knowledge
            fleet_state = player1_fleet_state
        elif game.move == game.player2.name:
            knowledge = game.player2.knowledge
            fleet_state = player2_fleet_state
        print('knowledge={}'.format(knowledge))
        candidate_hit_list = list()
        candicate_hit_list_adjacent_to_hit_cell = list()
        total_rows = len(knowledge)
        total_cols = len(knowledge[0])
        for i in range(len(knowledge)):
            for j, char in enumerate(knowledge[i]):
                if char == '.':
                    continue
                elif char == 'X':
                    # if encounter a hit cell, check the adjacent cells, if a "?", most likely part of a ship
                    # first determine if to make a move, ie. check left and right, then up and down
                    # if the hit cell in a ship that already marked as destroyed, ie. in consecutive 'X's and with
                    # '.'s on either sides, close_end = True
                    add_left = False
                    add_right = False
                    add_upper = False
                    add_lower = False
                    horizontal_len = 1  # NOTE, starting from X so len already 1
                    vertical_len = 1  # NOTE, starting from X so len already 1

                    left_col = j
                    right_col = j
                    left_end = ''
                    right_end = ''
                    # while (0 <= left_col) and (knowledge[i][left_col] == 'X'):
                    #     left_col -= 1
                    #     horizontal_len += 1
                    # left_col += 1
                    for left_col in range(j-1, -1, -1):
                        if knowledge[i][left_col] == 'X':
                            horizontal_len += 1
                        else:
                            break
                    # NOTE, left_end can be 'X' if the hit cell reached the edge
                    left_end = knowledge[i][left_col]
                    for right_col in range(j+1, total_cols):
                        if knowledge[i][right_col] == 'X':
                            horizontal_len += 1
                        else:
                            break
                    right_end = knowledge[i][right_col]
                    # NOTE, only need to consider vertical if horizontal_len = 1
                    upper_row = i
                    lower_row = i
                    upper_end = ''
                    lower_end = ''
                    for upper_row in range(i-1, -1, -1):
                        if knowledge[upper_row][j] == 'X':
                            vertical_len += 1
                        else:
                            break
                    upper_end = knowledge[upper_row][j]
                    for lower_row in range(i+1, total_rows):
                        if knowledge[lower_row][j] == 'X':
                            vertical_len += 1
                        else:
                            break
                    lower_end = knowledge[lower_row][j]

                    # NOTE, in non-adjacent layout, if horizontal_len > vertical_len vertical_len = 1
                    if horizontal_len > vertical_len:
                        start_col = left_col
                        if left_end != 'X':
                            start_col = left_col + 1
                        end_col = right_col
                        if right_end != 'X':
                            end_col = right_col - 1
                        size = end_col - start_col + 1
                        letter = chr(chr_val_list[i])
                        int_str = str(int_list[start_col])
                        start_grid_ref = letter + int_str
                        int_str = str(int_list[end_col])
                        end_grid_ref = letter + int_str
                        fleet_state_copy = copy.deepcopy(fleet_state)
                        for item in fleet_state:
                            if item['size'] == size:
                                update_fleet_state = False
                                # need to consider left_end == '' and right_end == '', as 'X' cell can be at grid edge
                                if (left_end != '?' and right_end != '?' and
                                    len(item['occupied_grid_refs']) == 0):
                                    update_fleet_state = True
                                # check if all ships with a size greater than the current size been
                                # marksed as destroyed, if so, no need to make a move just mark the ship
                                # with the current size as destroyed in fleet_state, because even
                                # if one end has a '?', it's more likely be a miss cell
                                else:
                                    all_longer_ships_destroyed = True
                                    for item_copy in fleet_state_copy:
                                        if item_copy['size'] > size and len(item_copy['occupied_grid_refs']) == 0:
                                            all_longer_ships_destroyed = False
                                            break
                                    if all_longer_ships_destroyed:  # current continuous 'X' cells must be a ship
                                        update_fleet_state = True
                                    else:
                                        if left_end == '?':
                                            add_left = True
                                        if right_end == '?':
                                            add_right = True
                                if update_fleet_state:
                                    item['occupied_grid_refs'] = [start_grid_ref, end_grid_ref]
                                    break
                                    # do not break here, as there are two size 2. and two size 1 ships

                    # NOTE, in non-adjacent layout, if vertical_len > horizontal_len horizontal_len = 1
                    elif vertical_len > horizontal_len:
                        start_row = upper_row
                        if upper_end != 'X':
                            start_row = upper_row + 1
                        end_row = lower_row
                        if lower_end != 'X':
                            end_row = lower_row - 1
                        size = end_row - start_row + 1
                        letter = chr(chr_val_list[start_row])
                        int_str = str(int_list[j])
                        start_grid_ref = letter + int_str
                        letter = chr(chr_val_list[end_row])
                        end_grid_ref = letter + int_str
                        fleet_state_copy = copy.deepcopy(fleet_state)
                        for item in fleet_state:
                            if item['size'] == size:
                                update_fleet_state = False
                                # need to consider upper_end == '' and lower_end == '', as 'X' cell can be at grid edge
                                if (upper_end != '?' and lower_end != '?' and
                                    len(item['occupied_grid_refs']) == 0):
                                    update_fleet_state = True
                                    # do not break here, as there are two size 2. and two size 1 ships
                                # check if all ships with a size greater than the current size been
                                # marksed as destroyed, if so, no need to make a move just mark the ship
                                # with the current size as destroyed in fleet_state, because even
                                # if one end has a '?', it's more likely be a miss cell
                                else:
                                    all_longer_ships_destroyed = True
                                    for item_copy in fleet_state_copy:
                                        if item_copy['size'] > size and len(item_copy['occupied_grid_refs']) == 0:
                                            all_longer_ships_destroyed = False
                                            break
                                    if all_longer_ships_destroyed:
                                        update_fleet_state = True
                                    else:
                                        if upper_end == '?':
                                            add_upper = True
                                        if lower_end == '?':
                                            add_lower = True
                                if update_fleet_state:
                                    item['occupied_grid_refs'] = [start_grid_ref, end_grid_ref]
                                    break
                    # this is teh case horizontal_len == vertical_len = 1,
                    # in which case, all four adjacent cells added as candidates if a '?'
                    else:
                        if (j - 1) >= 0 and knowledge[i][j - 1] == '?':
                            add_left = True
                        elif (j + 1) < total_cols and knowledge[i][j + 1] == '?':
                            add_right = True
                        if (i - 1) >= 0 and knowledge[i - 1][j] == '?':
                            add_upper = True
                        elif (i + 1) < total_rows and knowledge[i + 1][j] == '?':
                            add_lower = True

                    if add_left:
                        letter = chr(chr_val_list[i])
                        int_str = str(int_list[left_col])
                        grid_ref_temp = letter + int_str
                        candicate_hit_list_adjacent_to_hit_cell.append(grid_ref_temp)
                    if add_right:
                        letter = chr(chr_val_list[i])
                        int_index = right_col
                        int_str = str(int_list[right_col])
                        grid_ref_temp = letter + int_str
                        candicate_hit_list_adjacent_to_hit_cell.append(grid_ref_temp)
                    if add_upper:
                        letter = chr(chr_val_list[upper_row])
                        int_str = str(int_list[j])
                        grid_ref_temp = letter + int_str
                        candicate_hit_list_adjacent_to_hit_cell.append(grid_ref_temp)
                    if add_lower:
                        letter = chr(chr_val_list[lower_row])
                        int_str = str(int_list[j])
                        grid_ref_temp = letter + int_str
                        candicate_hit_list_adjacent_to_hit_cell.append(grid_ref_temp)
                else:   # in this case, char == '?'
                    letter = chr(chr_val_list[i])
                    int_str = str(int_list[j])
                    grid_ref_temp = letter + int_str
                    candidate_hit_list.append(grid_ref_temp)

        print('candidate_hit_list={}\ncandicate_hit_list_adjacent_to_hit_cell={}'.format(
            candidate_hit_list, candicate_hit_list_adjacent_to_hit_cell))

        if (len(candicate_hit_list_adjacent_to_hit_cell) != 0):
            grid_ref = candicate_hit_list_adjacent_to_hit_cell[0]
            print('grid_ref={}'.format(grid_ref))
        else:
            grid_ref = random.choice(candidate_hit_list)
            print('no candidate adjacent to the hit cell, randomly generated grid_ref={}'.format(grid_ref))

        return grid_ref, player1_fleet_state, player2_fleet_state


    display_players = True
    display_graphic = True
    # start_new_game = False
    # play_with_another_player = False

    make_random_move = False
    enforce_non_adjacent_ships = True

    # root.withdraw()     # hide the little root window

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
            from swagger_client.models import GetGame, Move, Player, StartGame, GetPlayer
            import tkinter.messagebox as messageBox
            import copy

            # global start_new_game
            # global play_with_another_player
            start_new_game = False
            play_with_another_player = False
            # play_as_spacific_player = False

            default_server = '10.44.37.98:9000'
            game_id = ''
            player = ''
            server = ''
            player1 = ''
            player2 = ''

            api_instance_1 = swagger_client.DefaultApi(swagger_client.ApiClient())
            games = api_instance_1.games_get()  # 'http://10.44.37.98:9000/games/')
            print('games=\n{}'.format(games))

            if messageBox.askokcancel("BattleShips", "Start a new game?", icon="question"):
                # NOTE, the order of the params provide has to be in the same order as defined in
                # MyDialog_StartGameDlg.__init__
                start_new_game = True
                game_def = None
                d = MyDialog_StartGameDlg("Start a new game", default_server, player1, player2, root)
                game_def = d.result
                if not game_def:
                    messageBox.showerror('error', 'two player names are needed to start a new game', icon="error")
                else:
                    while game_def['start_another_game']:
                        d = MyDialog_StartGameDlg("Start a new game", default_server, player1, player2, root)
                        game_def = d.result
                        server = game_def['server']
                        player1 = game_def['player1']
                        player2 = game_def['player2']
                        print('starting a new game: server={}, player1={}, player2={}\n'.format(server, player1, player2))
                        # NOTE, api_instance_1.games_post returns a game_id object, then id method returns the string
                        game_id = api_instance_1.games_post(body=StartGame(player1, player2)).id
                        print('new game started, game_id={}'.format(game_id))

            if messageBox.askokcancel("BattleShips", "Play with another player?", icon="question"):
                play_with_another_player = True

            # NOTE, the order of the params provide has to be in the same order as defined in
            # MyDialog_JoinGameDlg.__init__
            if ((start_new_game and play_with_another_player) or not start_new_game):
                game_def = None
                # NOTE, if started a new game, game_id has a value, else, empty
                d = MyDialog_JoinGameDlg("Join a game", game_id, '',
                                         play_with_another_player, root)
                game_def = d.result
                # Rule I:
                # either game_id or player value must be provided, cannot be both empty
                # Rule II:
                # If play with another player, player name must be provided:
                # Rule III:
                # if player provided, it should be the self-player, and two scenarios entail:
                # 1. game_id provided, the player only plays with a specific game
                # 2. game_id not provided, the player plays multiple games that request the player's participation
                # Rules IV:
                # if player not provided, game_id must be provided, and the client plays both players
                if not game_def:
                    errorMsg = 'current setting: play_with_another_player = {}, ' \
                               ' some information missing'.format(play_with_another_player)
                    messageBox.showerror('error', errorMsg, icon="error")
                else:
                    game_id = game_def['game_id']
                    player = game_def['player']

            if (player == ''):
                player_str = 'play two players'
            else:
                player_str = player
            print('\njoined a game: game_id: {}, player: {}\n'.format(game_id, player_str))

            # drawing graphics based on information from the server
            # NOTE, number range from 1 to 11, as last 11 is excluded,
            # chr value range from A to K, as last K is exlcluded
            # and top row and left col are for labelling
            int_list = list(range(1, 11))
            chr_val_list = list(range(ord('A'), ord('K')))
            print('int_list={}, chr_val_list={}'.format(int_list, chr_val_list))
            while (True):   # keep the client alive checking if anyone requires a game
                game_ids = list()
                if game_id == '':
                    player_info = api_instance_1.players_name_get(player)
                    game_ids = player_info.games
                else:
                    game_ids.append(game_id)
                print('current player = {}, game_ids = {}'.format(player, game_ids))
                for this_game_id in game_ids:
                    print('this_game_id = {}, getting game information'.format(this_game_id))
                    game = api_instance_1.games_game_id_get(this_game_id)
                    print('game=\n{}'.format(game))
                    player1_fleet_state = get_initial_fleet_state(game)
                    player2_fleet_state = copy.deepcopy(player1_fleet_state)
                    if ((game.winner == '') and
                        (not play_with_another_player or (play_with_another_player and game.move == player))):
                        if make_random_move:
                            grid_ref = get_random_move_with_player_knowledge(int_list, chr_val_list, game)
                        elif enforce_non_adjacent_ships:
                            grid_ref, player1_fleet_state, player2_fleet_state = \
                                get_stratigic_move_with_player_knowledge_enforce_non_adjacent_ships(
                                    int_list, chr_val_list, game, player1_fleet_state, player2_fleet_state)
                        else:
                            grid_ref = get_stratigic_move_with_player_knowledge(int_list, chr_val_list, game)
                        print('this_game_id={}, grid_ref={}. game.move={}'.format(this_game_id,grid_ref, game.move))
                        move_result = api_instance_1.games_game_id_grid_ref_put(this_game_id, grid_ref, body=Move(game.move))
                        print('game.move={}\ngrid_ref={}\nmove_result=\n{}'.format(game.move, grid_ref, move_result))
                    game = api_instance_1.games_game_id_get(this_game_id)
                    print('this_game_id={}\ngame=\n{}'.format(this_game_id, game))
                    update_plot(number_of_cells, font_szie, w, global_total_rows_in_plot, fig, plotCanvas,
                                grid_texts_default, grid_colours_default, game)
        elif display_graphic:
            test_realtime_display_graphics(number_of_cells, font_szie, w,
                                           global_total_rows_in_plot, fig, plotCanvas,
                                           grid_texts_default, grid_colours_default, sleep_param=0.5)
        else:
            test_title_img_pairs_list = generate_test_title_img_pairs_list()
            print('test_title_img_pairs_list = \n{}'.format(test_title_img_pairs_list))
            test_realtime_display_group_of_images(global_total_rows_in_plot, test_title_img_pairs_list, fig, plotCanvas)

        root.mainloop()

    if __name__ == '__main__':
        main()
#endregion


