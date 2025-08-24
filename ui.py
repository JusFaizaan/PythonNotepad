import tkinter as tk
from tkinter import Text, Menu
from file_io import new_file, open_file, save_file, save_as

__all__ = ["build_root", "build_text", "build_menu", "bind_keys"]

def build_root():
    root = tk.Tk()
    root.title("Python Notepad")
    root.minsize(width=500, height=500)
    root.maxsize(width=500, height=500)
    return root

def build_text(root):
    text = Text(root, wrap="word")
    text.pack(expand=True, fill="both")
    return text

def build_menu(root, state, text):
    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="New", command=lambda: new_file(state, text, root))
    filemenu.add_command(label="Open", command=lambda: open_file(state, text, root))
    filemenu.add_command(label="Save", command=lambda: save_file(state, text, root))
    filemenu.add_command(label="Save As", command=lambda: save_as(state, text, root))
    filemenu.add_separator()
    filemenu.add_command(label="Quit", command=root.quit)
    menubar.add_cascade(label="File", menu=filemenu)
    root.config(menu=menubar)

def bind_keys(root, state, text):
    root.bind("<Control-s>",       lambda e: (save_file(state, text, root), "break"))
    root.bind("<Control-Shift-S>", lambda e: (save_as(state, text, root),  "break"))
    root.bind("<Control-o>",       lambda e: (open_file(state, text, root), "break"))
    root.bind("<Control-n>",       lambda e: (new_file(state, text, root),  "break"))
