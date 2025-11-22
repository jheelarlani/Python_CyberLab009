import socket
import sys
from concurrent.futures import ThreadPoolExecutor

def scan_port(target, port):

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        sock.close()

        if result == 0:
            return f"Port {port}: Open"
        return None

    except Exception:
        return None


def port_scan(target, ports):
   
    open_ports = []

    with ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(lambda p: scan_port(target, p), ports)

        for result in results:
            if result:
                open_ports.append(result)

    return open_ports


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python Task1.2.py <target>")
        sys.exit(1)

    target = sys.argv[1]

    # FTP, SSH, Telnet, HTTP, HTTPS, RDP
    common_ports = [21, 22, 23, 80, 443, 3389]

    print(f"Scanning {target} on common ports...\n")

    open_ports = port_scan(target, common_ports)

    if open_ports:
        print("Open ports:")
        for port in open_ports:
            print(port)
    else:
        print("No open ports found.")
