from tkinter import *

config = {"title":"Editor", "version":"[Version: 0.1]"}

window = Tk()
window.title(config["title"] + " " +config["version"])
window.config(bg="#20232A")
window.state('zoomed')

def Start():
    menubar = Menu(window, borderwidth=0, bg="#20232A") # Tried adding background to this, but it doesent work

    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Open")
    filemenu.add_command(label="Save")
    menubar.add_cascade(label="File", menu=filemenu)
    window.config(menu=menubar)

Start()
window.mainloop()