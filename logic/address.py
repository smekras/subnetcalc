"""
Stergios Mekras
eaasmek@students.eaaa.dk
"""

import ipaddress as ip


class Address(object):
    def __init__(self, address="192.168.1.1", cidr="24"):
        self.address = ip.ip_address(address)
        self.cidr = cidr
        self.range = self.get_address_class()
        self.type = self.get_address_type()

    def get_address_class(self):
        class_a_p = ip.ip_network("10.0.0.0/8")
        class_b_p = ip.ip_network("172.16.0.0/12")
        class_c_p = ip.ip_network("192.168.0.0/16")

        class_level = "classless"

        octet = int(list(str(self.address).split("."))[0])
        class_id = "{0:08b}".format(octet)
        exceptions = ["00000000", "01111111"]

        if class_id in exceptions:
            if class_id == exceptions[0]:
                print("Not a valid IP.")
            else:
                print("This is a loopback address.")
            class_level = "exception"
        else:
            if self.address.is_private:
                if self.address in class_a_p:
                    class_level = "private Class A"
                elif self.address in class_b_p:
                    class_level = "private Class B"
                elif self.address in class_c_p:
                    class_level = "private Class C"
                else:
                    class_level = "private classless"
            elif self.address.is_global:
                if class_id[:1] == "0":
                    class_level = "public Class A"
                elif class_id[:2] == "10":
                    class_level = "public Class B"
                elif class_id[:3] == "110":
                    class_level = "public Class C"
                elif class_id[:4] == "1110":
                    class_level = "public Class D"
                elif class_id[:4] == "1111":
                    class_level = "public Class E"
        return class_level

    def get_address_type(self):
        ip_type = "normal"
        if self.address.is_loopback:
            ip_type = "loopback"
        elif self.address.is_multicast:
            ip_type = "multicast"
        elif self.address.is_link_local:
            ip_type = "link-local"
        return ip_type

    def print_information(self):
        if self.range == "exception" or self.type == "loopback":
            print("Nothing more to do here. Have a nice life!")
            exit()
        else:
            print("The given IP is", self.address)
            print("This is a {} address.".format(self.type))
            print("It belongs to a {} network.".format(self.range))
