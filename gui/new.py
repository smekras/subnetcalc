from gui.custom import *
from tkinter import *
from tkinter.ttk import *


class TestOutput(object):
    def __init__(self, parent):
        self.init()
        button = Button(parent, text="Start", command=self.print_out)
        button.grid(row=2, column=0, columnspan=2)

    def print_out(self):
        print("stuff")

    def init(self):
        text_box = Text(wrap="word", height=10, width=44)
        error_box = Text(wrap="word", height=10, width=44)
        text_box.grid(row=0, column=0, columnspan=2, sticky="NSWE", padx=5, pady=5)
        error_box.grid(row=1, column=0, columnspan=2, sticky="NSWE", padx=5, pady=5)
        sys.stdout = OutputRedirector(text_box)
        sys.stderr = OutputRedirector(error_box)


def on_click_mask():
    return messagebox.askyesno("Subnet Calculator", "Is a custom subnet mask used?")


def on_click_subnets():
    return messagebox.askyesno("Subnet Calculator", "Show all subnets?")


def toggle_custom():
    mask_label = Label(custom_frame, text="Enter custom CIDR")
    mask_cidr = CidrEntry(ip_frame, width=2, textvariable=default_cidr)

    if custom_mask.get() == 1:
        mask_label.pack()
        mask_cidr.pack()

        custom_mask.set(1)
        print("custom mask")
    else:
        mask_label.pack_forget()
        mask_cidr.pack_forget()

        custom_mask.set(0)
        print("no custom")


if __name__ == "__main__":

    custom_frame = Frame(net_frame)
    custom_label = Label(custom_frame, text="Is a custom subnet mask used?")
    custom_mask = IntVar()
    custom_yes = Radiobutton(custom_frame, text="Yes", variable=custom_mask, value=1, command=lambda: toggle_custom)
    custom_no = Radiobutton(custom_frame, text="No", variable=custom_mask, value=0, command=lambda: toggle_custom)


net_label_1 = Label(net_frame, text="Custom Network Information: ")
# net_label_1 = Label(net_frame, text = net.get_host_label(address))
net_info_0 = Text(net_frame, width=30, height=9)
net_info_1 = Text(net_frame, width=30, height=9)
net_button_0 = Button(net_frame, text="Custom Mask", command=lambda: on_click_mask())
