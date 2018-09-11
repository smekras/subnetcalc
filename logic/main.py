"""
Stergios Mekras

stergios.mekras@gmail.com
eaasmek@students.eaaa.dk
"""

from logic.address import *
from logic.network import *


def get_address():
    given_address = input("Enter IP address (default CIDR /24): ")

    try:
        if '/' in given_address:
            address, cidr = given_address.split(sep='/')
        else:
            address = given_address
            cidr = "24"

        full_ip = Address(address, cidr)
        return full_ip
    except ValueError:
        print("Not a valid address.")
        quit()


def get_network(add):
    network = str(add.address) + "/" + add.cidr
    return network


def get_custom_subnets(net):
    custom = input("Is a custom subnet mask used (y/N)?: ").lower()

    if custom == "y":
        new_cidr = input("Enter custom CIDR: ")
        net.get_subnet_list(new_cidr)
    else:
        net.get_subnet_list()


def get_subnet_list(net):
    show = input("Show all subnets (Y/n)?: ").lower()

    if show != "n":
        net.print_subnet_list()


bla = get_address()
bla.print_information()
print()
blu = Network(get_network(bla))
blu.print_information()
print()
get_custom_subnets(blu)
print()
get_subnet_list(blu)
print()
blu.print_specific_subnet()
print()
