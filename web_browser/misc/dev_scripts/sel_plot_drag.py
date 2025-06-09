from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

import re
import math
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import requests
from PIL import Image
from io import BytesIO

os.makedirs("./screenshots", exist_ok=True)

os.makedirs("./tiles", exist_ok=True)

def tile_to_latlon(x, y, z):
    n = 2.0 ** z
    lon = x / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * y / n)))
    lat = math.degrees(lat_rad)
    return lat, lon
service = Service(executable_path="./chromedriver") 

driver = webdriver.Chrome(service=service)
driver.get("https://openguessr.com/")  
wait = WebDriverWait(driver, 10)
map_el = wait.until(EC.presence_of_element_located((By.ID, "map")))

while True:
    # ActionChains(driver).move_to_element_with_offset(map_el, 0,0).click().perform()
    driver.execute_script("document.getElementById('map').style.maxHeight = '100%';")
    time.sleep(5)

    size = map_el.size
    width = size['width']
    height = size['height']
    print(f"Width: {width}")
    # Compute drag distances (left = negative X)
    drag_x = width // 3
    drag_y = height // 3 # no vertical drag

    # Start from center of map element
    start_x = width // 2
    start_y = height // 2

    # Create an ActionChains instance
    actions = ActionChains(driver)
    driver.execute_script("document.getElementById('map').style.maxHeight = '100%';")
    time.sleep(1)

    # Perform the click-and-drag
    for _ in range(1):
        actions.move_to_element_with_offset(map_el, 0, 0)
        actions.click_and_hold()
        actions.move_by_offset(330, 330)
        print(drag_x)
        actions.release()
        actions.perform()
        print(f"\rDrag {_}", end='', flush=True)
    time.sleep(2)
    tiles = driver.find_elements(By.CSS_SELECTOR, "img.leaflet-tile")
    tile_info = []
    driver.execute_script("document.getElementById('map').style.maxHeight = '100%';")

    for tile in tiles:
        src = tile.get_attribute("src")
        style = tile.get_attribute("style")
        
        match = re.search(r"[?&]x=(\d+)&y=(\d+)", src)
        if match:
            x = int(match.group(1))
            y = int(match.group(2))
            tile_info.append((src, x, y))

    # for src, x, y in tile_info:
    #     print(f"{src} at ({x}, {y})")+
    tile_dict = {}
    # Map tile_info into dict for coordinate alignment 
    for tile in tile_info: 
        print(tile)
        tile_dict[(tile[1], tile[2])] = tile[0]
    TILE_SIZE = 256
    print(tile_dict)


    canvas_width =  TILE_SIZE *3
    canvas_height = TILE_SIZE *4


    canvas = Image.new("RGB", (canvas_width, canvas_height))


