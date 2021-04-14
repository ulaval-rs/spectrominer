import tkinter
from typing import List, Optional

from spectrominer.parser import Parser
from spectrominer.parser.analysis import Analysis
from spectrominer.ui.main_frame import MainFrame


class App(tkinter.Tk):

    def __init__(self):
        super().__init__()

        self.geometry('800x600')
        self.winfo_toplevel().title('Spectrominer')  # Title
        MainFrame(self)


if __name__ == '__main__':
    app = App()
    app.mainloop()
