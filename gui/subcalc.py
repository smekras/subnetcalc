"""
Stergios Mekras
eaasmek@students.eaaa.dk
"""

# Left here for future GTK port
# import gi
# gi.require_version("Gtk", "3.0")
# from gi.repository import Gtk

from ttkthemes import themed_tk as tk

from gui.frames import *


class SubnetCalc(object):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.master = Frame()

        # Address
        self.add_frame = AddressFrame(self)

        # Network
        self.net_frame = NetworkFrame(self)

        # Custom
        self.cus_frame = CustomFrame(self)

        # Debug Console
        self.err_frame = DebugFrame(self)

        # Subnets
        self.sub_frame = SubnetFrame(self)

        # Assembly
        self.master.pack()
        self.add_frame.frame.grid(row=0, column=0)
        self.net_frame.frame.grid(row=1, column=0)
        self.cus_frame.frame.grid(row=2, column=0)
        self.err_frame.frame.grid(row=3, column=0)


root = tk.ThemedTk()
root.title("Subnet Calculator")
root.resizable(False, False)
root.set_theme("ubuntu")

app = SubnetCalc()

root.mainloop()
