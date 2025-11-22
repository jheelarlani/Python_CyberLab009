import requests
import argparse
import csv
import re
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


# Exercise 1.4: IP Scraper from Blocklist.de 

print("--- Exercise 1.4: IP Scraper ---")

default_url = "https://lists.blocklist.de/lists/ssh.txt"
parser = argparse.ArgumentParser(description="Scrape IPs from threat feed (Blocklist.de SSH list)")
parser.add_argument("url", nargs='?', default=default_url, help="URL to scrape (optional, uses default if not given)")
args = parser.parse_args()
url = args.url
print(f"Using URL: {url}")

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
try:
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"[!] Error fetching URL: {e}")
    sys.exit(1)

text = response.text.strip()
ips = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', text)
unique_ips = sorted(list(set(ips)))

csv_file = 'malicious_ips.csv'
with open(csv_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Malicious IP'])
    for ip in unique_ips[:100]: 
        writer.writerow([ip])

print(f"[+] Total IPs found: {len(unique_ips)}")
print(f"[+] First 100 IPs saved to {csv_file}")

print("-" * 40)

print("\n--- Exercise 1.5: Form Tester ---")

target_url = "http://localhost/DVWA/vulnerabilities/brute/"
payloads = [
    "admin",
    "test' OR '1'='1",
    "<script>alert(1)</script>"
]

print(f"Testing form at: {target_url}")

for payload in payloads:
    data = {"username": payload, "password": "test"}

    try:
        response = requests.post(target_url, data=data, timeout=5)
        print(f"\n[+] Payload: {payload}")
        print(f"Status: {response.status_code}")

        if "error" not in response.text.lower():
            print("[!] Possible vulnerability detected!")
        else:
            print("[-] Login failed as expected.")

    except Exception as e:
        print(f"[ERROR] {e}")

print("-" * 40)


print("\n--- Exercise 1.6: Dynamic Selenium Scraper ---")

def scrape_dynamic_page(url):
    print(f"--- Dynamically scraping {url} with Selenium ---")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.92 Safari/537.36"
    )
    
    driver = None
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print("Driver initialized. Navigating to page...")
        driver.get(url)
        
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        links = soup.find_all('a', href=True)
        
        print(f"\n[SUCCESS] Page parsed. Found {len(links)} links.")
        print("Showing first 10 unique links:")
        
        unique_links = set()
        for link in links:
            href = link['href']
            if href.startswith('http'):
                unique_links.add(href)
        
        for link in list(unique_links)[:10]:
            print(f"  - {link}")

    except Exception as e:
        print(f"\n[ERROR] Something went wrong: {e}")
    finally:
        if driver:
            driver.quit()
            print("\nBrowser driver closed.")

if __name__ == "__main__":
    target_url = "https://otx.alienvault.com/"
    scrape_dynamic_page(target_url)

print("-" * 40)