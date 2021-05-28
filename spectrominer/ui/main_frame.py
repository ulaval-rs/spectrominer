import tkinter
from tkinter import filedialog, ttk
from typing import List, Optional

import matplotlib.pyplot as plt

from spectrominer.corrections.experimental import apply_experimental_corrections
from spectrominer.parser import Parser
from spectrominer.parser.analysis import Analysis
from spectrominer.ui.correction_wizard import CorrectionWizard
from spectrominer.ui.file_selector_frame import FileSelectorFrame


class MainFrame(ttk.Frame):

    def __init__(self, root: tkinter.Tk, **kw):
        super().__init__(root, **kw)
        self.root = root

        self.parser: Optional[Parser] = None
        self.experimental_correction_applied: bool = False
        self.control_analyzes_indexes: List[int] = []
        self.theoretical_correction_applied: False = False
        self.relative_result = tkinter.IntVar()

        # Widgets
        self.cb_molecule = ttk.Combobox(self.root, values=[], state='readonly')
        self.cb_molecule.bind('<<ComboboxSelected>>', self.recalculate_results)
        self.btn_apply_experimental_corrections = ttk.Button(
            self.root,
            text='Apply corrections with control measures',
            command=self._apply_experimental_corrections
        )
        self.table = ttk.Treeview(self.root)
        self.scrollbar = ttk.Scrollbar()
        self._set_table()
        self.cb_m_value = ttk.Combobox(self.root, values=[], state='readonly')
        self.btn_show_histogram = ttk.Button(self.root, text='Show histogram', command=self._show_histogram)
        self.btn_export = ttk.Button(
            self.root,
            text='Export metabolite data',
            command=lambda: self._export_data(all_data=False)
        )
        self.btn_export_all = ttk.Button(
            self.root,
            text='Export all data',
            command=lambda: self._export_data(all_data=True)
        )

        # Frames
        FileSelectorFrame(self, width=760, height=90).place(x=320, y=20)

        # Layout
        ttk.Label(self.root, text='Metabolite:').place(x=320, y=130)
        self.cb_molecule.place(x=400, y=125, width=200, height=25)
        ttk.Checkbutton(
            self.root,
            text='Relative results',
            variable=self.relative_result,
            command=self.recalculate_results,
        ).place(x=630, y=125, width=130, height=25)
        self.btn_apply_experimental_corrections.place(x=780, y=125, width=300, height=25)
        self.cb_m_value.place(x=50, y=840, width=115, height=30)
        self.btn_show_histogram.place(x=200, y=840, width=150, height=30)
        self.btn_export.place(x=1050, y=840, width=180, height=30)
        self.btn_export_all.place(x=1250, y=840, width=115, height=30)

    def _set_table(self):
        del self.scrollbar
        self.scrollbar = ttk.Scrollbar(self.root)
        self.scrollbar.place(x=1350, y=160, width=20, height=660)
        self.table.place(x=50, y=160, width=1300, height=660)

        self.scrollbar.config(command=self.table.yview)
        self.table.config(yscrollcommand=self.scrollbar.set)

        self.table.bind("<Delete>", self._delete_row)

    def recalculate_results(self, *_):
        analyzes = self._get_analyzes()
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

    def _apply_experimental_corrections(self):
        if not self.experimental_correction_applied and self.cb_molecule.get() != '':
            self.wait_window(CorrectionWizard(self))

        else:
            self.experimental_correction_applied = False
            self.btn_apply_experimental_corrections.config(text='Apply corrections with control measures')
            self.recalculate_results()

    def _export_data(self, all_data: bool):
        with filedialog.asksaveasfile(mode='w', title='Select file', defaultextension='.csv') as file:
            analyzes = self._get_analyzes(all_data=all_data)
            header: List[str] = ['Analysis']
            rows: List[List[str]] = [[analysis.name] for analysis in analyzes]

            for molecule_result in analyzes[0].results:
                header += [f'{molecule_result.name} M+{m_result.m_number}' for m_result in molecule_result.m_results]

            for i, analysis in enumerate(analyzes):
                for molecule_result in analysis.results:
                    rows[i] += [str(r.istd_resp_ratio) for r in molecule_result.m_results]

            file.write(','.join(header) + '\n')
            for row in rows:
                file.write(','.join(row) + '\n')

    def _get_analyzes(self, all_data: bool = False) -> List[Analysis]:
        if all_data:
            analyzes = self.parser.get_analyzes()
        else:
            analyzes = self.parser.get_analyzes_of_given_molecule(self.cb_molecule.get())

        if self.experimental_correction_applied:
            control_analyzes = self._find_control_analyzes(analyzes)
            with_relative_results = bool(self.relative_result.get())
            analyzes = apply_experimental_corrections(analyzes, control_analyzes, with_relative_results)

        elif self.theoretical_correction_applied:
            raise NotImplementedError('Theoretical corrections have not been implemented')

        return analyzes

    def _find_control_analyzes(self, analyzes: List[Analysis]) -> List[Analysis]:
        control_analyzes = []

        for analysis_index in self.control_analyzes_indexes:
            for analysis in analyzes:
                if analysis.index == analysis_index:
                    control_analyzes.append(analysis)
                    break

        return control_analyzes

    def _show_histogram(self):
        analyzes = self._get_analyzes()
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

    def _delete_row(self, *_):
        for row in self.table.selection():
            self.table.delete(row)
