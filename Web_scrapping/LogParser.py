import re
import csv

# ---------------------------
# Step 1: Create a dummy log file
# ---------------------------
log_filename = "dummy_access.log"

log_content = """
192.168.1.1 - - [01/Oct/2025:12:00:00] "GET /login" 200
10.0.0.5 - - [01/Oct/2025:12:01:00] "POST /admin" 403
192.168.1.1 - - [01/Oct/2025:12:02:00] "GET /home" 200
8.8.8.8 - - [01/Oct/2025:12:03:00] "GET /" 200
10.0.0.5 - - [01/Oct/2025:12:04:00] "POST /admin" 403
"""

try:
    with open(log_filename, "w") as f:
        f.write(log_content.strip())
    print(f"Created '{log_filename}' for parsing.")
except Exception as e:
    print(f"Error creating log file: {e}")

# ---------------------------
# Step 2: Define patterns
# ---------------------------
ip_pattern = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
timestamp_pattern = r'\[(.*?)\]'
status_pattern = r'"\s(\d{3})'

# ---------------------------
# Step 3: Parse the log file
# ---------------------------
log_entries = []

try:
    with open(log_filename, 'r') as f:
        for line in f:
            ip_match = re.search(ip_pattern, line)
            time_match = re.search(timestamp_pattern, line)
            status_match = re.search(status_pattern, line)
            
            if ip_match and time_match and status_match:
                log_entries.append({
                    "IP": ip_match.group(1),
                    "Timestamp": time_match.group(1),
                    "Status": status_match.group(1)
                })

except FileNotFoundError:
    print(f"Error: Log file '{log_filename}' not found.")
except Exception as e:
    print(f"An error occurred: {e}")

# ---------------------------
# Step 4: Display unique IPs and counts
# ---------------------------
unique_ips = set(entry["IP"] for entry in log_entries)
print("\nUnique IPs found:")
for ip in unique_ips:
    print(f"  - {ip}")

# Optional: Count status codes per IP
status_count = {}
for entry in log_entries:
    key = (entry["IP"], entry["Status"])
    status_count[key] = status_count.get(key, 0) + 1

print("\nIP-wise Status Counts:")
for (ip, status), count in status_count.items():
    print(f"IP: {ip}, Status: {status}, Count: {count}")

# ---------------------------
# Step 5: Save results to CSV
# ---------------------------
csv_filename = "parsed_log.csv"
try:
    with open(csv_filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["IP", "Timestamp", "Status"])
        writer.writeheader()
        writer.writerows(log_entries)
    print(f"\nLog data saved to '{csv_filename}' successfully.")
except Exception as e:
    print(f"Error writing CSV: {e}")
