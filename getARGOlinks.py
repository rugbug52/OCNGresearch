import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os

# === CONFIGURE THESE ===
parent_url = "https://data-argo.ifremer.fr/geo/atlantic_ocean/2019/"  # <-- your real URL here
output_dir = "c:/Users/rugbug/Documents/OCNGresearch/argo_nc_files"
save_links_file = "argo_nc_links.txt"
os.makedirs(output_dir, exist_ok=True)

# === STEP 1: Get list of child subdirectories ===
print(f"Scanning parent directory: {parent_url}")
response = requests.get(parent_url)
soup = BeautifulSoup(response.text, 'html.parser')

subfolders = []

for link in soup.find_all('a'):
    href = link.get('href')
    if href and href.endswith('/') and href != '../':
        subfolders.append(urljoin(parent_url, href))

print(f"Found {len(subfolders)} subfolders.")

# === STEP 2: For each subfolder, collect .nc file links ===
all_nc_links = []

for sub_url in subfolders:
    print(f"Scanning subfolder: {sub_url}")
    sub_response = requests.get(sub_url)
    sub_soup = BeautifulSoup(sub_response.text, 'html.parser')

    for file_link in sub_soup.find_all('a'):
        file_href = file_link.get('href')
        if file_href and file_href.endswith('.nc'):
            full_file_url = urljoin(sub_url, file_href)
            all_nc_links.append(full_file_url)

print(f"Total .nc files found: {len(all_nc_links)}")

# === STEP 3: Save links to file ===
with open(save_links_file, 'w') as f:
    for url in all_nc_links:
        f.write(url + '\n')

print(f"Saved all links to {save_links_file}")

# === STEP 4: Download all .nc files ===
for url in all_nc_links:
    filename = os.path.join(output_dir, os.path.basename(url))
    print(f"Downloading: {url}")
    try:
        r = requests.get(url, stream=True)
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
    except Exception as e:
        print(f"Failed to download {url}: {e}")

print("✅ All downloads complete.")
