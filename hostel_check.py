import ipaddress

existing = [
    ipaddress.ip_network("192.168.10.0/25"),
    ipaddress.ip_network("192.168.10.128/26"),
    ipaddress.ip_network("192.168.10.192/27"),
    ipaddress.ip_network("192.168.10.224/30"),
]
hostel = ipaddress.ip_network("192.168.10.228/26", strict=False)
print("Remaining addresses in original /24:", 256 - 228)
print("A /26 needs 64 total addresses and 62 usable hosts.")
print("Hostel /26 candidate in original /24:", hostel)
print("Overlaps existing:", any(hostel.overlaps(n) for n in existing))
print("Expanded-block hostel subnet:", ipaddress.ip_network("192.168.11.0/26"))
