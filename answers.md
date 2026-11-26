# CSA07 – Computer Networks | Assignment 2 – CO2
**Student:** S. Sofiya | **Register Number:** 192521248

## Q1 – Spot the Invalid Addresses

### 1. Address calculations

| Device | Given address | Network address | Broadcast address | Usable host range | Valid host? |
|---|---|---|---|---|---|
| Admission PC | 172.16.45.200/20 | 172.16.32.0 | 172.16.47.255 | 172.16.32.1–172.16.47.254 | Yes |
| Lab printer | 10.0.15.255/21 | 10.0.8.0 | 10.0.15.255 | 10.0.8.1–10.0.15.254 | No – broadcast address |
| X-ray server | 192.168.4.0/23 | 192.168.4.0 | 192.168.5.255 | 192.168.4.1–192.168.5.254 | No – network address |
| Clinic router | 203.0.113.10/29 | 203.0.113.8 | 203.0.113.15 | 203.0.113.9–203.0.113.14 | Yes |

**Traps:** The printer address is the subnet broadcast address. The X-ray server address is the subnet network address. Neither can be assigned to a normal host.

### 2. NAT example
The clinic has 18 devices sharing its public /29 block. One usable public address can be used by the NAT router. Port Address Translation (PAT) distinguishes connections using translated source ports.

| Inside device | Inside source | Public translated source |
|---|---|---|
| PC1 | 192.168.1.10:50000 | 203.0.113.10:40001 |
| PC2 | 192.168.1.11:50000 | 203.0.113.10:40002 |

Both PCs can use local source port 50000 because the NAT router assigns different public-side ports. Return packets are mapped back using the NAT table.

### 3. Datagram switching and virtual circuits
In datagram switching, each packet is routed independently. Packets from the same file may take different paths with different delays, so they can arrive out of order. The receiver reorders them using sequence information at a higher layer such as TCP. In virtual-circuit switching, a logical path is established before data transfer and packets generally follow that path in sequence; path setup is required and a failure on that path can interrupt the connection.

### 4. Alternative: public /27
A /27 contains 32 addresses: 30 usable host addresses. Eighteen separately addressed devices need 18 public host addresses, so a /27 has enough usable addresses, leaving 12 usable addresses spare (assuming the network and broadcast addresses are reserved). The actual monetary cost depends on the ISP's pricing and cannot be calculated from the question. Direct public addressing increases internet exposure and requires stronger firewalling and device security. NAT-related issues such as inbound connection setup, some peer-to-peer applications, and protocols that embed IP/port information may be reduced, but security and address-management responsibilities increase.

**Result:** Two invalid host addresses were identified and NAT/PAT and switching methods were compared.

---

## Q2 – Subnet a Campus That Keeps Growing

### 1. Equal-size subnetting
The largest department needs 100 hosts. It requires at least 102 addresses including network and broadcast, so the smallest suitable equal subnet is /25 (128 total, 126 usable). A /24 can be divided into only two /25 subnets. Therefore, it is **not possible** to give four separate equal-size subnets to Labs, Staff, Library and WAN using only 192.168.10.0/24 while supporting 100 hosts in Labs. If four equal subnets are created, each is /26 with only 62 usable hosts, which fails the Labs requirement.

Illustration of the failed four-way equal split:

| Subnet | Network | Prefix | Usable hosts | Broadcast |
|---|---|---:|---:|---|
| 1 | 192.168.10.0 | /26 | .1–.62 (62) | .63 |
| 2 | 192.168.10.64 | /26 | .65–.126 (62) | .127 |
| 3 | 192.168.10.128 | /26 | .129–.190 (62) | .191 |
| 4 | 192.168.10.192 | /26 | .193–.254 (62) | .255 |

### 2. VLSM allocation (largest requirement first)

| Department | Network/prefix | Mask | First host | Last host | Broadcast |
|---|---|---|---|---|---|
| Labs (100) | 192.168.10.0/25 | 255.255.255.128 | 192.168.10.1 | 192.168.10.126 | 192.168.10.127 |
| Staff (50) | 192.168.10.128/26 | 255.255.255.192 | 192.168.10.129 | 192.168.10.190 | 192.168.10.191 |
| Library (25) | 192.168.10.192/27 | 255.255.255.224 | 192.168.10.193 | 192.168.10.222 | 192.168.10.223 |
| WAN (2) | 192.168.10.224/30 | 255.255.255.252 | 192.168.10.225 | 192.168.10.226 | 192.168.10.227 |

