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


class MyDialog_GogenFiles(tkSimpleDialog.Dialog):

    def body(self, master):
        Label(master, text="Chose grid file and wordlist file", justify=LEFT).\
            grid(row=0, sticky=W, pady=5, padx=10)

        # for the label, no need for Entry reference, so combined Entry with Grid
        # for both e1 and btn_grid_file, Entry reference needed, so split into 2 lines
        # https://stackoverflow.com/questions/1101750/tkinter-attributeerror-nonetype-object-has-no-attribute-get
        self.grid_file = StringVar()
        Label(master, text="Puzzle file:").grid(row=1, sticky=W, pady=5, padx=10)
        self.e1 = Entry(master, textvariable=self.grid_file)
        self.e1.grid(row=1, column=1, padx=10)
        self.var_grid_file = IntVar()
        self.btn_grid_file = Button(master, text="...")
        self.btn_grid_file.grid(row=1, column=2, sticky=W, pady=5, padx=10)
        self.btn_grid_file.bind('<Button-1>', self.GridFileClick)

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

        self.grid_file = self.e1.get()
        self.wordlist_file = self.e2.get()
        print('Puzzle file: {} \nWordlist file: {} '.format(self.grid_file, self.wordlist_file))
        self.result = {'puzzle_file': self.grid_file, 'wordlist_file': self.wordlist_file}

    def validate(self):
        print('function: {}'.format(sys._getframe().f_code.co_name))

        self.apply()

        # import tkMessageBox
        import tkinter.messagebox as messageBox
        if (self.grid_file == '' or self.wordlist_file == ''):
            messageBox.showwarning('Error', 'please specify files contain the grid layout and the wordlist',
                                   icon="error")
            return 0

        return 1

    def GridFileClick(self, event):
        print('function: {}'.format(sys._getframe().f_code.co_name))

        self.var_grid_file = 1
        self.var_wordlist_file = 0

        self.SelectFile()

    def WordlistFileClick(self, event):
        print('function: {}'.format(sys._getframe().f_code.co_name))

        self.var_grid_file = 0
        self.var_wordlist_file = 1

        self.SelectFile()

    def SelectFile(self):
        print('function: {}'.format(sys._getframe().f_code.co_name))
        import os
        ROOT_DIR = os.path.abspath(os.curdir)
        GAME_DIR = ROOT_DIR + '/games/'
        filename = askopenfilename(initialdir=GAME_DIR,
                               filetypes =(("Text File", "*.txt"),("All Files","*.*")),
                               title = "Choose a file."
                               )
        print (filename)

        if self.var_grid_file == 1:
            self.grid_file.set(filename)
        elif self.var_wordlist_file == 1:
            self.wordlist_file.set(filename)

