import tkinter as tk
from tkinter import Text, Menu, font
from file_io import new_file, open_file, save_file, save_as, open_recent

__all__ = ["build_root", "build_text", "build_menu", "bind_keys"]

class LineNumbers(tk.Canvas):
    def __init__(self, master, text_widget, **kwargs):
        super().__init__(master, width=30, bg="#f0f0f0", highlightthickness=0, **kwargs)
        self.text_widget = text_widget
        self.text_widget.bind("<KeyRelease>", self.schedule_redraw)
        self.text_widget.bind("<MouseWheel>", self.schedule_redraw)
        self.text_widget.bind("<ButtonRelease-1>", self.schedule_redraw)
        self.text_widget.bind("<Configure>", self.schedule_redraw)
        self.text_widget.bind("<<ChangeFont>>", self.schedule_redraw)
        self.text_widget.bind("<<Modified>>", self.schedule_redraw)
        self.text_widget.config(yscrollcommand=self.on_scroll)
        self.schedule_redraw()

    def schedule_redraw(self, event=None):
        self.after_idle(self.redraw)

    def on_scroll(self, *args):
        self.schedule_redraw()
        if hasattr(self.text_widget, "_yscroll"):
            self.text_widget._yscroll(*args)

    def redraw(self):
        self.delete("all")
        self.config(height=self.text_widget.winfo_height())
        i = self.text_widget.index("@0,0")
        while True:
            dline = self.text_widget.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2, y, anchor="nw", text=linenum, font=self.text_widget["font"])
            i = self.text_widget.index(f"{i}+1line")

def build_root():
    root = tk.Tk()
    root.title("Python Notepad")
    root.geometry("700x500") 
    return root

def build_text(root, state=None):
    text_font = font.Font(family="Consolas", size=state.font_size if state else 12)
    text = Text(root, wrap="word", font=text_font)
    if state:
        text.bind("<<ChangeFont>>", lambda e: text.config(font=font.Font(family="Consolas", size=state.font_size)))
    def on_change(event):
        text.event_generate("<<Modified>>")
    text.bind("<<ChangeFont>>", on_change)
    text.bind("<KeyRelease>", on_change)
    text.bind("<MouseWheel>", on_change)
    text.bind("<ButtonRelease-1>", on_change)
    if hasattr(text, "yscrollcommand"):
        text._yscroll = text.yscrollcommand
    return text

def build_line_numbers(root, text):
    ln = LineNumbers(root, text)
    ln.pack(side="left", fill="y")
    text.pack(side="right", expand=True, fill="both") 
    return ln

def build_menu(root, state, text):
    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="New", command=lambda: new_file(state, text, root))
    filemenu.add_command(label="Open", command=lambda: open_file(state, text, root))
    filemenu.add_command(label="Save", command=lambda: save_file(state, text, root))
    filemenu.add_command(label="Save As", command=lambda: save_as(state, text, root))

    recentmenu = Menu(filemenu, tearoff=0)
    def update_recent_menu():
        recentmenu.delete(0, "end")
        for path in state.recent_files:
            recentmenu.add_command(
                label=path,
                command=lambda p=path: open_recent(state, text, root, p)
            )
    filemenu.add_cascade(label="Open Recent", menu=recentmenu)
    filemenu.add_separator()
    filemenu.add_command(label="Quit", command=root.quit)
    menubar.add_cascade(label="File", menu=filemenu)

    viewmenu = Menu(menubar, tearoff=0)
    viewmenu.add_command(label="Zoom In", command=lambda: zoom_in(state, text, root))
    viewmenu.add_command(label="Zoom Out", command=lambda: zoom_out(state, text, root))
    menubar.add_cascade(label="View", menu=viewmenu)
    root.config(menu=menubar)

    root.bind("<FocusIn>", lambda e: update_recent_menu())

def zoom_in(state, text, root):
    state.font_size += 2
    text.config(font=("Consolas", state.font_size))
    text.event_generate("<<ChangeFont>>")
    text.event_generate("<<Modified>>")

def zoom_out(state, text, root):
    if state.font_size > 6:
        state.font_size -= 2
        text.config(font=("Consolas", state.font_size))
        text.event_generate("<<ChangeFont>>")
        text.event_generate("<<Modified>>")

def bind_keys(root, state, text):
    root.bind("<Control-s>",       lambda e: (save_file(state, text, root), "break"))
    root.bind("<Control-Shift-S>", lambda e: (save_as(state, text, root),  "break"))
    root.bind("<Control-o>",       lambda e: (open_file(state, text, root), "break"))
    root.bind("<Control-n>",       lambda e: (new_file(state, text, root),  "break"))
    root.bind("<Control-plus>",    lambda e: (zoom_in(state, text, root), "break"))
    root.bind("<Control-equal>",   lambda e: (zoom_in(state, text, root), "break"))
    root.bind("<Control-minus>",   lambda e: (zoom_out(state, text, root), "break"))
    root.bind("<Control-underscore>", lambda e: (zoom_out(state, text, root), "break"))
