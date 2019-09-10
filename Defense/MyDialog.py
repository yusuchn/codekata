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

