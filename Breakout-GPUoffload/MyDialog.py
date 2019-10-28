from tkinter import *
import tkSimpleDialog
from tkinter.filedialog import askopenfilename
import tkinter.messagebox as messageBox


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


class MyDialog_GameFiles(tkSimpleDialog.Dialog):

    def body(self, master):
        Label(master, text="Chose puzzle file and wordlist file", justify=LEFT).\
            grid(row=0, sticky=W, pady=5, padx=10)

        # for the label, no need for Entry reference, so combined Entry with Grid
        # for both e1 and btn_puzzle_file, Entry reference needed, so split into 2 lines
        # https://stackoverflow.com/questions/1101750/tkinter-attributeerror-nonetype-object-has-no-attribute-get
        self.puzzle_file = StringVar()
        Label(master, text="Puzzle file:").grid(row=1, sticky=W, pady=5, padx=10)
        self.e1 = Entry(master, textvariable=self.puzzle_file)
        self.e1.grid(row=1, column=1, padx=10)
        self.var_puzzle_file = IntVar()
        self.btn_puzzle_file = Button(master, text="...")
        self.btn_puzzle_file.grid(row=1, column=2, sticky=W, pady=5, padx=10)
        self.btn_puzzle_file.bind('<Button-1>', self.PuzzleFileClick)

        self.wordlist_file = StringVar()
        Label(master, text="Wordlist file:").grid(row=2, sticky=W, pady=5, padx=10)
        self.e2 = Entry(master, textvariable=self.wordlist_file)
        self.e2.grid(row=2, column=1, padx=10)
        self.var_wordlist_file = IntVar()
        self.btn_wordlist_file = Button(master, text="...")
        self.btn_wordlist_file.grid(row=2, column=2, sticky=W, pady=5, padx=10)
        self.btn_wordlist_file.bind('<Button-1>', self.WordlistFileClick)

        return self.e1     # initial focus

    def apply(self):
        print('function: {}'.format(sys._getframe().f_code.co_name))

        self.puzzle_file = self.e1.get()
        self.wordlist_file = self.e2.get()
        print('Puzzle file: {} \nWordlist file: {} '.format(self.puzzle_file, self.wordlist_file))
        self.result = {'puzzle_file': self.puzzle_file, 'wordlist_file': self.wordlist_file}

    def validate(self):
        print('function: {}'.format(sys._getframe().f_code.co_name))

        self.apply()

        # import tkMessageBox
        import tkinter.messagebox as messageBox
        if (self.puzzle_file == '' or self.wordlist_file == ''):
            messageBox.showwarning('Error', 'please specify files contain the grid layout and the wordlist',
                                   icon="error")
            return 0

        return 1

    def PuzzleFileClick(self, event):
        print('function: {}'.format(sys._getframe().f_code.co_name))

        self.var_puzzle_file = 1
        self.var_wordlist_file = 0

        self.SelectFile()

    def WordlistFileClick(self, event):
        print('function: {}'.format(sys._getframe().f_code.co_name))

        self.var_puzzle_file = 0
        self.var_wordlist_file = 1

        self.SelectFile()

    def SelectFile(self):
        print('function: {}'.format(sys._getframe().f_code.co_name))
        import os
        ROOT_DIR = os.path.abspath(os.curdir)
        GAME_DIR = ROOT_DIR     # + '/games/'
        filename = askopenfilename(initialdir=GAME_DIR,
                               filetypes =(("All Files","*.*"),
                                           ("Text File", "*.txt"),
                                           ("JSON File", "*.json")),
                               title = "Choose a file."
                               )
        print (filename)

        if self.var_puzzle_file == 1:
            self.puzzle_file.set(filename)
        elif self.var_wordlist_file == 1:
            self.wordlist_file.set(filename)


