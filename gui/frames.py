"""
Stergios Mekras
eaasmek@students.eaaa.dk
"""

from tkinter.scrolledtext import *

from gui.custom import *
from logic.address import *
from logic.network import *


class GenericFrame(Frame):
    def __init__(self, app, **kw):
        super().__init__(**kw)
        self.app = app
        self.parent = app.master
        self.frame = Frame(self.parent)
        self.label = Label(self.frame, text="")
        self.info = Text(self.frame, state=DISABLED, width=55, height=4)

    def display_info(self, source):
        self.info.delete("1.0", END)
        sys.stdout = OutputRedirector(self.info)
        self.info.config(state=NORMAL)
        source.print_information()
        self.info.config(state=DISABLED)


class AddressFrame(GenericFrame):
    def __init__(self, app, **kw):
        super().__init__(app, **kw)
        self.entry = Frame(self.frame)
        self.octets = Frame(self.entry)

        self.label = Label(self.entry, text="Enter IP Address:")
        self.sep_0 = Label(self.octets, text=".")
        self.sep_1 = Label(self.octets, text=".")
        self.sep_2 = Label(self.octets, text=".")
        self.sep_3 = Label(self.octets, text="/")

        self.button = Button(self.entry, text="OK", width=3, command=self.get_address)

        octet_0 = StringVar()
        octet_1 = StringVar()
        octet_2 = StringVar()
        octet_3 = StringVar()
        octets = [octet_0, octet_1, octet_2, octet_3]
        cidr = StringVar()

        self.octet_entry_0 = ValidatingEntry(self.octets, width=3, textvariable=octet_0)
        self.octet_entry_1 = ValidatingEntry(self.octets, width=3, textvariable=octet_1)
        self.octet_entry_2 = ValidatingEntry(self.octets, width=3, textvariable=octet_2)
        self.octet_entry_3 = ValidatingEntry(self.octets, width=3, textvariable=octet_3)
        self.cidr_entry = ValidatingEntry(self.octets, width=2, textvariable=cidr)

        octet_entries = [self.octet_entry_0, self.octet_entry_1, self.octet_entry_2, self.octet_entry_3]
        for i in range(len(octet_entries)):
            octet_entries[i].limit = 255
        self.cidr_entry.limit = 32

        [octet.set(0) for octet in octets]
        cidr.set(24)

        self.entry.pack()
        self.label.grid(row=0, column=0)
        self.octets.grid(row=0, column=1, padx=5)
        self.octet_entry_0.pack(side=LEFT)
        self.sep_0.pack(side=LEFT)
        self.octet_entry_1.pack(side=LEFT)
        self.sep_1.pack(side=LEFT)
        self.octet_entry_2.pack(side=LEFT)
        self.sep_2.pack(side=LEFT)
        self.octet_entry_3.pack(side=LEFT)
        self.sep_3.pack(side=LEFT)
        self.cidr_entry.pack(side=LEFT)
        self.button.grid(row=0, column=2)
        self.info.pack()

    def get_address(self):
        full_ip = self.octet_entry_0.get() + "." + self.octet_entry_1.get() + "." + \
                  self.octet_entry_2.get() + "." + self.octet_entry_3.get()

        address = Address(full_ip, self.cidr_entry.get())
        self.display_info(address)
        self.app.net_frame.get_original_network(address)


class CustomFrame(GenericFrame):
    def __init__(self, app, **kw):
        super().__init__(app, **kw)
        self.label.config(text="Subnet Configuration")

        self.custom_used = False
        self.banner = Frame(self.frame)

        self.new_cidr = IntVar()
        self.entry = ValidatingEntry(self.banner, state=DISABLED, width=2, textvariable=self.new_cidr)
        self.entry.limit = 32
        self.new_cidr = 0
        self.check = Checkbutton(self.banner, text="Allow Custom CIDR:", variable=self.custom_used,
                                 command=self.enable_custom_cidr())
        self.button = Button(self.banner, text="Subnet List >>", command=self.show_subnet_list)

        self.label.pack()
        self.banner.pack()
        self.check.pack(side=LEFT)
        self.entry.pack(side=LEFT, padx=5)
        self.button.pack(side=RIGHT)

    def enable_custom_cidr(self):
        if self.custom_used is not False:
            self.entry.config(state=NORMAL)
        else:
            self.entry.config(state=DISABLED)

    def show_subnet_list(self):
        visible = False
        if visible:
            self.app.sub_frame.grid_remove()
            visible = False
        else:
            self.app.sub_frame.grid(row=0, column=1, rowspan=4)
            visible = True


class DebugFrame(GenericFrame):
    def __init__(self, app, **kw):
        super().__init__(app, **kw)
        self.info = ScrolledText(self.frame, state=DISABLED, width=53, height=4)

        self.label.config(text="Debug Console:")
        self.info.config(state=NORMAL, height=2)
        sys.stderr = OutputRedirector(self.info)

        self.label.pack()
        self.info.pack()


class NetworkFrame(GenericFrame):
    def __init__(self, app, **kw):
        super().__init__(app, **kw)
        self.label.config(text="Original Network Information")
        self.info.config(height=6)

        self.label.pack()
        self.info.pack()

    def get_original_network(self, address):
        net_address = str(address.address) + "/" + address.cidr
        address.network = Network(net_address)
        # self.master.subnet_list = self.get_subnet_list()

        self.display_info(address.network)

    def get_subnet_list(self):
        new_cidr = self.master.new_cidr
        if self.master.network is not None:
            if new_cidr != "0":
                subnets = self.master.network.get_subnet_list(new_cidr)
            else:
                subnets = self.master.network.get_subnet_list()
            print(subnets)
        else:
            subnets = []
        return subnets


class SubnetFrame(GenericFrame):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self.label.config(text="Network Subnets")
        self.listbox = Listbox(self.frame, width=45, height=16)

        self.label.pack()
        self.listbox.pack()

    def fill_list(self, subnet_list):
        for item in subnet_list:
            self.listbox.insert(END, item)