Next free address: **192.168.10.228**.

### 3. Hostel growth trap
A 60-host hostel needs a /26 (62 usable hosts). The remaining range begins at 192.168.10.228 and has only 28 addresses to the end of the /24. It cannot fit a /26 without moving existing subnets or renumbering. A small clean expansion is to obtain the adjacent block 192.168.11.0/24 and treat the campus allocation as 192.168.10.0/23. The hostel can then use **192.168.11.0/26** (hosts 192.168.11.1–192.168.11.62, broadcast 192.168.11.63), without changing the existing subnets. This requires the provider/administrator to make the adjacent address space available and update routing.

### 4. Route summarisation
The four contiguous /24 networks 172.16.8.0/24 through 172.16.11.0/24 combine into **172.16.8.0/22** (mask 255.255.252.0). A /21 summary would cover 172.16.8.0 through 172.16.15.255, including 172.16.12.0/24 through 172.16.15.0/24. If those networks are not actually reachable through the summarising router, traffic for them may be sent to the wrong place or black-holed. Adding 172.16.12.0/24 does not justify changing the summary to /21 unless the whole covered range is correctly routed.

### 5. Why largest-first VLSM?
VLSM allocates the largest block first because it has the strictest alignment and space requirement. Allocating small blocks first can split the available range into fragments and leave no correctly aligned contiguous block for a large subnet.

**Result:** VLSM supports all four original networks; the later 60-host network does not fit in the remaining /24 space.

---

## Q3 – Which Way Will the Packet Go?

### 1. Longest-prefix match

| Destination | Matching best route | Next hop |
|---|---|---|
| 10.1.2.200 | 10.1.2.128/25 | 192.0.2.13 |
| 10.1.2.100 | 10.1.2.0/24 | 192.0.2.9 |
| 10.1.9.9 | 10.1.0.0/16 | 192.0.2.5 |
| 10.7.7.7 | 10.0.0.0/8 | 192.0.2.1 |
| 8.8.8.8 | 0.0.0.0/0 default | 198.51.100.1 |

**Rule:** The router selects the matching route with the longest prefix (most specific network). The default route is used only when no more specific route matches.

### 2. R1 configuration (main link)
```text
enable
configure terminal
hostname R1
interface GigabitEthernet0/0
 ip address 192.168.10.1 255.255.255.0
 no shutdown
exit
interface Serial0/0/0
 ip address 10.0.0.1 255.255.255.252
 clock rate 64000
 no shutdown
exit
ip route 192.168.20.0 255.255.255.0 10.0.0.2
end
write memory
show ip route
```
On R2, configure its LAN as 192.168.20.1/24 and serial interface as 10.0.0.2/30. Add the reverse route:
```text
ip route 192.168.10.0 255.255.255.0 10.0.0.1
```
Set the clock rate only on the DCE end. If the DCE clock rate is missing, the serial link may remain down or fail to come up correctly.

### 3. Floating static backup route
Use a second physical/serial path with a different next hop. Example template on R1 (replace the example backup next hop with the actual address configured on your second link):
```text
ip route 192.168.20.0 255.255.255.0 10.0.0.6 200
```
The administrative distance 200 makes it less preferred than the primary static route (default AD 1). When the primary route becomes unavailable, the backup can be installed, provided the backup interface and next hop are correctly configured. Verify before and after shutdown using `show ip route` and ping.

### 4. Static routing vs OSPF
For two campuses, static routing is simple and needs only a few route commands, while OSPF requires router process/network statements and neighbour formation. With five campuses, static routes grow roughly with the number of remote networks and must be updated manually at each relevant router. OSPF exchanges link-state information and calculates routes automatically, so it is easier to scale and can reconverge after a failure. Exact recovery time depends on timers, topology and simulator settings; measure it in Packet Tracer rather than inventing a value.

**Result:** Next hops were selected using longest-prefix match and static/floating route commands were prepared.

---

## Q4 – Watch Distance-Vector Routing Count to Infinity

### 1. Converged shortest-path table
The Bellman-Ford distance-vector program in `Task04/distance_vector.py` produces:

```text
converged after 4 rounds
A  0  2  5  6 10
B  2  0  3  4  8
C  5  3  0  1  5
D  6  4  1  0  4
E 10  8  5  4  0
```

A's best route to C is A–B–C with cost 2 + 3 = **5**, which is lower than the direct A–C cost of **7**.

