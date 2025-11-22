import sys
import hashlib
import psutil
import re
from cryptography.fernet import Fernet
import sys

# ----------------------------------------
# Cyber Lab - Advanced Python Scripting
# ----------------------------------------

print("--- Exercise 3.1 ---")

# Default argument if none provided
if len(sys.argv) > 1:
    argument = sys.argv[1]
else:
    argument = "HelloWorld"  # Bydefault

print(f"Argument: {argument}")
hash_obj = hashlib.sha256(argument.encode())
print(f"SHA256: {hash_obj.hexdigest()}")
print("-" * 40)


# Exercise 3.2: Process Monitoring
print("--- Exercise 3.2 ---")

print("Running Processes:")
for proc in psutil.process_iter(['pid', 'name']):
    print(f"PID: {proc.info['pid']}, Name: {proc.info['name']}")

print("-" * 40)


# Exercise 3.3: Log Analyzer
print("--- Exercise 3.3 ---")

def analyze_log(filename, keyword="error"):
    try:
        with open(filename, "r") as file:
            content = file.read()
            matches = re.findall(keyword, content, re.IGNORECASE)
            print(f"Found {len(matches)} '{keyword}' occurrences in {filename}.")
    except FileNotFoundError:
        print(f"File {filename} not found.")

# Example usage:
analyze_log("cyber_log.txt", "error")

print("-" * 40)


print("--- Exercise 3.4 ---")

if len(sys.argv) < 2:
    print("Usage: python encrypt_file.py <filename>")
    sys.exit(1)
filename = sys.argv[1]
key = Fernet.generate_key()
cipher = Fernet(key)
with open(filename, "rb") as file:
    data = file.read()
encrypted_data = cipher.encrypt(data)

with open(filename + ".enc", "wb") as file:
    file.write(encrypted_data)

print(f"File encrypted successfully: {filename}.enc")
print(f"Encryption Key (keep it safe!): {key.decode()}")
print("-" * 40)
