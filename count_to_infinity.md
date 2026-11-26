# Count-to-infinity lab notes

For X–Y–Z, each link cost is 1. Initially X's distance to Z is 2 and Y's is 1. Shut down Y–Z. Without split horizon/poison reverse, X and Y can feed stale routes to one another and increase their advertised metric. RIP treats metric 16 as infinity/unreachable. Split horizon with poison reverse advertises an infinite metric back toward the neighbour from which the route was learned, preventing this two-router loop. Capture the actual Packet Tracer update sequence; the exact intermediate sequence depends on update timing.
