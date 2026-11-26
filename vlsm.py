"""Variable-length subnetting (VLSM) of 192.168.10.0/24 for a college campus."""
import math
import ipaddress

def vlsm(base, needs):
    addr = int(ipaddress.IPv4Address(base))
    for name, hosts in sorted(needs, key=lambda x: -x[1]):
        # Find smallest power-of-two block for hosts + network + broadcast.
        block = 1 << math.ceil(math.log2(hosts + 2))
        prefix = 32 - int(math.log2(block))
        # Align the next network address to the block boundary.
        addr = ((addr + block - 1) // block) * block
        network = ipaddress.IPv4Network((addr, prefix))
        first = network.network_address + 1
        last = network.broadcast_address - 1
        print(f"{name:<14} {network.network_address}/{prefix} "
              f"hosts {first} - {last} bcast {network.broadcast_address}")
        addr = int(network.broadcast_address) + 1
    return str(ipaddress.IPv4Address(addr))

if __name__ == "__main__":
    needs = [("Labs", 100), ("Staff", 50), ("Library", 25), ("WAN link", 2)]
    print("next free address:", vlsm("192.168.10.0", needs))
