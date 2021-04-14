import tkinter
from tkinter import filedialog, ttk
from typing import Optional

from spectrominer.parser import Parser
from spectrominer.ui.file_selector_frame import FileSelectorFrame


class MainFrame(ttk.Frame):

    def __init__(self, root: tkinter.Tk, **kw):
        super().__init__(root, **kw)
        self.root = root

        self.parser: Optional[Parser] = None

        # Widgets
        self.cb_molecule = ttk.Combobox(self.root, values=[], state='readonly')
        self.cb_molecule.bind('<<ComboboxSelected>>', self.molecule_has_been_selected)
        self.table = ttk.Treeview(self.root)
        self.scrollbar = ttk.Scrollbar()
        self._set_table()
        self.btn_export = ttk.Button(self.root, text='Export data', command=self.export_data)

        # Frames
        FileSelectorFrame(self, width=760, height=90).place(x=320, y=20)

        # Layout
        ttk.Label(self.root, text='Molecule:').place(x=320, y=130)
        self.cb_molecule.place(x=400, y=125, width=200, height=25)
        self.btn_export.place(x=1250, y=840, width=115, height=30)

    def molecule_has_been_selected(self, *_):
        analyzes = self.parser.get_analyzes_of_given_molecule(self.cb_molecule.get())
        nbr_of_M = len(analyzes[0].results[0].m_results)

        # Setting columns
        del self.table
        self.table = ttk.Treeview(self.root, columns=list(range(nbr_of_M + 1)), show='headings')
        self._set_table()

        self.table.heading(0, text='Analysis')
        self.table.column(0, minwidth=80)
        for i in range(nbr_of_M):
            self.table.heading(i + 1, text=f'M+{i}')
            self.table.column(i + 1, anchor='center', width=50)

        # Setting rows
        for analysis in analyzes:
            values = [analysis.name] + [f'{r.istd_resp_ratio:e}' for r in analysis.results[0].m_results]
            self.table.insert('', 'end', values=values)

    def export_data(self):
        with filedialog.asksaveasfile(mode='w', title='Select file', defaultextension='.csv') as file:
            analyzes = self.parser.get_analyzes_of_given_molecule(self.cb_molecule.get())
            nbr_of_M = len(analyzes[0].results[0].m_results)
            header = ['Analysis'] + [f'M+{i}' for i in range(nbr_of_M)]

            file.write(','.join(header) + '\n')

            for analysis in analyzes:
                file.write(
                    ','.join([analysis.name] + [str(r.istd_resp_ratio) for r in analysis.results[0].m_results]) + '\n'
                )

    def _set_table(self):
        del self.scrollbar
        self.scrollbar = ttk.Scrollbar(self.root)
        self.scrollbar.place(x=1350, y=160, width=20, height=660)
        self.table.place(x=50, y=160, width=1300, height=660)

        self.scrollbar.config(command=self.table.yview)
        self.table.config(yscrollcommand=self.scrollbar.set)