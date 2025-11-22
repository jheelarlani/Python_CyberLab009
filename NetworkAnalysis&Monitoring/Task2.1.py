from scapy.all import sniff, IP, TCP, UDP, get_if_list
import sys

def packet_handler(packet):
    """Handle each captured packet: Print source/dest IP and protocol."""
    if IP in packet:
        ip_layer = packet[IP]

        if TCP in packet:
            proto = "TCP"
            ports = f"{packet[TCP].sport} -> {packet[TCP].dport}"
        elif UDP in packet:
            proto = "UDP"
            ports = f"{packet[UDP].sport} -> {packet[UDP].dport}"
        else:
            proto = "Other"
            ports = "N/A"

        print(f"IP: {ip_layer.src} -> {ip_layer.dst} | Protocol: {proto} | Ports: {ports}")

        if proto == "TCP" and packet[TCP].dport == 4444:
            print("ALERT: Potential malicious traffic on port 4444!")

def sniff_packets(interface, count=10, flt=None):
    """Sniff packets on interface for 'count' packets, with optional filter."""
    print(f"Sniffing on interface: {interface} for {count} packets...")
    if flt:
        print(f"Applying filter: {flt}")
    sniff(iface=interface, prn=packet_handler, count=count, filter=flt)

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Available Interfaces:")
        for iface in get_if_list():
            print(" -", iface)
        print("\nUsage: python Task2.1.py <InterfaceName>")
        sys.exit()

    interface = sys.argv[1]  # e.g., "Wi-Fi" or "Ethernet"

    # Optional: set IP filter for extension
    flt = "host 8.8.8.8"  # Only capture packets to/from 8.8.8.8
    # flt = None          # Uncomment this line to capture all packets

    sniff_packets(interface=interface, count=10, flt=flt)
