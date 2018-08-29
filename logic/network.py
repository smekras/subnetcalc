"""
Stergios Mekras
eaasmek@students.eaaa.dk
"""

import ipaddress as ip


class Network(object):
    def __init__(self, net="192.168.1.0/24"):
        self.net = ip.ip_network(net, strict=False)
        self.type = self.get_subnet_type()
        self.subnet_list = self.get_subnet_list()
        self.subnet_number = len(self.subnet_list)
        self.host_list = list(self.net.hosts())
        self.host_number = self.get_host_number()
        self.host_first = self.get_host_first()
        self.host_last = self.get_host_last()

    def get_subnet(self, subnet_id):
        subnet = Network(self.subnet_list[subnet_id])
        subnet.print_subnet_information()

    def get_subnet_type(self):
        if len(list(self.net)) <= 2:
            subnet_type = "Special"
        else:
            subnet_type = "Standard"
        return subnet_type

    def get_subnet_list(self, new_cidr=None):
        address, cidr = str(self.net).split("/")

        if new_cidr is not None:
            if int(new_cidr) > int(cidr):
                subnet_list = list(self.net.subnets(new_prefix=int(new_cidr)))
            else:
                subnet_list = list(self.net.supernet(new_prefix=int(new_cidr)))
        else:
            parent = ""
            if int(cidr) > 24:
                parent = address + "/24"
            elif 24 > int(cidr) > 16:
                parent = address + "/16"
            elif 16 > int(cidr) > 8:
                parent = address + "/8"

            if int(cidr) == 24 or int(cidr) == 16 or int(cidr) == 8:
                subnet_list = [address]
            else:
                subnet_list = list(ip.ip_network(parent, strict=False).subnets(new_prefix=int(cidr)))
        self.subnet_list = subnet_list  # Needed for subsequent calls
        return subnet_list

    def get_host_number(self):
        if len(self.host_list) <= 2:
            host_number = len(self.host_list)
        else:
            host_number = len(self.host_list) - 2
        return host_number

    def get_host_first(self):
        if len(self.host_list) <= 2:
            first_host = self.net[0]
        else:
            first_host = self.net[1]
        return first_host

    def get_host_last(self):
        if len(self.host_list) <= 2:
            last_host = self.net[-1]
        else:
            last_host = self.net[-2]
        return last_host

    def print_network_information(self):
        print(self.type, "configuration. Proceed accordingly.")
        print("The Subnet Mask is:     ", self.net.netmask)
        print("The Host Mask is:       ", self.net.hostmask)
        print("Subnets per network:    ", self.subnet_number)
        print("Valid Hosts per subnet: ", self.host_number)

    def print_subnet_list(self):
        if len(self.subnet_list) == 1:
            print("The only subnet on this network is:", self.subnet_list[0])
        else:
            for i in range(len(self.subnet_list)):
                print("Subnet #" + str(i), "is:", self.subnet_list[i])

    def print_specific_subnet(self):
        show = True
        while show:
            subnet_id = input("Enter subnet # to show (0 to {}) or empty for none: ".format(len(self.subnet_list) - 1))
            print()
            if subnet_id is not "":
                print("This is subnet {}".format(subnet_id))
                self.get_subnet(int(subnet_id))
                print()
            else:
                show = False

    def print_subnet_information(self):
        print("The Network IP is:      ", self.net)
        print("The First Host (DG) is: ", self.host_first)
        print("The Last Host is:       ", self.host_last)
        print("The Broadcast IP is:    ", self.net.broadcast_address)
