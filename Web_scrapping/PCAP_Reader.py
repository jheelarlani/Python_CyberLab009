#!/usr/bin/env python
from scapy.all import rdpcap

# Replace this with your PCAP file path
pcap_file = "sample.pcap"

try:
    packets = rdpcap(pcap_file)
    print(f"Loaded {len(packets)} packets from {pcap_file}\n")
    
    # Print summary of first 5 packets
    for pkt in packets[:5]:
        print(pkt.summary())

except FileNotFoundError:
    print(f"Error: PCAP file '{pcap_file}' not found. Please provide a valid PCAP file.")
except Exception as e:
    print(f"An error occurred: {e}")
