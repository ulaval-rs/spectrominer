import tkinter
from tkinter import ttk


class PopUp(tkinter.Toplevel):

    def __init__(self, message: str):
        super(PopUp, self).__init__()
        self.geometry('400x300')

        self.wm_title('Message')

        label = ttk.Label(self, text=message, anchor=tkinter.N)
        label.place(x=20, y=10, width=360, height=230)

        btn = ttk.Button(self, text='Ok', command=self.destroy)
        btn.place(x=320, y=250, width=60, height=30)
