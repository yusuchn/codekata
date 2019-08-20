from tkinter import *
import tkSimpleDialog

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


class MyDialog_ChoosePlayer(tkSimpleDialog.Dialog):

    def body(self, master):
        # Label is a module in tkinter
        # Label(master, text="me_human:").grid(row=0)
        # Label(master, text="me_computer:").grid(row=1)
        # Label(master, text="another_human:").grid(row=0)
        # Label(master, text="another_computer:").grid(row=1)
        # Label(master, text="another_remote:").grid(row=0)

        Label(master, text="Choose two players out of the following options\n"
                           "please put play order in the right column,\n"
                           "0-first, 1-second:", justify=LEFT).\
            grid(row=0, sticky=W, pady=5, padx=10)
        # self.e0 = Entry(master)
        # self.e0.grid(row=0, column=1)
        # self.e0.configure(text='play order: 0-first, 1-second')

        self.var_me_human = IntVar()
        self.var_me_human_string = StringVar()
        self.cb_me_human = Checkbutton(master, text="me_human", variable = self.var_me_human).\
            grid(row=1, sticky=W, pady=5, padx=10)
        self.e1 = Entry(master)
        self.e1.grid(row=1, column=1, padx=10)

        self.var_me_computer = IntVar()
        self.var_me_computer_string = StringVar()
        self.cb_me_computer = Checkbutton(master, text="me_computer", variable = self.var_me_computer).\
            grid(row=2, sticky=W, pady=5, padx=10)
        self.e2 = Entry(master)
        self.e2.grid(row=2, column=1, padx=10)

        self.var_another_human = IntVar()
        self.var_another_human_string = StringVar()
        self.cb_another_human = Checkbutton(master, text="another_human", variable = self.var_another_human).\
            grid(row=3, sticky=W, pady=5, padx=10)
        self.e3 = Entry(master)
        self.e3.grid(row=3, column=1, padx=10)

        self.var_another_computer = IntVar()
        self.var_another_computer_string = StringVar()
        self.cb_another_computer = Checkbutton(master, text="another_computer", variable = self.var_another_computer).\
            grid(row=4, sticky=W, pady=5, padx=10)
        self.e4 = Entry(master)
        self.e4.grid(row=4, column=1, padx=10)

        self.var_another_remote = IntVar()
        self.var_another_remote_string = StringVar()
        self.cb_another_remote = Checkbutton(master, text="another_remote", variable = self.var_another_remote).\
            grid(row=5, sticky=W, pady=5, padx=10)
        self.e5 = Entry(master)
        self.e5.grid(row=5, column=1, padx=10)

        self.total_selected_players = IntVar
        self.total_selected_me_players = IntVar
        self.total_selected_another_players = IntVar

        return self.cb_me_human     # initial focus

    def apply(self):
        print('function: {}'.format(sys._getframe().f_code.co_name))

        self.total_selected_players = 0
        self.total_selected_me_players = 0
        self.total_selected_another_players = 0

        selected_player_list = {}
        if self.var_me_human.get():
            self.var_me_human_string = 'selected'
            play_order = 'none_e1'
            if self.e1.get():
                play_order = self.e1.get()
            selected_player_list[play_order] = 'me_human'
            self.total_selected_players += 1
            self.total_selected_me_players += 1
        else:
            self.var_me_human_string = 'not selected'

        if self.var_me_computer.get():
            self.var_me_computer_string = 'selected'
            play_order = 'none_e2'
            if self.e2.get():
                play_order = self.e2.get()
            selected_player_list[play_order] = 'me_computer'
            self.total_selected_players += 1
            self.total_selected_me_players += 1
        else:
            self.var_me_computer_string = 'not selected'

        if self.var_another_human.get():
            self.var_another_human_string = 'selected'
            play_order = 'none_e3'
            if self.e3.get():
                play_order = self.e3.get()
            selected_player_list[play_order] = 'another_human'
            self.total_selected_players += 1
            self.total_selected_another_players += 1
        else:
            self.var_another_human_string = 'not selected'

        if self.var_another_computer.get():
            self.var_another_computer_string = 'selected'
            play_order = 'none_e4'
            if self.e4.get():
                play_order = self.e4.get()
            selected_player_list[play_order] = 'another_computer'
            self.total_selected_players += 1
            self.total_selected_another_players += 1
        else:
            self.var_another_computer_string = 'not selected'

        if self.var_another_remote.get():
            self.var_another_remote_string = 'selected'
            play_order = 'none_e5'
            if self.e5.get():
                play_order = self.e5.get()
            selected_player_list[play_order] = 'another_remote'
            self.total_selected_players += 1
            self.total_selected_another_players += 1
        else:
            self.var_another_remote_string = 'not selected'

        print('player me_human is {}, player me_computer is {}, '
              'player another_human is {}, player another_computer is {}, '
              'player another_remote is {}'.format(
                self.var_me_human_string, self.var_me_computer_string,
                self.var_another_human_string, self.var_another_computer_string,
                self.var_another_remote_string
        ))
        self.result = selected_player_list

    def validate(self):
        print('function: {}'.format(sys._getframe().f_code.co_name))
        self.apply()

        # self.total_selected_players = 0
        # self.total_selected_me_players = 0
        # self.total_selected_another_players = 0
        #
        # if self.var_me_human.get():
        #     self.total_selected_players += 1
        #     self.total_selected_me_players += 1
        #
        # if self.var_me_computer.get():
        #     self.total_selected_players += 1
        #     self.total_selected_me_players += 1
        #
        # if self.var_another_human.get():
        #     self.total_selected_players += 1
        #     self.total_selected_another_players += 1
        #
        # if self.var_another_computer.get():
        #     self.total_selected_players += 1
        #     self.total_selected_another_players += 1
        #
        # if self.var_another_remote.get():
        #     self.total_selected_players += 1
        #     self.total_selected_another_players += 1

        print('self.var_me_human = {}, self.var_me_computer = {}, self.var_another_human = {}, '
              'self.var_another_computer = {}, self.var_another_remote = {}, '
              'self.total_selected_players = {}, self.tatal_selected_me_players = {}, '
              'self.total_selected_another_players = {}'.format(
                self.var_me_human, self.var_me_computer, self.var_another_human,
                self.var_another_computer, self.var_another_remote, self.total_selected_players,
                self.total_selected_me_players, self.total_selected_another_players
        ))

        # import tkMessageBox
        import tkinter.messagebox as messageBox
        if (self.total_selected_players == 2 and
            self.total_selected_me_players == 1 and
            self.total_selected_another_players == 1):
            for key in self.result.keys():
                if key.find('none_') != -1:
                    messageBox.showwarning('Error', 'please specify player order: 0 first, 1 second', icon="error")
                    return 0
            return 1
        else:
            messageBox.showwarning("Error",
                "Only two players are allowed, you must select one me player and one another player,\n"
                "Please try again",
                icon="error")
            return 0


