import requests
import xml.etree.ElementTree as ET
import re
import os
import json

# Base sitemap URL
main_sitemap_url = "https://www.immoweb.be/sitemap.xml"
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
}

# Get all valid URL's from immoweb.be by looking at sitemap.xml
def get_urls(filename):
    # Check if the file exists otherwise make file so we have all ID's to scrape
    if os.path.exists("classified_ids.txt"):
        print(f"{filename} already exists. No need to find ID's")
    else:
        print(f"{filename} does not exist. A new file will be created when saving IDs.")
        # Get the classified sitemap URLs from the main sitemap
        sitemap_urls = get_classified_sitemap_urls()

        print(sitemap_urls)

        # Loop through all classified sitemap files and collect IDs
        all_ids = []
        for sitemap_url in sitemap_urls:
            ids = fetch_ids_from_sitemap(sitemap_url)
            all_ids.extend(ids)
            save_ids_to_file(ids)

        #remove duplicates form list    
        remove_duplicates_and_sort()

# Function to get all classified sitemap URLs
def get_classified_sitemap_urls():
    response = requests.get(main_sitemap_url, headers=headers)
    classified_urls = []
    if response.status_code == 200:
        # Parse the XML
        root = ET.fromstring(response.content)
        
        # Define the namespace and find all <loc> under <sitemap> in <sitemapindex>
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        # Extract all URLs with "classifieds" in them
        for loc in root.findall('ns:sitemap/ns:loc', namespace):
            loc_text = loc.text
            if "classifieds" in loc_text:
                classified_urls.append(loc_text)
    else:
        print(f"Failed to retrieve main sitemap from {main_sitemap_url}")
    return classified_urls

# Function to fetch and parse IDs from a sitemap XML file
def fetch_ids_from_sitemap(url):
    response = requests.get(url)
    print(url)
    ids = set()  # Use a set instead of a list to automatically remove duplicates
    if response.status_code == 200:
        print(f"Successful to retrieve {url}")
        root = ET.fromstring(response.content)
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
       
        for loc in root.findall('ns:url/ns:loc', namespace):
            match = re.search(r'/(\d+)$', loc.text)
            if match:
                ids.add(match.group(1))  # Add to set instead of appending to list
    else:
        print(f"Failed to retrieve {url}")
    return ids

# Define a function to save IDs to a text file
def save_ids_to_file(ids, filename="classified_ids.txt"):
    with open(filename, 'a') as file:
        for id in ids:
            file.write(f"{id}\n")
    print(f"Successfully saved {len(ids)} IDs to {filename}")

# Will try to remove all duplicate ID's in file and also sort alfabeticly so we always have the same scrape
def remove_duplicates_and_sort(filename="classified_ids.txt"):
    # Read all lines from the file
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    # Remove duplicates and strip whitespace
    unique_lines = set(line.strip() for line in lines)
    
    # Sort the unique lines
    sorted_lines = sorted(unique_lines)
    
    # Write the sorted, unique lines back to the file
    with open(filename, 'w') as file:
        for line in sorted_lines:
            file.write(line + '\n')
    
    print(f"Removed duplicates and sorted {len(sorted_lines)} unique lines in {filename}")