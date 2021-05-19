import tkinter

from spectrominer.ui.main_frame import MainFrame


class App(tkinter.Tk):

    def __init__(self):
        super().__init__()

        self.geometry('1400x900')
        self.winfo_toplevel().title('Spectrominer')  # Title
        MainFrame(self)


def start():
    app = App()
    app.mainloop()


if __name__ == '__main__':
    start()
