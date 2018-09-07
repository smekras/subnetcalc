"""
Stergios Mekras
eaasmek@students.eaaa.dk
"""

from tkinter.scrolledtext import *

from gui.custom import *
from logic.address import *


class GenericFrame(Frame):
    def __init__(self, app=None, **kw):
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
        self.label.configure(text="Address Configuration")
        self.banner = Frame(self.frame)
        self.octets = Frame(self.banner)

        self.prompt = Label(self.banner, text="IP Address:")
        self.sep_0 = Label(self.octets, text=".")
        self.sep_1 = Label(self.octets, text=".")
        self.sep_2 = Label(self.octets, text=".")
        self.sep_3 = Label(self.octets, text="/")

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
        self.cidr_entry = ValidatingEntry(self.banner, width=2, textvariable=cidr)

        octet_entries = [self.octet_entry_0, self.octet_entry_1, self.octet_entry_2, self.octet_entry_3]
        for i in range(len(octet_entries)):
            octet_entries[i].limit = 255
        self.cidr_entry.limit = 32

        [octet.set(0) for octet in octets]
        cidr.set(24)

        self.custom_used = IntVar()
        self.new_cidr = IntVar()

        self.entry = ValidatingEntry(self.banner, state=DISABLED, width=2, textvariable=self.new_cidr)
        self.entry.limit = 32

        self.check = Checkbutton(self.banner, text="Allow Custom CIDR:", variable=self.custom_used,
                                 command=self.enable_custom_cidr)

        self.button = Button(self.banner, text="OK", width=3, command=self.app.get_address)

        self.new_cidr = 0

        self.label.grid(row=0, column=0)
        self.banner.grid(row=1, column=0)
        self.info.grid(row=2, column=0)

        self.prompt.grid(row=0, column=0)
        self.octets.grid(row=0, column=1, padx=5)
        self.cidr_entry.grid(row=0, column=2)
        self.check.grid(row=1, column=0, columnspan=2, sticky='e')
        self.entry.grid(row=1, column=2, padx=5)
        self.button.grid(row=1, column=3)

        self.octet_entry_0.grid(row=0, column=0)
        self.sep_0.grid(row=0, column=1)
        self.octet_entry_1.grid(row=0, column=2)
        self.sep_1.grid(row=0, column=3)
        self.octet_entry_2.grid(row=0, column=4)
        self.sep_2.grid(row=0, column=5)
        self.octet_entry_3.grid(row=0, column=6)
        self.sep_3.grid(row=0, column=7)

    def get_address(self):
        full_ip = self.octet_entry_0.get() + "." + self.octet_entry_1.get() + "." + \
                  self.octet_entry_2.get() + "." + self.octet_entry_3.get()

        address = Address(full_ip, self.cidr_entry.get())
        return address

    def enable_custom_cidr(self):
        if self.custom_used != 0:
            self.entry.config(state='NORMAL')
        else:
            self.entry.config(state='DISABLED')


class NetworkFrame(GenericFrame):
    def __init__(self, app, **kw):
        super().__init__(app, **kw)
        self.label.config(text="Original Network Information")
        self.info.config(height=6)

        self.button = Button(self.frame, state=DISABLED, text="Subnet List >>", command=self.app.show_subnet_list)

        self.label.pack()
        self.info.pack()
        self.button.pack()


class SubnetFrame(GenericFrame):
    def __init__(self, app, **kw):
        super().__init__(app, **kw)
        self.label.config(text="Subnet Information")
        self.info.config(height=6)

        self.label.pack()
        self.info.pack()


class DebugFrame(GenericFrame):
    def __init__(self, app, **kw):
        super().__init__(app, **kw)
        self.info = ScrolledText(self.frame, state=NORMAL, height=4)

        self.label.config(text="Debug Console:")

        sys.stderr = OutputRedirector(self.info)

        self.label.pack()
        self.info.pack(fill='x')


class ListFrame(GenericFrame):
    def __init__(self, app, **kw):
        super().__init__(app, **kw)
        self.label.config(text="Network Subnets")
        self.sub_list = Treeview(self.frame, columns=["", "", "", ""])
        self.sub_list.configure(height=14)
        self.sub_list.heading("#0", text="Subnet")
        self.sub_list.heading("#1", text="Network IP")
        self.sub_list.heading("#2", text="First Host")
        self.sub_list.heading("#3", text="Last Host")
        self.sub_list.heading("#4", text="Broadcast IP")
        self.sub_list.column("#0", width=70, stretch=0)
        self.sub_list.column("#1", width=140, stretch=0)
        self.sub_list.column("#2", width=140, stretch=0)
        self.sub_list.column("#3", width=140, stretch=0)
        self.sub_list.column("#4", width=140, stretch=0)
        self.sub_list.bind("<<TreeViewSelect>>", self.on_subnet_select)
        self.sub_view = self.sub_list
        self.scroll = Scrollbar(self.frame, orient="vertical", command=self.sub_list.yview)

        self.label.pack()
        self.sub_list.pack(side='left')
        self.scroll.pack(side='right', fill='y')

    def on_subnet_select(self, subnet):
        print("Stuff to show here", subnet)
