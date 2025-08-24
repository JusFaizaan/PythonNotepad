from state import AppState
from ui import build_root, build_text, build_menu, bind_keys

def main():
    state = AppState()
    root = build_root()
    text = build_text(root)
    build_menu(root, state, text)
    bind_keys(root, state, text)
    root.mainloop()

if __name__ == "__main__":
    main()