class MyDialog_MapFiles(tkSimpleDialog.Dialog):

    def body(self, master):
        Label(master, text="Chose map text file and map image file", justify=LEFT).\
            grid(row=0, sticky=W, pady=5, padx=10)

        # for the label, no need for Entry reference, so combined Entry with Grid
        # for both e1 and btn_puzzle_file, Entry reference needed, so split into 2 lines
        # https://stackoverflow.com/questions/1101750/tkinter-attributeerror-nonetype-object-has-no-attribute-get
        self.text_file = StringVar()
        Label(master, text="Text file:").grid(row=1, sticky=W, pady=5, padx=10)
        self.e1 = Entry(master, textvariable=self.text_file)
        self.e1.grid(row=1, column=1, padx=10)
        self.var_text_file = IntVar()
        self.btn_text_file = Button(master, text="...")
        self.btn_text_file.grid(row=1, column=2, sticky=W, pady=5, padx=10)
        self.btn_text_file.bind('<Button-1>', self.TextFileClick)

        self.image_file = StringVar()
        Label(master, text="Image file:").grid(row=2, sticky=W, pady=5, padx=10)
        self.e2 = Entry(master, textvariable=self.image_file)
        self.e2.grid(row=2, column=1, padx=10)
        self.var_image_file = IntVar()
        self.btn_image_file = Button(master, text="...")
        self.btn_image_file.grid(row=2, column=2, sticky=W, pady=5, padx=10)
        self.btn_image_file.bind('<Button-1>', self.ImageFileClick)

        return self.e1     # initial focus

    def apply(self):
        print('function: {}'.format(sys._getframe().f_code.co_name))

        self.text_file = self.e1.get()
        self.image_file = self.e2.get()
        print('Text file: {} \nImage file: {} '.format(self.text_file, self.image_file))
        self.result = {'text_file': self.text_file, 'image_file': self.image_file}

    def validate(self):
        print('function: {}'.format(sys._getframe().f_code.co_name))

        self.apply()

        # import tkMessageBox
        import tkinter.messagebox as messageBox
        if (self.text_file == '' or self.image_file == ''):
            messageBox.showwarning('Error', 'please specify map text file and map image file',
                                   icon="error")
            return 0

        return 1

    def TextFileClick(self, event):
        print('function: {}'.format(sys._getframe().f_code.co_name))

        self.var_text_file = 1
        self.var_image_file = 0

        self.SelectFile()

    def ImageFileClick(self, event):
        print('function: {}'.format(sys._getframe().f_code.co_name))

        self.var_text_file = 0
        self.var_image_file = 1

        self.SelectFile()

    def SelectFile(self):
        print('function: {}'.format(sys._getframe().f_code.co_name))
        import os
        ROOT_DIR = os.path.abspath(os.curdir)
        GAME_DIR = ROOT_DIR     # + '/games/'
        filename = askopenfilename(initialdir=GAME_DIR,
                               filetypes =(("All Files","*.*"),
                                           ("Text File", "*.txt"),
                                           ("PNG File", "*.png"),
                                           ("JPG File", "*.jpg")),
                               title = "Choose a file."
                               )
        print (filename)

        if self.var_text_file == 1:
            self.text_file.set(filename)
        elif self.var_image_file == 1:
            self.image_file.set(filename)


