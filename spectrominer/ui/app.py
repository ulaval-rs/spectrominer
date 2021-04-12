import tkinter
from tkinter import filedialog, ttk


class App(tkinter.Frame):

    def __init__(self, root: tkinter.Tk):
        super().__init__(root)
        self.root = root

        self.winfo_toplevel().title('Spectrominer')  # Title

        self.inline_filepath = tkinter.Entry(self.root)
        self.btn_browse = tkinter.Button(self.root, text='Browse', command=self.browse_file)

        self.inline_filepath.place(x=20, y=20, width=600, height=30)
        self.btn_browse.place(x=640, y=20, width=140, height=30)

        self.root.geometry('800x600')

    def browse_file(self):
        filepath = filedialog.askopenfilename(title='Browse')
        self.inline_filepath.delete(0, tkinter.END)
        self.inline_filepath.insert(0, filepath)
        print(filepath)


if __name__ == '__main__':
    root = tkinter.Tk()
    app = App(root)

    style = ttk.Style(root)
    style.theme_use('clam')

    app.mainloop()
