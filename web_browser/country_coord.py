import requests
import json

import csv
# country --> iso --> capital --> coord
# ctry2coord(country_dict, model_output, centroid)


# -----------------------#
# Get country iso2 code
def getISO2(ctry):
    url = "https://countriesnow.space/api/v0.1/countries/iso"
    payload = {"country": ctry}
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload)
    if(response.status_code==429):
        raise Exception("In ISO2: <Response [429]>: Too many requests")
    else:
        res = dict(json.loads(response.text))
        #print(type(res))
        iso2 = res["data"]["Iso2"]
        return iso2
        
# -----------------------#
# lookup using country -> capital (api1 cities)
def ctry2capital(ctry):
    # iso code
    iso2 = getISO2(ctry)

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

        return capital
    
# -------------------- #
# capital lat lon dictionary with all-capital-cities-in-the-world dataset
capital_dict = {}
with open("model/dataset/all_capital_cities_in_the_world.csv",mode="r",newline="") as file:
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
with open("model/dataset/concap.csv",mode="r",newline="") as file:
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