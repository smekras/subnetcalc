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
        self.con_frame = ControlFrame(self)
        self.add_frame = AddressFrame(self)
        self.net_frame = NetworkFrame(self)
        self.err_frame = DebugFrame(self)
        self.cus_frame = CustomFrame(self)
        self.sub_frame = SubnetFrame(self)

        # Assembly
        self.master.pack()
        self.con_frame.frame.grid(row=0, column=0, padx=5, columnspan=2)
        self.add_frame.frame.grid(row=1, column=0, padx=5)
        self.net_frame.frame.grid(row=2, column=0, padx=5, pady=5)
        self.err_frame.frame.grid(row=1, column=1, padx=5)
        self.cus_frame.frame.grid(row=2, column=1, padx=5, pady=5)

    def get_address(self):
        self.address = self.con_frame.get_address()
        self.network = Network(str(self.address.address) + "/" + self.address.cidr)
        sys.stdout = OutputRedirector(self.err_frame.info)
        self.err_frame.info.configure(state=NORMAL)
        if self.network.get_subnet_type() == "Special":
            print("Special case, no proper distinction between network address, valid hosts, and broadcast address. "
                  "Proceed with caution")
        else:
            self.err_frame.info.delete('1.0', END)
        self.err_frame.info.configure(state=DISABLED)
        self.add_frame.display_info(self.address)
        self.con_frame.button_1.config(state=NORMAL)
        self.net_frame.display_info(self.network)
        if self.con_frame.custom_used.get() != 0:
            if self.con_frame.entry.get():
                self.con_frame.new_cidr = int(self.con_frame.entry.get())
                self.subnets = self.network.get_subnet_list(self.con_frame.new_cidr)
                self.cus_frame.display_info()
        else:
            self.subnets = self.network.subnet_list
            self.cus_frame.clear_info()
        sys.stdout = OutputRedirector(self.err_frame.info)
        self.fill_subnet_list()

    def show_subnet_list(self):
        if self.expanded:
            self.sub_frame.frame.grid_remove()
            self.con_frame.button_1.configure(text="Show Subnet List")
            self.expanded = False
        else:
            self.sub_frame.frame.grid(row=3, column=0, columnspan=2)
            self.con_frame.button_1.configure(text="Hide Subnet List")
            self.expanded = True

    def fill_subnet_list(self):
        self.sub_frame.sub_list.delete(*self.sub_frame.sub_list.get_children())
        if self.subnets is not None:
            for i in range(len(self.subnets)):
                subnet = self.subnets[i]
                # TODO: Get the list to work for /31 and /32
                if str(subnet.netmask) == "255.255.255.255":
                    subnet_ips = [subnet[0], subnet[0], subnet[0], subnet[0]]
                elif str(subnet.netmask) == "255.255.255.254":
                    subnet_ips = [subnet[0], subnet[0], subnet[-1], subnet[-1]]
                else:
                    subnet_ips = [subnet[0], subnet[1], subnet[-2], subnet[-1]]
                self.sub_frame.sub_view.insert("", "end", text="#" + str(i),
                                               values=(subnet_ips[0], subnet_ips[1], subnet_ips[2], subnet_ips[3]))


root = tk.ThemedTk()
root.title("Subnet Calculator")
root.resizable(False, False)
"""
List of available themes from root.get_themes()
['classic', 'ubuntu', 'keramik_alt', 'elegance', 'equilux', 'black', 'default', 'arc', 'radiance', 
'plastik', 'aquativo', 'keramik', 'clam', 'winxpblue', 'clearlooks', 'kroc', 'blue', 'alt']
"""
root.set_theme("ubuntu")

app = SubnetCalc()

root.eval('tk::PlaceWindow %s center' % root.winfo_pathname(root.winfo_id()))
root.mainloop()
