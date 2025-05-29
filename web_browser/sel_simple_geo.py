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
from PIL import Image
from pathlib import Path
import yaml 
import time
import undetected_chromedriver as uc

from scipy.interpolate import interp1d
from math import log, tan, pi, radians


RED     = "\033[91m"
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
BLUE    = "\033[94m"
MAGENTA = "\033[95m"
CYAN    = "\033[96m"
BOLD    = "\033[1m"
RESET   = "\033[0m"


def has_confirm_active(driver):
    try:
        element = driver.find_element(By.ID, "confirmButton")
        return "confirmActive" in element.get_attribute("class")
    except:
        return False

def wait_for_output(output_path: Path, round_num: int, timeout: float = 80.0):
    start_time = time.time()
    while time.time() - start_time < timeout:
        if output_path.exists():
            try:
                with open(output_path, 'r') as f:
                    data = yaml.safe_load(f)
                if isinstance(data, list):
                    for entry in data:
                        if entry.get('meta', {}).get('round') == round_num:
                            return entry
                else:
                    print("Unexpected data format:", type(data))
            except Exception as e:
                print(f"Error reading file: {e}")
        time.sleep(1)
    raise TimeoutError(f"Timed out waiting for output {output_path}")

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

def countdown(t_length): 
    for i in range(t_length, 0, -1):
        print(f"\r{YELLOW}Time till next round: {i}...{RESET}", end='', flush=True)
        time.sleep(1)
    print("\rTime till next round: 0   ")


lat_up =73.958420
long_low = -181.102949

lat_low = -75.299304
long_up = 179.235395



service = Service(executable_path="./chromedriver") 
driver = webdriver.Chrome(service=service)
driver.get("https://openguessr.com/?join=gwa5kzz")  
wait = WebDriverWait(driver, 15)

gui_selector_ids = ['confirmButton', 'mapHolder', 'standardButton', 'chatContainer', 'BottomBar', 
                    'bottomFooterAds', 'topButtonAre', 'mapDiv', 'svelte-announcer' ]
gui_query_class = ['adsTextResult', "button.accountButton", "button.standardButton.white"]
time.sleep(1)
driver.execute_script("document.body.style.zoom='64%'")
png = driver.get_screenshot_as_png()


round_num = 1
image_path = Path(f"./screenshots/round_{round_num:02}.png")

image_path.parent.mkdir(parents=True, exist_ok=True)

input(f"\n\n\nLog into the AI Account to begin gameplay: Hit enter once done\n\n\n")

while True:
    print(f'=' * 10 + ' ROUND {round_num} START ' + '=' * 10)

    map_el = wait.until(EC.presence_of_element_located((By.ID, "map")))
    size = map_el.size
    size = map_el.size

    output_path = Path(f"./processed/round_{round_num:02}_output.yaml")

    result = wait_for_output(output_path, round_num)
    print("Got result:", result)

    lat = result['location']['lat']
    lon = result['location']['lon']

    round_num+=1
    long_conv = interp1d([long_low,long_up],[-327,327])
    # lat_conv = interp1d([lat_up,lat_low],[-200,200])
    x = long_conv(lon)
    y = lat_to_mercator_y(lat, lat_up, lat_low, 400)


    ActionChains(driver).move_to_element_with_offset(map_el, 0,0).click().perform()
    time.sleep(1)
    ActionChains(driver).move_to_element_with_offset(map_el, 0,0).click().perform()
    time.sleep(1)
    ActionChains(driver).move_to_element_with_offset(map_el, x,y).click().perform()
    time.sleep(5)
    WebDriverWait(driver, 300).until(has_confirm_active)
    print("Confirm button was activated. AI will now click.")
    time.sleep(1)  # Wait 1 second before clicking Continue
    confirm_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "confirmButton"))
    )
    ActionChains(driver).move_to_element(confirm_btn).click().perform()

    continue_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "nextRound"))
    )
    countdown(10)

    continue_btn.click()
    print("Clicked Continue button.")

    print("Done with round", round_num)
    time.sleep(2)  # Wait until next round loads
    # ActionChains(driver).move_to_element_with_offset(map_el, 200,0).click().perform()
    # time.sleep(2)
    # ActionChains(driver).move_to_element_with_offset(map_el, 300,0).click().perform()
    # time.sleep(2)
    # ActionChains(driver).move_to_element_with_offset(map_el, 327,-200).click().perform()
    # time.sleep(1)