class MyDialog_JoinGameDlg(tkSimpleDialog.Dialog):

    def __init__(self, title,
                 default_game_id = None,
                 default_player = None,
                 play_with_another_player = None,
                 parent = None):

        if not parent:
            import Tkinter
            parent = Tkinter._default_root

        self.default_game_id = default_game_id
        self.default_player = default_player
        self.play_with_another_player = play_with_another_player

        super().__init__(parent, title)


    def body(self, master):
        Label(master, text="Chose a Game to join", justify=LEFT).\
            grid(row=0, sticky=W, pady=5, padx=10)

        # for the label, no need for Entry reference, so combined Entry with Grid
        # for both e1, Entry reference needed, so split into 2 lines
        # https://stackoverflow.com/questions/1101750/tkinter-attributeerror-nonetype-object-has-no-attribute-get
        self.game_id = StringVar()
        Label(master, text="game_id:").grid(row=1, sticky=W, pady=5, padx=10)
        self.e1 = Entry(master, textvariable=self.game_id)
        self.e1.grid(row=1, column=1, padx=10)
        self.game_id.set(self.default_game_id)  # to display the default value

        self.player = StringVar()
        Label(master, text="player:").grid(row=2, sticky=W, pady=5, padx=10)
        self.e2 = Entry(master, textvariable=self.player)
        self.e2.grid(row=2, column=1, padx=10)
        self.player.set(self.default_player)  # to display the default value

        return self.e1     # initial focus

    def apply(self):
        # print('function: {}'.format(sys._getframe().f_code.co_name))

        self.game_id = self.e1.get()
        self.player = self.e2.get()
        self.result = {'game_id': self.game_id, 'player': self.player}

    def validate(self):
        # print('function: {}'.format(sys._getframe().f_code.co_name))

        self.apply()

        import tkinter.messagebox as messageBox
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
        if ((self.game_id == '' and self.player == '') or
            (self.play_with_another_player and (self.player == '')) or
            (not self.play_with_another_player and (self.game_id == ''))):
            self.result = None
            messageBox.showerror('error', 'play_with_another_player = {}, some information missing'.format(
                self.play_with_another_player), icon="error")
            return 0
        return 1


class MyDialog_StartGameDlg(tkSimpleDialog.Dialog):

    def __init__(self, title,
                 default_server = None,
                 default_player1 = None,
                 default_player2 = None,
                 parent = None):

        if not parent:
            import Tkinter
            parent = Tkinter._default_root

        self.default_server = default_server
        self.default_player1 = default_player1
        self.default_player2 = default_player2

        self.start_another_game = False

        super().__init__(parent, title)


    def body(self, master):
        Label(master, text="Start a game", justify=LEFT).\
            grid(row=0, sticky=W, pady=5, padx=10)

        # for the label, no need for Entry reference, so combined Entry with Grid
        # for both e1, Entry reference needed, so split into 2 lines
        # https://stackoverflow.com/questions/1101750/tkinter-attributeerror-nonetype-object-has-no-attribute-get

        self.server = StringVar()
        Label(master, text="server:").grid(row=1, sticky=W, pady=5, padx=10)
        self.e1 = Entry(master, textvariable=self.server)
        self.e1.grid(row=1, column=1, padx=10)
        self.server.set(self.default_server)  # to display the default value

        self.player1 = StringVar()
        Label(master, text="player1:").grid(row=2, sticky=W, pady=5, padx=10)
        self.e2 = Entry(master, textvariable=self.player1)
        self.e2.grid(row=2, column=1, padx=10)
        self.player1.set(self.default_player1)  # to display the default value

        self.player2 = StringVar()
        Label(master, text="player2:").grid(row=3, sticky=W, pady=5, padx=10)
        self.e3 = Entry(master, textvariable=self.player2)
        self.e3.grid(row=3, column=1, padx=10)
        self.player2.set(self.default_player2)  # to display the default value

        return self.e1     # initial focus

    def apply(self):
        # print('function: {}'.format(sys._getframe().f_code.co_name))

        self.server = self.e1.get()
        self.player1 = self.e2.get()
        self.player2 = self.e3.get()

        import tkinter.messagebox as messageBox
        if messageBox.askokcancel('Question', 'start another game?', icon="question"):
            self.start_another_game = True
        else:
            self.start_another_game = True

        self.result = {'server': self.server, 'player1': self.player1, 'player2': self.player2,
                       'start_another_game': self.start_another_game}

    def validate(self):
        # print('function: {}'.format(sys._getframe().f_code.co_name))

        # in base class tkSimpleDialog.Dialog, when ok button clicked, validate is called first
        # followed by apply, and in this dialog the variable values are updated with the input
        # in the UI, so no need to call self.apply()
        # self.apply()

        import tkinter.messagebox as messageBox
        if (self.server == '' or self.player1 == '' or self.player2 == ''):
            self.result = None
            messageBox.showerror('error', 'two player names are needed to start a new game', icon="error")
            return 0
        return 1


