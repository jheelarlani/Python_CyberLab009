import argparse
import threading
import csv
import requests
from bs4 import BeautifulSoup
import time
import re
import smtplib
from email.mime.text import MIMEText


DEFAULT_URL = "https://otx.alienvault.com/"

parser = argparse.ArgumentParser()
parser.add_argument(
    "url",
    nargs="?",               
    default=DEFAULT_URL,      
    help="Target URL for scraping"
)
args = parser.parse_args()
url = args.url

print("\n--- Exercise 1.7: Multi-Threaded IP Scanner with CSV ---")
print(f"Using URL: {url}\n")

# Scraping Logic
try:
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.title.string if soup.title else "No title found"
    print(f"[+] Page title: {title}")

except Exception as e:
    print(f"[ERROR] Scraping failed: {e}")

# Multi-threaded IP scanner
ips = ["192.168.0.1", "192.168.0.10", "8.8.8.8", "1.1.1.1"]
scan_results = []

def ping_ip(ip):
    try:
        r = requests.get(f"http://{ip}", timeout=1)
        status = "Alive"
    except:
        status = "Dead"

    scan_results.append({"IP": ip, "Status": status})
    print(f"Scanned {ip}: {status}")

threads = []
for ip in ips:
    t = threading.Thread(target=ping_ip, args=(ip,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

csv_file = "scan_results.csv"
with open(csv_file, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["IP", "Status"])
    writer.writeheader()
    writer.writerows(scan_results)

print(f"\n[+] Scan results saved to {csv_file}")

print("-" * 40)



print("\n--- Exercise 1.9: Vulnerability Scanner (SQLi + XSS) ---")

DEFAULT_URL = "http://localhost/DVWA/"
parser = argparse.ArgumentParser(description="Vuln Scanner")
parser.add_argument("url", nargs="?", default=DEFAULT_URL, help="Target URL")
args = parser.parse_args()

target_url = args.url
vulns = []

# Fetch Page
try:
    response = requests.get(target_url, timeout=10)
    response.raise_for_status()
except Exception as e:
    print(f"[ERROR] Could not connect: {e}")
    exit()

soup = BeautifulSoup(response.text, 'html.parser')

# SQL Injection Check
if "mysql" in response.text.lower() and "error" in response.text.lower():
    vulns.append("Potential SQL Injection Exposure")


# XSS Detection (Reflected)
def test_xss(target_url):
    payload = "<script>alert(1)</script>"
    test_url = target_url + "?q=" + payload

    try:
        test_resp = requests.get(test_url, timeout=10)
        if payload in test_resp.text:
            return True
    except:
        return False

    return False

if test_xss(target_url):
    vulns.append("Reflected XSS Detected")

# XSS Detection (Stored) — Basic
stored_payload = "<img src=x onerror=alert(1)>"

if stored_payload in response.text:
    vulns.append("Stored XSS Detected")
with open("vuln_report.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Vulnerability", "Description"])
    for vuln in vulns:
        writer.writerow([vuln, "Detected on target application"])
print(f"[DONE] Report saved → vuln_report.csv")
print(f"[INFO] Total issues found: {len(vulns)}")
if vulns:
    print("Vulnerabilities:")
    for v in vulns:
        print(" -", v)
else:
    print("No vulnerabilities detected.")

print("-" * 40)




print("\n--- Exercise 1.8: Threat Feed Monitor ---")

# ---------------------------
# Arguments
# ---------------------------
DEFAULT_URL = "https://lists.blocklist.de/lists/ssh.txt"

parser = argparse.ArgumentParser(description="Threat Feed Monitor")
parser.add_argument("url", nargs="?", default=DEFAULT_URL, help="Threat feed URL")
args = parser.parse_args()
url = args.url

# ---------------------------
# Gmail Alert Configuration
# ---------------------------
SENDER_EMAIL = "yourgmail@gmail.com"
SENDER_PASSWORD = "your_app_password_here"  # Use App Password
RECEIVER_EMAIL = "receiver@gmail.com"

# ---------------------------
# Email Alert Function
# ---------------------------
def send_email(new_iocs):
    body = "New IOCs detected:\n" + "\n".join(new_iocs)
    msg = MIMEText(body)
    msg['Subject'] = "Threat Feed Alert"
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("[EMAIL] Alert sent successfully!")
    except Exception as e:
        print(f"[EMAIL ERROR] {e}")

# ---------------------------
# Scrape IOCs
# ---------------------------
def scrape_iocs(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        text = response.text
        # Extract IP addresses
        iocs = set(re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', text))
        return iocs
    except Exception as e:
        print(f"[ERROR] Fetch failed: {e}")
        return set()

# Main Monitoring Loop
last_iocs = set()

while True:
    iocs = scrape_iocs(url)
    new_iocs = iocs - last_iocs

    if new_iocs:
        # Save to CSV
        with open('iocs.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            for ioc in new_iocs:
                writer.writerow([ioc, time.ctime()])
        print(f"[NEW IOCs] {new_iocs}")

        # Send Gmail alert
        send_email(new_iocs)

    last_iocs = iocs
    print(f"[INFO] Checked at {time.ctime()}. Total IOCs tracked: {len(last_iocs)}")
    time.sleep(20) 
print("-" * 40)



