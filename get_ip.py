import os
import sys
import re
import netifaces as ni
import ipaddress

ip = str(ni.ifaddresses('wlo1')[ni.AF_INET][0]['addr'])
netmask = str(ni.ifaddresses('wlo1')[ni.AF_INET][0]['netmask'])

net = ipaddress.ip_network(str(ip + "/" + netmask), strict=False)
network_address = net.network_address

count_netmask = str(netmask).split(".").count("255")
network_address = str(network_address).split(".")[0:count_netmask]
network_address = ".".join(network_address)


def get_os() -> str:
    return os.name


def ping_network(ip_network: str):
    cmd = ""
    if get_os() == "posix":
        cmd = "ping -f"
    if get_os() == "nt":
        cmd = "ping -f "
    for i in range(255):
        os.system(cmd + " " + ip_network + "." + str(i) + " > /dev/null")


def get_ip_from_arp_table(mac: str) -> str:
    re_ip_pattern = "([0-9]{1,3}[\.]){3}[0-9]{1,3}"
    if get_os() == "posix":
        if mac.find("-"):
            mac = mac.replace("-", ":")
        ip = re.search(re_ip_pattern, str(os.popen("arp -a | grep " + mac, "r").read()))
    if get_os() == "nt":
        if mac.find(":"):
            mac = mac.replace(":", "-")
        ip = re.search(re_ip_pattern, str(os.popen("arp -a | findstr " + mac, "r").read()))
    return ip.group()


ERROR_MSG = '''
    ERROR\n
    python3 get_ip.py MAC\n
    python3 get_ip.py 98-da-c4
'''


def main():
    try:
        mac = sys.argv[1]
        ping_network(network_address)
        print(get_ip_from_arp_table(mac))
    except Exception as e:
        print(ERROR_MSG + str(e))


if __name__ == '__main__':
    main()
