import tkinter
from tkinter import filedialog, ttk
from typing import List, Optional

import matplotlib.pyplot as plt

from spectrominer.corrections import apply_corrections
from spectrominer.parser import Parser
from spectrominer.parser.analysis import Analysis
from spectrominer.ui.file_selector_frame import FileSelectorFrame


class MainFrame(ttk.Frame):

    def __init__(self, root: tkinter.Tk, **kw):
        super().__init__(root, **kw)
        self.root = root

        self.parser: Optional[Parser] = None
        self.correction_applied: bool = False

        # Widgets
        self.cb_molecule = ttk.Combobox(self.root, values=[], state='readonly')
        self.cb_molecule.bind('<<ComboboxSelected>>', self.molecule_has_been_selected)
        self.btn_apply_corrections = ttk.Button(self.root, text='Apply corrections', command=self.apply_corrections)
        self.table = ttk.Treeview(self.root)
        self.scrollbar = ttk.Scrollbar()
        self._set_table()
        self.cb_m_value = ttk.Combobox(self.root, values=[], state='readonly')
        self.btn_show_histogram = ttk.Button(self.root, text='Show histogram', command=self.show_histogram)
        self.btn_export = ttk.Button(self.root, text='Export data', command=self.export_data)

        # Frames
        FileSelectorFrame(self, width=760, height=90).place(x=320, y=20)

        # Layout
        ttk.Label(self.root, text='Molecule:').place(x=320, y=130)
        self.cb_molecule.place(x=400, y=125, width=200, height=25)
        self.btn_apply_corrections.place(x=880, y=125, width=200, height=25)
        self.cb_m_value.place(x=50, y=840, width=115, height=30)
        self.btn_show_histogram.place(x=200, y=840, width=115, height=30)
        self.btn_export.place(x=1250, y=840, width=115, height=30)

    def molecule_has_been_selected(self, *_):
        analyzes = self._get_data()
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

        # Showing available M values that can be plot
        self.cb_m_value.config(values=[f'M+{i}' for i in range(nbr_of_M)])
        self.cb_m_value.current(0)

    def apply_corrections(self):
        if not self.correction_applied:
            self.correction_applied = True
            self.btn_apply_corrections.config(text='Remove corrections')

        else:
            self.correction_applied = False
            self.btn_apply_corrections.config(text='Apply corrections')

        # Reloading data
        if self.cb_molecule.get() != '':
            self.molecule_has_been_selected()

    def show_histogram(self):
        analyzes = self._get_data()
        molecule_name = f'{analyzes[0].results[0].name} {self.cb_m_value.get()}'
        analysis_names, analysis_results = [], []

        for analysis in analyzes:
            for m_result in analysis.results[0].m_results:
                if f'M+{m_result.m_number}' == self.cb_m_value.get():
                    analysis_names.append(analysis.name)
                    analysis_results.append(m_result.istd_resp_ratio)
                    continue

        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111)
        ax.bar(analysis_names, analysis_results)
        ax.set_xticklabels(analysis_names, rotation=45, ha='right')

        plt.title(molecule_name)
        plt.tight_layout()
        plt.show()

    def export_data(self):
        with filedialog.asksaveasfile(mode='w', title='Select file', defaultextension='.csv') as file:
            analyzes = self._get_data()
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

        # Actions on table
        self.table.bind("<Delete>", self._delete_row)

    def _get_data(self) -> List[Analysis]:
        analyzes = self.parser.get_analyzes_of_given_molecule(self.cb_molecule.get())

        if not self.correction_applied:
            return analyzes

        # Applying correction to analysis
        for analysis in analyzes:
            analysis.results = [apply_corrections(molecule_results) for molecule_results in analysis.results]

        return analyzes

    def _delete_row(self, event):
        for row in self.table.selection():
            self.table.delete(row)
