import datetime
import getpass
# ----------------------------------------
# Cyber Lab - Basic Python Scripting
# ----------------------------------------

# Exercise 1.1: Hello World
print("--- Exercise 1.1 ---")
print("Hello, Cybersecurity World!")
print("-" * 40)

# Exercise 1.2: User Input
print("--- Exercise 1.2 ---")
name = input("Enter your name: ")
print(f"Hello, {name}!")
print("-" * 40)

# Exercise 1.3: File Operations (Advanced Log)
print("--- Exercise 1.3 ---")

# Prepare log details
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
user = getpass.getuser()
script_name = "cyber_lab_script.py"
message = "Script executed successfully"

# Write log entry
with open("cyber_log.txt", "a") as file:
    file.write(f"[{timestamp}] User: {user} | Script: {script_name} | Status: {message}\n")

print("Advanced log entry written to cyber_log.txt")
print("-" * 40)
