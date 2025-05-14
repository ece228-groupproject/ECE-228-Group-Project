import math
def latlon_to_pixel(lat, lon, zoom):
    scale = 256 * 2**zoom
    x = (lon + 180) / 360 * scale
    y = (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * scale
    return (x, y)


# Washington DC 
lat = 38.9072 
lon = 77.0369

x,y = latlon_to_pixel(lat, lon, 0)

print(f"X: {x}, Y: {y}" )