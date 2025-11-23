import os
os.environ["PATH"] += os.pathsep + r"C:\Program Files (x86)\Nmap"
import nmap
import psutil
import time
import sys
from statistics import mean, stdev

# -------------------- Network Scanning --------------------
def scan_hosts(network):
    """
    Scan network for live hosts using Nmap ping scan.
    """
    nm = nmap.PortScanner()
    nm.scan(hosts=network, arguments='-sn')  # Ping scan
    hosts = []
    for host in nm.all_hosts():
        if nm[host].state() == 'up':
            hosts.append(host)
    return hosts

# -------------------- Traffic Monitoring --------------------
def monitor_traffic(interface="Wi-Fi", duration=60, interval=5):
    """
    Monitor bytes sent/received over time.
    Detect anomalies if deviation > 2 std devs.
    """
    stats = []
    print(f"Monitoring interface {interface} for {duration}s...")
    start_time = time.time()

    # Capture stats over time
    while time.time() - start_time < duration:
        net_io = psutil.net_io_counters(pernic=True).get(interface)
        if not net_io:
            print(f"Interface {interface} not found!")
            return
        stats.append((net_io.bytes_sent, net_io.bytes_recv))
        time.sleep(interval)

    # Calculate rate of change per interval
    sent_rates = [stats[i][0] - stats[i-1][0] for i in range(1, len(stats))]
    recv_rates = [stats[i][1] - stats[i-1][1] for i in range(1, len(stats))]

    # Detect anomalies in outbound traffic
    if len(sent_rates) > 1:
        sent_mean, sent_std = mean(sent_rates), stdev(sent_rates)
        if any(rate > sent_mean + 2 * sent_std for rate in sent_rates):
            print("ALERT: Unusual outbound traffic spike detected!")
        print(f"Outbound Avg: {sent_mean:.2f} bytes/interval, Std: {sent_std:.2f}")

    # Detect anomalies in inbound traffic
    if len(recv_rates) > 1:
        recv_mean, recv_std = mean(recv_rates), stdev(recv_rates)
        if any(rate > recv_mean + 2 * recv_std for rate in recv_rates):
            print("ALERT: Unusual inbound traffic spike detected!")
        print(f"Inbound Avg: {recv_mean:.2f} bytes/interval, Std: {recv_std:.2f}")

    return stats

# -------------------- Main --------------------
if __name__ == "__main__":
    network = sys.argv[1] if len(sys.argv) > 1 else '192.168.1.0/24'
    interface = sys.argv[2] if len(sys.argv) > 2 else "Wi-Fi"

    print("Scanning hosts...")
    live_hosts = scan_hosts(network)
    print(f"Live hosts detected: {live_hosts}")

    monitor_traffic(interface=interface, duration=60, interval=5)

