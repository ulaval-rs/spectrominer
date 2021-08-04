import tkinter

from spectrominer.ui.main_frame import MainFrame


class GUIApp(tkinter.Tk):

    def __init__(self):
        super().__init__()

        self.winfo_toplevel().title('Spectrominer')  # Title
        mainframe = MainFrame(self)
        self.geometry(f'1400x{230 + mainframe.table_height}')


def start():
    app = GUIApp()
    app.mainloop()
