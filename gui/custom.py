"""
Stergios Mekras

stergios.mekras@gmail.com
eaasmek@students.eaaa.dk
"""

from tkinter import *
from tkinter.ttk import *


class ValidatingEntry(Entry):
    # base class for validating entry widgets
    def __init__(self, *args, **kwargs):
        Entry.__init__(self, *args, **kwargs)

        vcmd = (self.register(self.on_validate), "%P")
        self.configure(validate="key", validatecommand=vcmd)
        self.limit = 0

    def disallow(self):
        self.bell()

    def on_validate(self, new_value):
        try:
            if new_value.strip() == "":
                return True
            value = int(new_value)
            if value < 0 or value > self.limit:
                self.disallow()
                return False
        except ValueError:
            self.disallow()
            return False

        return True


class OutputRedirector(object):
    def __init__(self, text_widget):
        self.text_space = text_widget

    def write(self, string):
        self.text_space.insert("end", string)
        self.text_space.see("end")
