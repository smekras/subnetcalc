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
        self.expanded = False

        # Frames
        self.add_frame = AddressFrame(self)
        self.net_frame = NetworkFrame(self)
        self.sub_frame = SubnetFrame(self)
        self.err_frame = DebugFrame(self)
        self.lis_frame = ListFrame(self)

        # Assembly
        self.master.pack()
        self.add_frame.frame.grid(row=0, column=0)
        self.net_frame.frame.grid(row=0, column=1)
        self.sub_frame.frame.grid(row=0, column=2)
        self.err_frame.frame.grid(row=2, column=0, columnspan=3)

    def get_address(self):
        self.address = self.add_frame.get_address()
        self.network = Network(str(self.address.address) + "/" + self.address.cidr)
        self.add_frame.display_info(self.address)
        self.net_frame.display_info(self.network)
        self.net_frame.button.config(state=NORMAL)
        sys.stdout = OutputRedirector(self.err_frame.info)
        if self.add_frame.custom_used.get() != 0:
            if self.add_frame.entry.get():
                self.add_frame.new_cidr = int(self.add_frame.entry.get())
                self.subnets = self.network.get_subnet_list(self.add_frame.new_cidr)
        else:
            self.subnets = self.network.subnet_list
        self.fill_subnet_list()

    def show_subnet_list(self):
        if self.expanded:
            self.lis_frame.frame.grid_remove()
            self.net_frame.button.configure(text="Subnet List >>")
            self.expanded = False
        else:
            self.lis_frame.frame.grid(row=1, column=0, columnspan=3)
            self.net_frame.button.configure(text="Subnet List <<")
            self.expanded = True

    def fill_subnet_list(self):
        self.lis_frame.sub_list.delete(*self.lis_frame.sub_list.get_children())
        if self.subnets is not None:
            for i in range(len(self.subnets)):
                subnet = self.subnets[i]
                if str(subnet.netmask) == "255.255.255.255":
                    subnet_ips = [subnet[0], subnet[0], subnet[0], subnet[0]]
                elif str(subnet.netmask) == "255.255.255.254":
                    subnet_ips = [subnet[0], subnet[0], subnet[-1], subnet[-1]]
                else:
                    subnet_ips = [subnet[0], subnet[1], subnet[-2], subnet[-1]]
                self.lis_frame.sub_view.insert("", "end", text="#" + str(i),
                                               values=(subnet_ips[0], subnet_ips[1], subnet_ips[2], subnet_ips[3]))


root = tk.ThemedTk()
root.title("Subnet Calculator")
root.resizable(False, False)
root.set_theme("ubuntu")

app = SubnetCalc()

root.mainloop()
