# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 14:23:00 2022

@author: arda.ercan
"""
# Variante 1:
from tkinter import *
from tkcalendar import Calendar,DateEntry # Version 1.6.1 // pip install tkcalendar
from datetime import datetime, timedelta

root = Tk()

start = DateEntry(root, width = 20, bg = "darkblue", fg = "white", year = 2022, month = 1, day = 1)
start.grid()

end = DateEntry(root, width = 30, bg ="darkblue", fg = "white", year = 2022, month = 1, day = 2)
end.grid()

root.mainloop()




# Variante 2:
# def get_date():
#     import tkinter as tk
#     from tkinter import ttk
#     from tkcalendar import Calendar, DateEntry

#     def cal_done():
#         top.withdraw()
#         root.quit()

#     root = tk.Tk()
#     root.withdraw() # keep the root window from appearing

#     top = tk.Toplevel(root)

#     cal = Calendar(top,
#                    font="Arial 14", selectmode='day',
#                    cursor="hand1")
#     cal.pack(fill="both", expand=True)
#     ttk.Button(top, text="ok", command=cal_done).pack()

#     selected_date = None
#     root.mainloop()
#     return cal.selection_get()

# selection = get_date()
# print(selection)