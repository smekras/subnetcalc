"""
Stergios Mekras

stergios.mekras@gmail.com
eaasmek@students.eaaa.dk
"""
import ipaddress as ip


def address_information(address):
    """
    Display address information.

    :param address: IPv4Address
    :return: None
    """
    address_type = get_address_type(address)
    class_level = get_address_class(address)

    print()
    if class_level == "exception" or address_type == "loopback":
        print("Nothing more to do here. Have a nice life!")
        exit()
    else:
        print("The given IP is:        ", address)
        print("This is a {} address.".format(address_type))
        print("It belongs to a {} network.".format(class_level))


def network_information(net):
    """
    Display network information.

    :param net:
    :return: None
    """
    if str(net.netmask) in ["255.255.255.254", "255,255,255,255"]:
        """
        Networks with 2 or less total hosts, like those with CIDR 31 and 32,
        are special cases often used for peer-to-peer interfaces or host routes.
        """
        print("Special configuration, be careful!")
        host_number = len(list(net))
        first_host = "Not Available"
        last_host = "Not Available"
    else:
        host_number = len(list(net)) - 2
        first_host = net[1]
        last_host = net[-2]
    print("The Subnet Mask is:     ", net.netmask)
    print("The Host Mask is:       ", net.hostmask)
    print("Valid Hosts per subnet: ", host_number)
    print()
    print("The Network IP is:      ", net)
    print("The First Host (DG) is: ", first_host)
    print("The Last Host is:       ", last_host)
    print("The Broadcast IP is:    ", net.broadcast_address)


def subnet_information(subnet_list):
    """
    Display subnet information.

    :param subnet_list:
    :return: None
    """
    print()
    print("Subnets per network:    ", len(subnet_list))
    show_subnets(subnet_list)


def get_address_type(address):
    """
    Retrieve address type.

    :param address: IPv4Address
    :return: String
    """
    ip_type = "normal"
    if address.is_loopback:
        ip_type = "loopback"
        print("This is a loopback address.")
    elif address.is_multicast:
        ip_type = "multicast"
    elif address.is_link_local:
        ip_type = "link-local"
    return ip_type


def get_address_class(address):
    """
    Calculate network class based on the address.

    :param address: ip_address
    :return: String
    """
    class_a_p = ip.ip_network("10.0.0.0/8")
    class_b_p = ip.ip_network("172.16.0.0/12")
    class_c_p = ip.ip_network("192.168.0.0/16")

    class_level = "classless"

    octet = int(list(str(address).split("."))[0])
    class_id = "{0:08b}".format(octet)
    exceptions = ["00000000", "01111111"]

    if class_id in exceptions:
        if class_id == exceptions[0]:
            print("Not a valid IP.")
        else:
            print("This is a loopback address.")
        class_level = "exception"
    else:
        if address.is_private:
            if address in class_a_p:
                class_level = "private Class A"
            elif address in class_b_p:
                class_level = "private Class B"
            elif address in class_c_p:
                class_level = "private Class C"
            else:
                class_level = "private classless"
        elif address.is_global:
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


def get_subnet_list(old_net, new_net=None):
    """
    Calculate subnet list based on CIDR.
    Cheat Sheet: https://kthx.at/subnetmask/

    :param old_net: ip_network
    :param new_net: ip_network
    :return: List of ip_network objects
    """
    address, cidr = str(old_net).split("/")

    if new_net is not None:
        """
        The following code calculates the subnets of a network in case of a custom setup. For example,
        dividing a /24 network into a /28 one, will result in different subnets than a normal /28 network.
        The same is true for using less bits for the network, for example turning a /25 into a /22 network.
        """
        junk, mask = str(new_net).split("/")

        if int(mask) > int(cidr):
            subnet_list = list(ip.ip_network(old_net, strict=False).subnets(new_prefix=int(mask)))
        else:
            subnet_list = list(ip.ip_network(old_net, strict=False).supernet(new_prefix=int(mask)))
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

    return subnet_list


def show_subnets(subnet_list):
    """
    Get user input, display subnet list and information as prompted.

    :param subnet_list: List of IPv4Network objects
    :return: None
    """
    choice = input("Show all subnets (Y/n)? ").lower()
    if choice != "n":
        if len(subnet_list) == 1:
            print("The only subnet on this network is:", subnet_list[0])
        else:
            for i in range(len(subnet_list)):
                print("Subnet #" + str(i), "is:", subnet_list[i])

            show = True
            while show:
                subnet_id = input("Enter subnet # to show (0 to {}) or empty for none: ".format(len(subnet_list) - 1))
                print()
                if subnet_id is not "":
                    print("This is subnet {}".format(subnet_id))
                    network_information(subnet_list[int(subnet_id)])
                    print()
                else:
                    show = False


def main():
    """
    Ask user for IP address, calculate the necessary information.

    :return: None
    """
    given_address = input("Enter IP address (default CIDR /24): ")
    if '/' in given_address:
        add, cidr = given_address.split(sep='/')
        full_address = given_address
    else:
        add = given_address
        cidr = "24"
        full_address = given_address + "/" + cidr

    try:
        """
        The following block of code will only be executed if the user input (given_address) is valid. If the address or
        the netmask are not valid ones, then the program should throw an error and exit gracefully.
        Note:
        If an IPv6Address is required, the following code has to be altered to:
        address = ip.IPv6Address(add)
        orig_net = ip.IPv6Network(full_address, strict=False)
        If a more generic version is required, then the code should be altered to:
        try:
            address = ip.ip_address(add)
            orig_net = ip.ip_network(full_address, strict=False)
        except ValueError:
        """
        address = ip.IPv4Address(add)
        orig_net = ip.IPv4Network(full_address, strict=False)

        address_information(address)
        network_information(orig_net)

        print()
        custom = input("Is a custom subnet mask used (y/N)? ").lower()
        if custom == "y":
            mask = input("Enter custom mask (CIRD): ")
            new_address = add + "/" + mask
            new_net = ip.ip_network(new_address, strict=False)

            print()
            print("The altered network information:")
            network_information(new_net)
            subnet_list = get_subnet_list(orig_net, new_net)
        else:
            subnet_list = get_subnet_list(orig_net)
        subnet_information(subnet_list)

    except ip.AddressValueError:
        print("This is not a valid address.")
        quit()
    except ip.NetmaskValueError:
        print("This is not a valid netmask.")
        quit()


main()
