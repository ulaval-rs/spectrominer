import tkinter
from tkinter import filedialog, ttk

from spectrominer.parser import Parser
from spectrominer.ui.popup import PopUp


class FileSelectorFrame(ttk.LabelFrame):

    def __init__(self, parent: tkinter.Tk, **kw):
        super().__init__(parent, text='Select file to parse', **kw)
        self.parent = parent

        # Widgets
        self.inline_filepath = ttk.Entry(self)
        self.combobox_delimiter = ttk.Combobox(self, values=[',', ';', ' '], state='readonly')
        self.combobox_delimiter.current(0)
        self.btn_browse = ttk.Button(self, text='Browse', command=self.browse_file)

        # Layout
        self.place(x=20, y=20)
        self.inline_filepath.place(x=20, y=25, width=500, height=30)
        ttk.Separator(self, orient='vertical').place(x=530, y=5, height=55)
        ttk.Label(self, text='Delimiter').place(x=540, y=5)
        self.combobox_delimiter.place(x=540, y=25, width=80, height=30)
        ttk.Separator(self, orient='vertical').place(x=630, y=5, height=55)
        self.btn_browse.place(x=640, y=25, width=100, height=30)

    def browse_file(self):
        filepath = filedialog.askopenfilename(title='Browse')
        if filepath == ():  # No file have been selected
            return

        try:
            self.parent.parser = Parser(filepath, delimiter=self.combobox_delimiter.get())
            self.inline_filepath.delete(0, tkinter.END)
            self.inline_filepath.insert(0, filepath)

            # TODO
            analysis = self.parent.parser.get_analysis_list()
            print(analysis)
        except Exception as e:
            PopUp(message=str(e))
