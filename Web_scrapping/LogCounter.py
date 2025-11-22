import re


log_filename = "dummy_access.log"

log_content = """
192.168.1.1 - - [01/Oct/2025:12:00:00] "GET /login" 200
10.0.0.5 - - [01/Oct/2025:12:01:00] "POST /admin" 403
192.168.1.1 - - [01/Oct/2025:12:02:00] "GET /home" 200
8.8.8.8 - - [01/Oct/2025:12:03:00] "GET /" 200
10.0.0.5 - - [01/Oct/2025:12:04:00] "POST /admin" 403
"""

with open(log_filename, "w") as f:
    f.write(log_content)

# Regex patterns
ip_pattern = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
timestamp_pattern = r'\[(.*?)\]'

unique_ips = set()
log_entries = []

# Parse log file
with open(log_filename, 'r') as f:
    for line in f:
        ip_match = re.search(ip_pattern, line)
        ts_match = re.search(timestamp_pattern, line)
        if ip_match and ts_match:
            ip = ip_match.group(1)
            ts = ts_match.group(1)
            unique_ips.add(ip)
            log_entries.append((ip, ts))


print(f"Unique IPs ({len(unique_ips)}):")
for ip in unique_ips:
    print(f"  - {ip}")

print("\nAll log entries with timestamps:")
for entry in log_entries:
    print(f"  - IP: {entry[0]} | Timestamp: {entry[1]}")
