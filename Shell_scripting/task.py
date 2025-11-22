import datetime
import socket

print("--- task1 ---")

timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
with open("cyber_log.txt", "a") as log:
    log.write(f"[{timestamp}] System info collected\n")

print("-" * 40)


print("--- task2 ---")

target = "127.0.0.1"
for port in range(20, 1025):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)  
    result = s.connect_ex((target, port))
    if result == 0:
        print(f"Port {port} is OPEN")
    s.close()

print("-" * 40)


print("--- task3 ---")

try:
    open("C:\\Windows\\System32\\config\\SAM")
except PermissionError:
    print("Access denied! Run as administrator.")

print("-" * 40)
