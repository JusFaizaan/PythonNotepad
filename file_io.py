from tkinter import END, filedialog, messagebox

def update_recent_files(state, path):
    if path in state.recent_files:
        state.recent_files.remove(path)
    state.recent_files.insert(0, path)
    state.recent_files = state.recent_files[:5] 

def new_file(state, text, root):
    state.filename = None
    text.delete("1.0", END)
    root.title("Python Notepad")

def open_file(state, text, root):
    path = filedialog.askopenfilename(
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if not path:
        return
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        messagebox.showerror("Oops!", f"Unable to open file:\n{e}")
        return
    text.delete("1.0", END)
    text.insert("1.0", content)
    state.filename = path
    root.title(f"Python Notepad - {state.filename}")
    update_recent_files(state, path)

def open_recent(state, text, root, path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        messagebox.showerror("Oops!", f"Unable to open file:\n{e}")
        return
    text.delete("1.0", END)
    text.insert("1.0", content)
    state.filename = path
    root.title(f"Python Notepad - {state.filename}")
    update_recent_files(state, path)

def save_file(state, text, root):
    if not state.filename:
        return save_as(state, text, root)
    try:
        content = text.get("1.0", END)
        with open(state.filename, "w", encoding="utf-8") as f:
            f.write(content.rstrip("\n"))
        update_recent_files(state, state.filename)
    except Exception as e:
        messagebox.showerror("Oops!", f"Unable to save file:\n{e}")

def save_as(state, text, root):
    path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if not path:
        return
    state.filename = path
    save_file(state, text, root)
