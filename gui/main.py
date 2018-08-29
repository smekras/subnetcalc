"""
Stergios Mekras
eaasmek@students.eaaa.dk
"""

# Left here for future GTK port
# import gi
# gi.require_version("Gtk", "3.0")
# from gi.repository import Gtk

# from tkinter import messagebox
from ttkthemes import themed_tk as tk

from gui.frame import *


class SubnetCalc(object):
    def __init__(self):
        self.add_frame = AddressFrame()


root = tk.ThemedTk()
root.title("Subnet Calculator")
root.set_theme("ubuntu")

app = SubnetCalc()

root.mainloop()
