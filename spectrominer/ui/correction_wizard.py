import tkinter
from tkinter import ttk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from spectrominer.ui.main_frame import MainFrame


class CorrectionWizard(tkinter.Toplevel):

    def __init__(self, parent: 'MainFrame'):
        super().__init__()
        self.parent = parent

        self.geometry('800x600')
        self.wm_title('Correction wizard')

        ttk.Label(self, text='Select control measures').place(x=20, y=20)
        self.table = ttk.Treeview(self, columns=[0], show='headings')
        self.table.heading(0, text='Analysis')
        self.scrollbar = ttk.Scrollbar()
        self.set_table()

        btn_ok = ttk.Button(self, text='Ok', command=self.correction_done)
        btn_ok.place(x=680, y=540, width=100, height=30)
        ttk.Checkbutton(self, text='Relative results', variable=self.parent.relative_result).place(x=540, y=540, width=125, height=30)

    def correction_done(self):
        self.parent.control_analyzes_indexes = []

        for row in self.table.selection():
            control_analysis_name = self.table.item(row)['values'][0]

            for analysis in self.parent.parser.get_analyzes():
                if analysis.name == control_analysis_name:
                    self.parent.control_analyzes_indexes.append(analysis.index)
                    break

        # If nothing have been selected
        if not self.parent.control_analyzes_indexes:
            return

        self.parent.experimental_correction_applied = True
        self.parent.btn_apply_experimental_corrections.config(text='Remove corrections with control measures')
        self.parent.recalculate_results()

        self.destroy()

    def set_table(self):
        del self.scrollbar
        self.scrollbar = ttk.Scrollbar(self)
        self.scrollbar.place(x=760, y=40, width=20, height=480)
        self.table.place(x=20, y=40, width=740, height=480)

        for analysis in self.parent.parser.get_analyzes():
            self.table.insert('', 'end', values=[analysis.name])

        self.scrollbar.config(command=self.table.yview)
        self.table.config(yscrollcommand=self.scrollbar.set)
