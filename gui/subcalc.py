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
from logic.network import *


class SubnetCalc(object):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.master = Frame()
        self.address = None
        self.network = None
        self.subnets = None

        # Frames
        self.add_frame = AddressFrame(self)
        self.net_frame = NetworkFrame(self)
        self.cus_frame = CustomFrame(self)
        self.err_frame = DebugFrame(self)
        self.sub_frame = SubnetFrame(self)

        # Assembly
        self.master.pack()
        self.add_frame.frame.grid(row=0, column=0)
        self.net_frame.frame.grid(row=1, column=0)
        self.cus_frame.frame.grid(row=2, column=0)
        self.err_frame.frame.grid(row=3, column=0)

    def get_address(self):
        self.address = self.add_frame.get_address()
        self.add_frame.display_info(self.address)
        self.network = Network(str(self.address.address) + "/" + self.address.cidr)
        self.net_frame.display_info(self.network)
        self.cus_frame.button.config(state=NORMAL)
        self.subnets = self.network.get_subnet_list()
        self.fill_subnet_list()

    def show_subnet_list(self):
        visible = False
        if visible:
            self.sub_frame.frame.grid_remove()
            visible = False
        else:
            self.sub_frame.frame.grid(row=0, column=1, rowspan=4)
            visible = True
        if self.cus_frame.new_cidr != 0:
            self.subnets = self.network.get_subnet_list(self.cus_frame.entry.get())

    def fill_subnet_list(self):
        self.sub_frame.sub_list.delete(0, END)
        if self.subnets is not None:
            [self.sub_frame.sub_list.insert(END, item) for item in self.subnets]


root = tk.ThemedTk()
root.title("Subnet Calculator")
root.resizable(False, False)
root.set_theme("ubuntu")

app = SubnetCalc()

root.mainloop()
