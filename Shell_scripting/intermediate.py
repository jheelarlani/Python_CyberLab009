import os
import subprocess

# ----------------------------------------
# Cyber Lab - Intermediate Python Scripting
# ----------------------------------------

# Exercise 2.1: File Existence Check
print("--- Exercise 2.1 ---")

filename = "cyber_log.txt"

if os.path.exists(filename):
    print(f"File {filename} exists.")
else:
    print(f"File {filename} does not exist.")

print("-" * 40)


# Exercise 2.2: Directory Listing
print("--- Exercise 2.2 ---")

print("Files in current directory:")
for file in os.listdir("."):
    print(file)

print("-" * 40)


# Exercise 2.3: System Commands Execution
print("--- Exercise 2.3 ---")

try:
    result = subprocess.run(["ipconfig"], capture_output=True, text=True)
    print("Network Info:\n" + result.stdout)
except Exception as e:
    print(f"Error: {e}")

print("-" * 40)
