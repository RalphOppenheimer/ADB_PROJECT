import tkinter as tk

class pop_up_window():
    def __init__(self, exception_text, _title = "Błąd"):
        win = tk.Toplevel()
        win.geometry('520x60+800+250')
        win.wm_title(_title)
        l = tk.Label(win, text=exception_text)
        l.config(anchor = tk.CENTER)
        l.pack()
        b = tk.Button(win, text="Zamknij", command = win.destroy)
        b.config(anchor = tk.CENTER)
        b.pack()