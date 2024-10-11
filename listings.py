import os
import csv

class Listing():

    # Class variable to keep track of instance made
    instance_count = 0

    def __init__(self, property_id, summary, locality, postal, address, region, 
                 country, price, property_type, sub_property_type, sale_type, 
                 number_of_bedrooms, living_area, kitchen, attic, basement,
                 furnished, open_fire, terrace, terrace_area, terrace_orientation,
                 garden, garden_area, garden_orientation, number_of_facades, 
                 construction_year, swimming_pool, state_of_building, epc, kwh):
        self.property_id = property_id
        self.summary = summary                              # webpage ID, 8 numbers, end of URL
        self.locality = locality                            # province
        self.postal = postal
        self.address = address
        self.region = region
        self.country = country
        self.price = price
        self.sale_type = sale_type                          # (note: exclude life sales)
        self.property_type = property_type                  # (house or apartment)
        self.sub_property_type = sub_property_type          # (bungalow, chalet, mansion, ...)
        self.number_of_bedrooms = number_of_bedrooms
        self.living_area = living_area                      # (area in m²)
        self.kitchen = kitchen
        self.attic = attic                                  # (0/1)
        self.basement = basement                            # (0/1)
        self.furnished = furnished                          # (0/1)
        self.open_fire = open_fire                          # (0/1)
        self.terrace = terrace                              
        self.terrace_area = terrace_area                    # (area in m² or null if no terrace)
        self.terrace_orientation = terrace_orientation
        self.garden = garden                                
        self.garden_area = garden_area                      # (area in m² or null if no garden)
        self.garden_orientation = garden_orientation        
        self.number_of_facades = number_of_facades          
        self.construction_year = construction_year          
        self.swimming_pool = swimming_pool                  # (0/1)
        self.state_of_building = state_of_building          # (new, to be renovated, ...)
        self.epc = epc
        self.kwh = kwh

        # Increment the class variable by 1 for each new instance
        Listing.instance_count += 1
        

    # write all info to a nice Dictionairy Object
    def to_dict(self):
        return {
            "property_id": self.property_id,
            "summary": self.summary,
            "locality": self.locality,
            "postal": self.postal,
            "address": self.address,
            "region": self.region,
            "country": self.country,
            "price": self.price,
            "sale_type": self.sale_type,
            "property_type": self.property_type,
            "sub_property_type": self.sub_property_type,
            "number_of_bedrooms": self.number_of_bedrooms,
            "living_area": self.living_area,
            "kitchen": self.kitchen,
            "attic": self.attic,
            "basement": self.basement,
            "furnished": self.furnished,
            "open_fire": self.open_fire,
            "terrace": self.terrace,
            "terrace_area": self.terrace_area,
            "terrace_orientation": self.terrace_orientation,
            "garden": self.garden,
            "garden_area": self.garden_area,
            "garden_orientation": self.garden_orientation,
            "number_of_facades": self.number_of_facades,
            "construction_year": self.construction_year,
            "swimming_pool": self.swimming_pool,
            "state_of_building": self.state_of_building,
            "epc": self.epc,
            "kwh": self.kwh
        }

    # Store our data in a CSV file
    def store_data(data, filename="listings_data.csv"):
        # is there date to Store? If not ingore
        if data is None:
           # print("Error: No data provided to store.")
            return
        
        # Check if file exists to determine if we need to write the header
        file_exists = os.path.isfile(filename)
        
        # Open the CSV file in append mode
        with open(filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=data.to_dict().keys())
            
            # Write the header only if the file does not exist
            if not file_exists:
                writer.writeheader()
            
            # Write the property data as a new row
            writer.writerow(data.to_dict())


    def __str__(self):
        return (
            f"Listing({self.property_id}):\n"
            f"Summary: {self.summary}\n"
            f"Locality: {self.locality}\n"
            f"Postal: {self.postal}\n"
            f"Address: {self.address}\n"
            f"Region: {self.region}\n"
            f"Country: {self.country}\n"
            f"Price: €{self.price}\n"
            f"Sale Type: {self.sale_type}\n"
            f"Property Type: {self.property_type} ({self.sub_property_type})\n"
            f"Bedrooms: {self.number_of_bedrooms}\n"
            f"Living Area: {self.living_area} m²\n"
            f"Kitchen: {self.kitchen}\n"
            f"Attic: {'Yes' if self.attic else 'No'}\n"
            f"Basement: {'Yes' if self.basement else 'No'}\n"
            f"Furnished: {'Yes' if self.furnished else 'No'}\n"
            f"Open Fire: {'Yes' if self.open_fire else 'No'}\n"
            f"Terrace: {'Yes' if self.terrace else 'No'} "
            f"({self.terrace_area} m², Orientation: {self.terrace_orientation})\n"
            f"  Garden: {'Yes' if self.garden else 'No'} "
            f"({self.garden_area} m², Orientation: {self.garden_orientation})\n"
            f"Number of Facades: {self.number_of_facades}\n"
            f"Construction Year: {self.construction_year}\n"
            f"Swimming Pool: {'Yes' if self.swimming_pool else 'No'}\n"
            f"State of Building: {self.state_of_building}\n"
            f"EPC: {self.epc}\n"
            f"KWh: {self.kwh}\n"
        )
    

    @classmethod
    def get_instance_count(cls):
        return cls.instance_count