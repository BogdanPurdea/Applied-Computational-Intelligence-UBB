import tkinter as tk
from gui import MASGUI

def main():
    root = tk.Tk()
    app = MASGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