### 2. Count-to-infinity example
For X–Y–Z, both links initially cost 1. Before failure, X reaches Z with cost 2 and Y reaches Z with cost 1. When Y–Z fails, if updates are not protected, X may believe Y still has a route and Y may then believe X has a route. Their advertised distances can increase step by step (for example 2, 3, 4, 5, …) until the protocol's defined infinity is reached. This is the count-to-infinity problem. The exact sequence depends on update timing and the protocol's infinity value.

**Split horizon with poison reverse:** A router advertises an unreachable/infinite metric back to the neighbour from which it learned that route. This prevents the two-router feedback loop in this example. RIP uses a finite infinity value of 16, so 16 means unreachable.

### 3. RIP Packet Tracer evidence
Configure RIP version 2 on each router, advertise its directly connected networks, and use `show ip route`, `show ip protocols`, and ping before/after shutting down the C–D link. Save screenshots of the route change and convergence. The actual Packet Tracer result must be captured after execution.

**Result:** The converged distance table and shortest path were identified; count-to-infinity and poison reverse were explained.

---

## Q5 – Why Does OSPF Treat 1 Gbps and 10 Gbps the Same?

### 1. Default OSPF reference bandwidth
OSPF cost = reference bandwidth / interface bandwidth, rounded to an integer with a minimum cost of 1. With default reference bandwidth 100 Mbps:

| Link speed | Calculation | OSPF cost |
|---|---:|---:|
| 10 Mbps | 100/10 | 10 |
| 100 Mbps | 100/100 | 1 |
| 1 Gbps | 100/1000 = 0.1 | 1 (minimum) |
| 10 Gbps | 100/10000 = 0.01 | 1 (minimum) |

Thus, 100 Mbps, 1 Gbps and 10 Gbps can all have cost 1. OSPF cannot distinguish those speeds using the default reference bandwidth.

### 2. New reference bandwidth
Choose **100,000 Mbps (100 Gbps)** on every router:

| Link speed | Calculation | OSPF cost |
|---|---:|---:|
| 10 Mbps | 100000/10 | 10000 |
| 100 Mbps | 100000/100 | 1000 |
| 1 Gbps | 100000/1000 | 100 |
| 10 Gbps | 100000/10000 | 10 |

Cisco IOS template:
```text
router ospf 1
 auto-cost reference-bandwidth 100000
```
Apply the same reference bandwidth on all routers in the OSPF domain.

### 3. Six-router Dijkstra example
Use this illustrative topology with R1 as the source:
- R1–R2 cost 10
- R1–R3 cost 100
- R2–R3 cost 10
- R2–R4 cost 100
- R3–R4 cost 10
- R3–R5 cost 100
- R4–R5 cost 10
- R5–R6 cost 10
- R4–R6 cost 100

Shortest paths from R1:
- R2 = 10 via R2
- R3 = 20 via R2
- R4 = 30 via R2–R3
- R5 = 40 via R2–R3–R4
- R6 = 50 via R2–R3–R4–R5

Dijkstra repeatedly chooses the unvisited router with the lowest tentative cost and relaxes the costs to its neighbours.

### 4. Area design and alternatives
For a small provider network, one area (Area 0) is simple. For a larger multi-city provider, use a hierarchical design with a backbone Area 0 and regional areas to reduce the size of link-state databases and contain some topology changes. EIGRP uses a composite metric mainly based on bandwidth and delay (with default K values); IS-IS also uses configurable link metrics. Their exact metrics cannot be computed from bandwidth alone without all required interface metric inputs and protocol settings. They can avoid this specific OSPF reference-bandwidth configuration issue only if their metrics are configured to distinguish the paths appropriately.

**Result:** The default OSPF cost limitation was demonstrated and a consistent 100-Gbps reference bandwidth was selected.

---

## Q6 – IPv6, ICMP, Multicast and SDN in a Smart City

### 1. IPv6 shortest form
Given: `2001:0db8:0000:0000:0000:ff00:0042:8329`  
Shortest form: **`2001:db8::ff00:42:8329`**

### 2. EUI-64
MAC: `00:1A:2B:3C:4D:5E`
1. Split: `00:1A:2B` and `3C:4D:5E`
2. Insert `FF:FE`: `00:1A:2B:FF:FE:3C:4D:5E`
3. Flip the U/L bit in first byte: `00` becomes `02`
4. Interface identifier: **`021A:2BFF:FE3C:4D5E`**

