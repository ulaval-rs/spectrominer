import tkinter
from tkinter import ttk

from spectrominer.parser.file_selector_frame import FileSelectorFrame


class MainFrame(ttk.Frame):

    def __init__(self, root: tkinter.Tk, **kw):
        super().__init__(root, **kw)
        self.root = root

        FileSelectorFrame(self.root, width=760, height=90)

