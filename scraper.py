import requests
import json
import re
import mysql.connector
import listings

# MySQL connection
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  db = "immo"
)


# url scrapper
def scrape(url, headers):
    # Get all data from the url and place it in response variable
    response = requests.get(url, headers=headers)
    
    #check if we got a status code of 200 back, if not website wont let us grab content
    if response.status_code == 200:    
        # Use regex to find the window.classified content
        match = re.search(r'window\.classified\s*=\s*({.*?});', response.text, re.DOTALL)
        
        if match:
            # Extract the JSON string
            json_str = match.group(1)
            
            try:
                # Parse the JSON string
                classified_data = json.loads(json_str)
                
                # Check if the data is worth storing to db
                # ingore Rent, Type of sale:exclude life sales)
                if safe_get(classified_data, 'transaction', "type") != "FOR_SALE" or safe_get(classified_data, 'transaction', 'subtype') == 'LIFE_ANNUITY':
                    # print("Not the right sale or type")
                    # TODO: nice to have. make an ignore list so we can ignore these urls all together when scraping again
                    # def make_ignore_id_list():
                    return
                else:
                    # Extract the data
                    property_id = safe_get(classified_data, 'id')
                    #print(property_id)                                                                  # here to see what ID's has been scraped
                    summary = safe_get(classified_data, 'property', 'description')
                    locality = safe_get(classified_data, 'property', 'location', 'locality')
                    postal = safe_get(classified_data, 'property', 'location', 'postalCode')
                    address = safe_get(classified_data, 'property', 'location', 'street')
                    region = safe_get(classified_data, 'property', 'location', 'region')
                    country = safe_get(classified_data, 'property', 'location', 'country')
                    price = safe_get(classified_data, 'transaction', 'sale', 'price')
                    property_type = safe_get(classified_data, 'property', 'type')
                    sub_property_type = safe_get(classified_data, 'property', 'subtype')
                    sale_type = safe_get(classified_data, 'transaction', 'type')
                    number_of_bedrooms = safe_get(classified_data, 'property', 'bedroomCount')
                    living_area = safe_get(classified_data, 'property', 'netHabitableSurface')
                    kitchen = safe_get(classified_data, 'property', 'kitchen')
                    attic = safe_get(classified_data, 'property', 'hasAttic')
                    basement = safe_get(classified_data, 'property', 'hasBasement')
                    furnished = safe_get(classified_data, 'transaction', 'isFurnished')
                    open_fire = safe_get(classified_data, 'property', 'fireplaceExists')
                    terrace = safe_get(classified_data, 'property', 'hasTerrace')
                    terrace_area = safe_get(classified_data, 'property', 'terraceSurface')
                    terrace_orientation = safe_get(classified_data, 'property', 'terraceOrientation')
                    garden = safe_get(classified_data, 'property', 'hasGarden')
                    garden_area = safe_get(classified_data, 'property', 'gardenSurface')
                    garden_orientation = safe_get(classified_data, 'property', 'gardenOrientation')
                    number_of_facades = safe_get(classified_data, 'property', 'building', 'facadeCount')
                    construction_year = safe_get(classified_data, 'property', 'building', 'constructionYear')
                    swimming_pool = safe_get(classified_data, 'property', 'hasSwimmingPool')
                    state_of_building = safe_get(classified_data, 'property', 'building', 'condition')
                    epc = safe_get(classified_data, 'property', 'propertyCertificates', 'primaryEnergyConsumptionLevel')
                    kwh = safe_get(classified_data, 'transaction', 'certificates', 'primaryEnergyConsumptionPerSqm')
                
                    #make instance of Class Properties and fill it.
                    listing = listings.Listing(property_id, summary, locality, postal, address, region, 
                               country, price, property_type, sub_property_type, sale_type, 
                               number_of_bedrooms, living_area, kitchen, attic, basement,
                               furnished, open_fire, terrace, terrace_area, terrace_orientation,
                               garden, garden_area, garden_orientation, number_of_facades, 
                               construction_year, swimming_pool, state_of_building, epc, kwh
                               )
                
                    return listing

            except json.JSONDecodeError:
                print("Failed to parse JSON data")
        else:
            print("Could not find window.classified data in the HTML")
    else:
        print(f"Failed to fetch the page. Status code: {response.status_code}")
        print(response.text)


# get data from json back in a safe way, when data is not there we make sure code doesn't break
def safe_get(d, *keys):
    for key in keys:
        if isinstance(d, dict):
            d = d.get(key)
        else:
            return None
    return d

mydb.close()