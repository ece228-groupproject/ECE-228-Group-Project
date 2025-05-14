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

print("Finished!")
map_size = map_el.size
map_width = map_size['width']
map_height = map_size['height']
print(map_width)
time.sleep(5)