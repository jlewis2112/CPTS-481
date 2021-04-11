"""
Joseph Lewis
Spreadsheet tester
"""

from tkinter import *
from spreadsheet import Spreadsheet

root = Tk()
nRows = 6
nCols = 8
root.title(f"A {nRows}X{nCols} Spreadsheet")
spreadsheet = Spreadsheet(root, nRows, nCols)
spreadsheet.grid(row=0, column=0)
spreadsheet.focusLabel.grid(row=0, column=0)
spreadsheet.focusEntry.grid(row=0, column=1)
root.mainloop()
