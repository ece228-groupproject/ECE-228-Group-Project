from scipy.interpolate import interp1d
from math import log, tan, pi, radians

def lat_to_mercator_y(lat, lat_min, lat_max, height):
    lat_rad = radians(lat)
    y_merc = log(tan(pi / 4 + lat_rad / 2))
    
    # Normalize to pixel Y range
    lat_min_rad = radians(lat_min)
    lat_max_rad = radians(lat_max)
    y_min = log(tan(pi / 4 + lat_min_rad / 2))
    y_max = log(tan(pi / 4 + lat_max_rad / 2))
    
    y = (y_merc - (y_min + y_max) / 2) / (y_max - y_min) * height
    return y

long = 2.341837
lat = 48.817151


lat_up =73.958420
long_low = -181.102949

lat_low = -75.299304
long_up = 179.235395
# x = map_range(long, 71, -71, -327, 327)
# y = map_range(lat, -176, 176, -200, 200)

long_conv = interp1d([long_low,long_up],[-327,327]) # x

x = long_conv(long)
y = lat_to_mercator_y(lat, lat_up, lat_low, 400)
# print(q)
print(f"x: {x}")  # Outputs -100?!?!?!??!?! it should be 
print(f"y: {y}")  # Outputs -100?!?!?!??!?! it should be 