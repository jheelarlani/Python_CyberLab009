import sys
import random
import time
import schedule

def monitor_device(host, username, password, device_type="cisco_ios"):
    """
    Simulated SSH connection to a Cisco-like device.
    Generates interface stats and checks for CRC errors.
    """
    print(f"\nConnecting to device {host} as {username}...")
    time.sleep(1)  # simulate connection delay

    # Simulated interface stats
    interfaces = ["GigabitEthernet0/0", "GigabitEthernet0/1", "GigabitEthernet0/2"]
    output = ""
    crc_dict = {}  # store CRC counts per interface

    for intf in interfaces:
        status = random.choice(["up", "down"])
        crc_errors = random.randint(0, 10)  # simulate CRC errors
        drops = random.randint(0, 2)
        output += f"{intf} is {status}\n  {crc_errors} CRC, {drops} drops\n"
        crc_dict[intf] = crc_errors

    print("Interface Stats:\n" + output)

    # Cybersecurity Hook: Check for high CRC errors
    for intf, crc_count in crc_dict.items():
        if crc_count > 5:
            print(f"ALERT: High CRC errors detected on {intf} - potential integrity attack!")

    print("Disconnected from device.")

# -------------------- Scheduler Setup --------------------
def job():
    monitor_device("localhost", "admin", "cisco")

print("Starting scheduled monitoring. Press Ctrl+C to stop.\n")
schedule.every(10).seconds.do(job)  # run every 10 seconds

# Main loop to keep scheduler running
while True:
    schedule.run_pending()
    time.sleep(1)

