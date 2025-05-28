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
os.makedirs("./screenshots", exist_ok=True)


def tile_to_latlon(x, y, z):
    n = 2.0 ** z
    lon = x / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * y / n)))
    lat = math.degrees(lat_rad)
    return lat, lon
service = Service(executable_path="./chromedriver") 

driver = webdriver.Chrome(service=service)
driver.get("https://openguessr.com/")  
time.sleep(5)

def has_confirm_active(driver):
    try:
        element = driver.find_element(By.ID, "confirmButton")
        return "confirmActive" in element.get_attribute("class")
    except:
        return False
def countdown(t_length): 
    for i in range(t_length, 0, -1):
        print(f"\r{i}", end='...', flush=True)
        time.sleep(1)
    print("\n")

    
while True:
    try:
        print("Waiting for 'confirmActive' class on #confirmButton...")

        # Wait until the class 'confirmActive' is present on the confirmButton
        WebDriverWait(driver, 300).until(has_confirm_active)

        print("Confirm button was activated. AI will now click Continue after delay.")
        time.sleep(1)  # Wait 1 second before clicking Continue
        confirm_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "confirmButton"))
        )
        ActionChains(driver).move_to_element(confirm_btn).click().perform()

        continue_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "nextRound"))
        )
        countdown(5)
        continue_btn.click()
        print("Clicked Continue button.")

        # time.sleep(5)  # Wait before starting the next cycle

    except TimeoutException:
        print("Timed out waiting for confirmActive class.")