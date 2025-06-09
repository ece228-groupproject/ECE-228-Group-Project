import requests
import json
from geopy.geocoders import Nominatim
import csv
import os
import country_converter as coco
import pycountry
from geopy import distance
# country --> iso --> capital --> coord
# ctry2coord(country_dict, model_output, centroid)

all_capital_cities_in_the_world=os.path.join("data","kaggle_dataset","all_capital_cities_in_the_world.csv")
concap=os.path.join("data","kaggle_dataset","concap.csv")

# -----------------------#
# Get country from lat and lon coordinates
def getDist(coord1,coord2):
    return distance.distance(coord1, coord2).km


# -----------------------#
# Get country from lat and lon coordinates
def getCountry_fromCoord(coord):
    geolocator = Nominatim(user_agent="http")
    location = geolocator.reverse(str(coord[0])+","+str(coord[1]))
    return location.raw["address"].get("country","")
    
# -----------------------#
# Get country iso2 code
def getISO2(ctry):
    iso2 = coco.convert(names=ctry, to='ISO2')
    if iso2 == "not_found":
        raise Exception("ISO2 not found for country: "+ctry)
    return iso2
    # url = "https://countriesnow.space/api/v0.1/countries/iso"
    # payload = {"country": ctry}
    # headers = {}

    # response = requests.request("POST", url, headers=headers, data=payload)
    # if(response.status_code==429):
    #     raise Exception("In ISO2: <Response [429]>: Too many requests")
    # else:
    #     res = dict(json.loads(response.text))
    #     #print(type(res))
    #     iso2 = res["data"]["Iso2"]
    #     return iso2
        
# -----------------------#
# lookup using country -> capital (api1 cities)
ctry2capital_dict = {}
def ctry2capital(ctry):
    # iso code
    iso2 = getISO2(ctry)
    capital = ctry2capital_dict.get(iso2, None)
    if capital:
        return capital
    # get capital
    url = "https://countriesnow.space/api/v0.1/countries/capital"
    payload = {"iso2": iso2}
    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload)
    if(response.status_code==429):
        raise Exception("In ctry2capital: <Response [429]>: Too many requests")
    else:
        res = dict(json.loads(response.text))
        capital = res["data"]["capital"]
        ctry2capital_dict[iso2] = capital
        return capital
    
# -------------------- #
# capital lat lon dictionary with all-capital-cities-in-the-world dataset
capital_dict = {}
with open(all_capital_cities_in_the_world,mode="r",newline="") as file:
    reader=csv.DictReader(file)
    for row in reader:
        #print(row['Country'])
        if (row["Latitude"])[-1] == "S":
            lat  = "-" + row["Latitude"][0:-1]
        elif (row["Latitude"])[-1] == "N":
            lat  = row["Latitude"][0:-1]
        
        if (row["Longitude"])[-1] == "E":
            long  = row["Longitude"][0:-1]
        elif (row["Longitude"])[-1] == "W":
            long  = "-" + row["Longitude"][0:-1]  
        
        capital_dict[row["Capital City"]] = lat,long

#print(capital_dict)

# -------------------- #
# capital lat lon dictionary with world-capitals-gps
capital_dict_1 = {}
with open(concap,mode="r",newline="") as file:
    reader=csv.DictReader(file)
    for row in reader:
        capital_dict_1[row["CapitalName"]] = (row["CapitalLatitude"],row["CapitalLongitude"])

#print(capital_dict_1)

# -----------------------#
# lookup using capital -> coord (dataset)
def capital2coord(capital, ctry, centroid):
    print("Getting coordinates...")
    if centroid:
        for key, coord in country_centroid.items():
            if ctry.lower() == key.lower():
                return coord
    try:
        print("Trying capital_dict_1: world-capitals-gps")
        for key, coord in capital_dict_1.items():
            if capital.lower() == key.lower():
                return coord
    except:
        try:
            print("Trying capital_dict: all-capital-cities-in-the-world")
            for key, coord in capital_dict.items():
                if capital.lower() == key.lower():
                    return coord
        except:
            print("Could not find capital, returning none")
            return None
            
# do try/except to see if capital exists in some datasets and not in others

# -----------------------#
# main function, output coord
def ctry2coord(ctry_dict, m_output, centroid):
    for key, ctry in ctry_dict.items():
        if m_output == key:
            # country -> capital (api1 cities) 
            capital = ctry2capital(ctry)
            # capital -> coord (api2 geocoding)
            coord = capital2coord(capital, ctry, centroid)
            print(f"Capital of {ctry}: {capital}: {coord}")
            # round coord to integers
            coord = (round(float(coord[0])), round(float(coord[1])))
            print(type(coord))
            return coord
            
# main function shoudl ahve boolean parameter to choose capital or centroid coordinates