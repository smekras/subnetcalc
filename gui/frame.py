"""
Stergios Mekras
eaasmek@students.eaaa.dk
"""

from gui.custom import *
from logic.address import *
from logic.network import *


class AddressFrame(Frame):
    address = None
    network = None
    subnet = None

    def __init__(self, **kw):
        super().__init__(**kw)
        self.master = Frame()

        self.add_frame = Frame(self.master)
        self.add_label = Label(self.add_frame, text="Enter IP Address:")
        self.add_octets = Frame(self.add_frame)

        octet_0 = StringVar()
        octet_1 = StringVar()
        octet_2 = StringVar()
        octet_3 = StringVar()
        cidr = StringVar()

        self.octet_0 = ValidatingEntry(self.add_octets, width=3, textvariable=octet_0)
        self.octet_0.limit = 255
        self.octet_1 = ValidatingEntry(self.add_octets, width=3, textvariable=octet_1)
        self.octet_1.limit = 255
        self.octet_2 = ValidatingEntry(self.add_octets, width=3, textvariable=octet_2)
        self.octet_2.limit = 255
        self.octet_3 = ValidatingEntry(self.add_octets, width=3, textvariable=octet_3)
        self.octet_3.limit = 255
        self.octet_cidr = ValidatingEntry(self.add_octets, width=2, textvariable=cidr)
        self.octet_cidr.limit = 32

        octet_0.set(0)
        octet_1.set(0)
        octet_2.set(0)
        octet_3.set(0)
        cidr.set(24)

        self.octet_sep_0 = Label(self.add_octets, text=".")
        self.octet_sep_1 = Label(self.add_octets, text=".")
        self.octet_sep_2 = Label(self.add_octets, text=".")
        self.octet_sep_3 = Label(self.add_octets, text="/")

        self.add_button = Button(self.add_frame, text="OK", width=3, command=self.get_address)
        self.add_info = Text(self.add_frame, state=DISABLED, width=55, height=4)

        self.net_frame = Frame(self.master)
        self.net_label = Label(self.net_frame, text="Original Network Information")
        self.net_info = Text(self.net_frame, state=DISABLED, width=55, height=6)

        self.net_label.grid(row=0, column=0)
        self.net_info.grid(row=1, column=0)

        self.custom_frame = Frame(self.master)
        self.custom_label = Label(self.custom_frame, text="Is a custom subnet mask used?")

        self.custom = BooleanVar()
        self.custom_yes = Radiobutton(self.custom_frame, state=DISABLED, text="Yes",
                                      variable=self.custom, value=True, command=self.show_custom_net)
        self.custom_no = Radiobutton(self.custom_frame, state=DISABLED, text="No",
                                     variable=self.custom, value=False, command=self.show_custom_net)
        # self.custom.set(False)

        self.custom_cidr = Frame(self.custom_frame)
        self.cidr_label = Label(self.custom_cidr, text="Enter custom CIDR:")
        new_cidr = StringVar()
        self.cidr_entry = ValidatingEntry(self.custom_cidr, state=DISABLED, width=2, textvariable=new_cidr)
        self.cidr_entry.limit = 32

        self.error_display = Text(self.master, width=55, height=2)
        sys.stderr = OutputRedirector(self.error_display)

        self.add_label.grid(row=0, column=0, padx=5)
        self.add_octets.grid(row=0, column=1)
        # Contents of self.add_octets - start
        self.octet_0.pack(side=LEFT)
        self.octet_sep_0.pack(side=LEFT)
        self.octet_1.pack(side=LEFT)
        self.octet_sep_1.pack(side=LEFT)
        self.octet_2.pack(side=LEFT)
        self.octet_sep_2.pack(side=LEFT)
        self.octet_3.pack(side=LEFT)
        self.octet_sep_3.pack(side=LEFT)
        self.octet_cidr.pack(side=LEFT)
        # Contents of self.add_octets - end
        self.add_button.grid(row=0, column=2, padx=5)
        self.add_info.grid(row=1, column=0, columnspan=3)

        self.custom_label.grid(row=0, column=0)
        self.custom_yes.grid(row=0, column=1)
        self.custom_no.grid(row=0, column=2)
        self.custom_cidr.grid(row=2, column=0)
        # Contents of self.custom_cidr - start
        self.cidr_label.pack(side=LEFT)
        self.cidr_entry.pack(side=LEFT)

        self.sub_frame = Frame(self.master)

        self.add_frame.grid(row=0, column=0)
        self.net_frame.grid(row=1, column=0)
        self.custom_frame.grid(row=2, column=0)
        self.error_display.grid(row=3, column=0)
        self.sub_frame.grid(row=0, column=1)
        self.master.grid(row=0, column=0)

    def get_address(self):
        full_ip = self.octet_0.get() + "." + self.octet_1.get() + "." + self.octet_2.get() + "." + self.octet_3.get()
        self.address = Address(full_ip, self.octet_cidr.get())

        self.display_info(self.add_info)

        self.get_original_network()
        self.enable_custom_frame()

    def get_original_network(self):
        net_address = str(self.address.address) + "/" + self.address.cidr
        self.network = Network(net_address)

        self.display_info(self.net_info)

    def get_subnet_list(self):
        pass

    def enable_custom_frame(self):
        self.custom_yes.config(state=NORMAL)
        self.custom_no.config(state=NORMAL)

    def show_custom_net(self):
        if self.custom.get():
            self.custom_cidr.grid(row=4, column=0)
        else:
            self.custom_cidr.grid_remove()

    def display_info(self, text_area):
        text_area.delete("1.0", END)
        sys.stdout = OutputRedirector(text_area)
        text_area.config(state=NORMAL)
        if text_area is self.add_info:
            self.address.print_information()
        elif text_area is self.net_info:
            self.network.print_network_information()
        text_area.config(state=DISABLED)
