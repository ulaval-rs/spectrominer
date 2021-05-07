import tkinter
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText


class PopUp(tkinter.Toplevel):

    def __init__(self, message: str):
        super(PopUp, self).__init__()
        self.geometry('800x600')

        self.wm_title('Message')

        btn = ttk.Button(self, text='Ok', command=self.destroy)
        btn.pack(anchor='e', side=tkinter.BOTTOM, padx=10, pady=10)

        text_box = ScrolledText(
            self,
            width=360,
            height=230,
            wrap=tkinter.WORD
        )
        text_box.pack(padx=10, pady=10, fill=tkinter.BOTH, expand=True)
        text_box.insert(tkinter.INSERT, message)
        text_box.config(state='disabled')