### 3. Traceroute and ICMP
Traceroute sends probes with gradually increasing TTL (IPv4) or Hop Limit (IPv6). Each router decreases the value. When it reaches zero, the router discards the probe and sends an ICMP Time Exceeded message to the source. The source records the responding router and increases TTL to discover the next hop.

### 4. IPv4 multicast MAC
For IPv4 multicast group `239.1.2.3`, the Ethernet multicast MAC is **`01:00:5E:01:02:03`**. The low 23 bits of the IPv4 multicast address are mapped into the Ethernet multicast address. Multicast routers/switches replicate packets in the network toward interested receiver ports, so the camera sends one multicast stream rather than creating a separate unicast stream for every control room.

### 5. OpenFlow decisions
- HTTP packet to destination `10.5.1.1`: the destination matches `10.5.0.0/16` at priority 200, so it is forwarded to **port 3**. This higher-priority rule wins over the TCP port 80 controller rule.
- SSH packet to destination `10.6.1.1`: it does not match `10.5.0.0/16` or TCP port 80, so the priority-0 rule **drops** it.

**SDN judgement:** SDN is useful for centralised policy, automation and consistent traffic control across many city devices. Trade-offs include controller availability/security, operational complexity and the need for staff skills. Redundant controllers and secure control channels are important.

### 6. IPv6 transition
A 6in4 tunnel adds an outer IPv4 header of normally 20 bytes (without IPv4 options). A 100-byte IPv6 packet therefore becomes **120 bytes** before link-layer overhead. Native IPv6 avoids this tunnel overhead but requires end-to-end IPv6 readiness. Dual-stack is a practical gradual migration when devices and services support both protocols; tunnelling is useful when IPv6 must cross an IPv4-only segment.

**Result:** IPv6 compression, EUI-64, ICMP traceroute, multicast MAC and OpenFlow actions were calculated.

---

## Q7 – Find the Weak Point, Redesign and Validate

### A. Limitation
Select the campus addressing design in Q2. The original `192.168.10.0/24` VLSM plan uses:
- Labs: .0–.127
- Staff: .128–.191
- Library: .192–.223
- WAN: .224–.227

Only 28 addresses remain (.228–.255), so a new 60-host hostel subnet requiring a /26 cannot fit.

### B. Measurable objective
Provide at least 60 usable host addresses for the hostel without changing any existing subnet addresses.

### C. Revised design
Obtain the adjacent `192.168.11.0/24` block and use the combined aligned range `192.168.10.0/23`.

| Network | Subnet | Usable range |
|---|---|---|
| Labs | 192.168.10.0/25 | 192.168.10.1–192.168.10.126 |
| Staff | 192.168.10.128/26 | 192.168.10.129–192.168.10.190 |
| Library | 192.168.10.192/27 | 192.168.10.193–192.168.10.222 |
| WAN | 192.168.10.224/30 | 192.168.10.225–192.168.10.226 |
| Hostel | 192.168.11.0/26 | 192.168.11.1–192.168.11.62 |

Topology (logical):
```text
                    Campus Router
                          |
       -----------------------------------------
       |          |          |         |        |
      Labs      Staff     Library     WAN    Hostel
     /25        /26        /27        /30      /26
 192.168.10  192.168.10 192.168.10 192.168.10 192.168.11
```

Trade-off: The organisation must obtain and route the additional adjacent /24 block. The address plan becomes larger, but the existing departments do not need renumbering.

### D. Prediction
The revised design will provide 62 usable hostel addresses (at least 60) while preserving the existing four subnet ranges.

### E. Implementation and validation plan
In Packet Tracer, configure the original four networks and attempt to allocate a /26 hostel subnet; record that the remaining range is insufficient. Then configure the expanded /23 plan and hostel VLAN/interface using `192.168.11.1/26`. Test:
1. Ping between each department and its default gateway.
2. Ping from a hostel PC to the campus gateway.
3. Ping between hostel and an authorised existing department.
4. Check masks and routes using `ipconfig` and `show ip route`.

Save the two `.pkt` files and screenshots in `Task07/`. Do not mark validation as completed until these tests have actually been run.

### F. Final judgement
The redesign achieves the objective on paper: the hostel has 62 usable addresses and existing subnets remain unchanged. The cost is obtaining another adjacent /24 and updating routing/documentation. If the college cannot obtain more address space, it must redesign or renumber existing subnets. The original /24 remains preferable when the campus has no growth requirement and wants to conserve address space.

**Result:** The address-exhaustion limitation was identified and a measurable, expandable VLSM redesign was proposed.
