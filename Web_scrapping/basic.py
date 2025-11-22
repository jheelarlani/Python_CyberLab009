import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# Exercise 1.1: Basic Page Scraper

print("--- Exercise 1.1: Basic Page Scraper ---")
url1 = "https://krebsonsecurity.com/"

try:
    response = requests.get(url1)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')    
    title = soup.title.string.strip()
    print(f"Page Title: {title}")
    links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('http')]
    print("External Links (first 5):")
    for link in links[:5]:
        print(link)
except requests.RequestException as e:
    print(f"Failed to fetch {url1}: {e}")

print("-" * 40)

# Exercise 1.2: Directory Checker

print("--- Exercise 1.2: Directory Checker ---")
url2 = "http://localhost/DVWA/"
dirs = ["/admin", "/login", "/config"]

for d in dirs:
    try:
        response = requests.get(url2 + d)
        print(f"[{response.status_code}] {url2 + d}")
    except requests.RequestException:
        print(f"[Error] Could not access {url2 + d}")

print("-" * 40)


# Exercise 1.3: Simple Link Extractor

print("--- Exercise 1.3: Simple Link Extractor ---")
url3 = "https://krebsonsecurity.com/" 
output_file = "krebsonsecurity_links.txt"
try:
    response = requests.get(url3)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    links = [a['href'] for a in soup.find_all('a', href=True)]
    print("Links Found (first 5):")
    for link in links[:5]:
        print(link)
    with open(output_file, "w") as f:
        for link in links:
            f.write(link + "\n")
    print(f"All links saved to {output_file}")

except requests.RequestException as e:
    print(f"Failed to fetch {url3}: {e}")

print("-" * 40)
