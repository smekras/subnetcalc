"""
Stergios Mekras
eaasmek@students.eaaa.dk
"""

# Left here for future GTK port
# import gi
# gi.require_version("Gtk", "3.0")
# from gi.repository import Gtk

from ttkthemes import themed_tk as tk

from gui.custom import *
from logic.address import *
from logic.network import *


class SubnetCalc(object):
    address = None
    network = None
    subnet = None

    def __init__(self, **kw):
        super().__init__(**kw)
        self.master = Frame()

        # Address
        self.add_frame = Frame(self.master)
        self.add_entry = Frame(self.add_frame)
        self.add_octets = Frame(self.add_entry)

        self.add_label = Label(self.add_entry, text="Enter IP Address:")
        self.add_sep_0 = Label(self.add_octets, text=".")
        self.add_sep_1 = Label(self.add_octets, text=".")
        self.add_sep_2 = Label(self.add_octets, text=".")
        self.add_sep_3 = Label(self.add_octets, text="/")

        self.add_button = Button(self.add_entry, text="OK", width=3, command=self.get_address)
        self.add_info = Text(self.add_frame, state=DISABLED, width=55, height=4)

        octet_0 = StringVar()
        octet_1 = StringVar()
        octet_2 = StringVar()
        octet_3 = StringVar()
        octets = [octet_0, octet_1, octet_2, octet_3]
        cidr = StringVar()

        self.add_octet_0 = ValidatingEntry(self.add_octets, width=3, textvariable=octet_0)
        self.add_octet_1 = ValidatingEntry(self.add_octets, width=3, textvariable=octet_1)
        self.add_octet_2 = ValidatingEntry(self.add_octets, width=3, textvariable=octet_2)
        self.add_octet_3 = ValidatingEntry(self.add_octets, width=3, textvariable=octet_3)
        self.add_cidr = ValidatingEntry(self.add_octets, width=2, textvariable=cidr)

        octet_entries = [self.add_octet_0, self.add_octet_1, self.add_octet_2, self.add_octet_3]
        for i in range(len(octet_entries)):
            octet_entries[i].limit = 255
        self.add_cidr.limit = 255

        [octet.set(0) for octet in octets]
        cidr.set(24)

        self.add_entry.pack()
        self.add_label.grid(row=0, column=0)
        self.add_octets.grid(row=0, column=1, padx=5)
        self.add_octet_0.pack(side=LEFT)
        self.add_sep_0.pack(side=LEFT)
        self.add_octet_1.pack(side=LEFT)
        self.add_octet_1.pack(side=LEFT)
        self.add_sep_1.pack(side=LEFT)
        self.add_octet_2.pack(side=LEFT)
        self.add_sep_2.pack(side=LEFT)
        self.add_octet_3.pack(side=LEFT)
        self.add_sep_3.pack(side=LEFT)
        self.add_cidr.pack(side=LEFT)
        self.add_button.grid(row=0, column=2)
        self.add_info.pack()

        # Network
        self.net_frame = Frame(self.master)
        self.net_label = Label(self.net_frame, text="Original Network Information")
        self.net_info = Text(self.net_frame, state=DISABLED, width=55, height=6)

        self.net_label.pack()
        self.net_info.pack()

        # Custom
        self.custom_used = False
        self.cus_frame = Frame(self.master)
        self.cus_banner = Frame(self.cus_frame)
        self.cus_cidr = Frame(self.cus_banner)
        self.cus_show = Frame(self.cus_frame)
        self.cus_sep_0 = Separator(self.cus_frame, orient=HORIZONTAL)

        self.cus_check = Checkbutton(self.cus_banner, text="Allow Custom", variable=self.custom_used,
                                     command=self.enable_custom_cidr())
        self.cus_input = Label(self.cus_cidr, text="Enter custom CIDR:")
        self.new_cidr = StringVar()
        self.cus_entry = ValidatingEntry(self.cus_cidr, state=DISABLED, width=2, textvariable=self.new_cidr)
        self.cus_entry.limit = 32
        self.cus_button = Button(self.cus_frame, text="Subnet List >>")

        self.cus_banner.pack()
        self.cus_check.pack(side=LEFT)
        self.cus_sep_0.pack()
        self.cus_cidr.pack(side=LEFT)
        self.cus_input.pack(side=LEFT)
        self.cus_entry.pack(side=LEFT)
        self.cus_show.pack()
        self.cus_button.pack(side=RIGHT)

        # Debug Console
        self.err_frame = Frame(self.master)
        self.err_label = Label(self.err_frame, text="Debug Console:")

        self.err_display = Text(self.err_frame, width=55, height=2)
        # sys.stderr = OutputRedirector(self.err_display)

        self.err_label.pack()
        self.err_display.pack()

        # Subnets
        self.sub_frame = Frame(self.master)

        self.sub_label = Label(self.sub_frame, text="Network Subnets")
        self.sub_list = Listbox(self.sub_frame, width=45, height=16)

        self.sub_label.pack()
        self.sub_list.pack()

        # Assembly
        self.master.pack()
        self.add_frame.grid(row=0, column=0)
        self.net_frame.grid(row=1, column=0)
        self.cus_frame.grid(row=2, column=0)
        self.err_frame.grid(row=3, column=0)
        self.sub_frame.grid(row=0, column=1, rowspan=4)

    def get_address(self):
        full_ip = self.add_octet_0.get() + "." + self.add_octet_1.get() + "." + \
                  self.add_octet_2.get() + "." + self.add_octet_3.get()
        self.address = Address(full_ip, self.add_cidr.get())

        self.display_info(self.add_info)

        self.get_original_network()

    def get_original_network(self):
        net_address = str(self.address.address) + "/" + self.address.cidr
        self.network = Network(net_address)

        self.display_info(self.net_info)

    def get_subnet_list(self):
        pass

    def enable_custom_cidr(self):
        if self.custom_used:
            self.cus_cidr.grid(row=1, column=0)
        else:
            self.cus_cidr.grid_forget()
        print(self.custom_used)

    def display_info(self, text_area):
        text_area.delete("1.0", END)
        sys.stdout = OutputRedirector(text_area)
        text_area.config(state=NORMAL)
        if text_area is self.add_info:
            self.address.print_information()
        elif text_area is self.net_info:
            self.network.print_network_information()
        text_area.config(state=DISABLED)


root = tk.ThemedTk()
root.title("Subnet Calculator")
root.set_theme("ubuntu")

app = SubnetCalc()

root.mainloop()
