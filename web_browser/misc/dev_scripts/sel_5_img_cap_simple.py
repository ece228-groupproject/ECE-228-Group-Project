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


#  Setup Chrome Driver 
service = Service(executable_path="./chromedriver") 
driver = webdriver.Chrome(service=service)
driver.get("https://openguessr.com/")  

wait = WebDriverWait(driver, 10)
map_el = wait.until(EC.presence_of_element_located((By.ID, "map")))
alert_script = "console.log('Alert via selenium')"
lat = 37.7749      # example latitude (San Francisco)
lon = -122.4194    # example longitude

while True:
    driver.execute_script(alert_script) 
    ActionChains(driver).move_to_element_with_offset(map_el, 0,0).click().perform()

    map_size = map_el.size
    map_width = map_size['width']
    map_height = map_size['height']
    # Move to map, offset, click
    print("======== Map Diagnostics ========")
    print(f"Map H: {map_height}")
    print(f"Map W: {map_width}")
    # map_el.click()
    # element.click()

    pixel_coords = driver.execute_script("""
    const someLatVal = L.latLng(arguments[0], arguments[1]);
    console.log(someLatVal)                            
    """, lat, lon)

    time.sleep(2)

