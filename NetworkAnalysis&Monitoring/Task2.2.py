from scapy.all import IP, ICMP, send

def craft_icmp(target, ttl=64):
    """
    Craft and send ICMP echo request.
    """
    packet = IP(dst=target, ttl=ttl) / ICMP()
    print(f"Sending ICMP to {target} with TTL {ttl}")
    response = send(packet, verbose=1)
    return response

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python icmp_craft.py <target>")
        sys.exit(1)

    target = sys.argv[1]
    craft_icmp(target)
