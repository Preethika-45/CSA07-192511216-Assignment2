# Q7 Packet Tracer validation checklist

- [ ] Build the original VLSM campus and save `original_campus.pkt`.
- [ ] Record why a 60-host /26 hostel cannot fit in the remaining 192.168.10.0/24 space.
- [ ] Extend addressing to 192.168.10.0/23 using adjacent 192.168.11.0/24.
- [ ] Configure hostel subnet 192.168.11.0/26; gateway example 192.168.11.1.
- [ ] Test host-to-gateway ping in each subnet.
- [ ] Test permitted inter-subnet ping.
- [ ] Capture `show ip route` and PC `ipconfig` output.
- [ ] Save `redesigned_campus.pkt` and screenshots in this folder.
- [ ] Add measured results to the comparison table below.

| Test | Original /24 | Redesigned /23 |
|---|---|---|
| Hostel /26 allocation | Cannot fit without changes | Fits |
| Existing subnet addresses | Original values | Preserved |
| Hostel gateway ping | Not applicable until readdressing | Record actual result |
| Inter-subnet ping | Record actual result | Record actual result |
