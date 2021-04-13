import tkinter
from tkinter import filedialog, ttk
from typing import Optional

from spectrominer.parser import Parser
from spectrominer.ui.popup import PopUp


class App(tkinter.Frame):

    def __init__(self, root: tkinter.Tk):
        self.parser: Optional[Parser] = None
        super().__init__(root)
        self.root = root

        ttk.Style(self.root).theme_use('clam')

        self.root.geometry('800x600')
        self.winfo_toplevel().title('Spectrominer')  # Title

        self.label_browse_file = ttk.Label(self.root, text='Select a file')
        self.inline_filepath = ttk.Entry(self.root)
        self.btn_browse = ttk.Button(self.root, text='Browse', command=self.browse_file)

        self.label_browse_file.place(x=20, y=20)
        self.inline_filepath.place(x=20, y=50, width=600, height=30)
        self.btn_browse.place(x=640, y=50, width=140, height=30)

    def browse_file(self):
        filepath = filedialog.askopenfilename(title='Browse')
        try:
            self.parser = Parser(filepath)
            self.inline_filepath.delete(0, tkinter.END)
            self.inline_filepath.insert(0, filepath)
        except Exception as e:
            PopUp(self.root, message=str(e))


if __name__ == '__main__':
    root = tkinter.Tk()
    app = App(root)

    app.mainloop()
