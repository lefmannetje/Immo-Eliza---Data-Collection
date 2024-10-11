import get_all_urls
import scraper
import listings
from datetime import datetime, timedelta

# Record the start time when the code starts
start_time = datetime.now()
print("Start Time:", start_time.strftime("%Y-%m-%d %H:%M:%S"))

# Function to print the elapsed time since start
def print_elapsed_time():
    current_time = datetime.now()
    elapsed_time = current_time - start_time
    return str(elapsed_time)

# Define the filename
filename = "classified_ids.txt"

# Define base_url and headers to be able to get the data from the correct website (immoweb.be/{id})
base_url = 'https://www.immoweb.be/en/classified/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.immoweb.be/',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0'
}

# Fill classified_ids.txt with all urls 
get_all_urls.get_urls(filename)

# loop over all url's and get data from it
try:
    # Open our file with all the IDs in, they are gonna be put behind the baseURL to grab correct website
    with open(filename, 'r') as urls:
        # for each found id in the txt file, we are going to take each one by one and call the scrape function from the scraper.py file
        for url in urls:
            data = scraper.scrape(base_url+url.strip(), headers)
            # We going to store all data from the website to a csv file by parsing it through the Listing class
            listings.Listing.store_data(data)

            # print the amount of lisitngs scraped
            counter = listings.Listing.get_instance_count()
            print("We stored ", counter, " listings. Time passed: ", print_elapsed_time())
except FileNotFoundError:
    print(f"{filename} does not exist. Please check the file name and path.")

