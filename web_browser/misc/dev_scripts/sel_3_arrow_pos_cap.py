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


# Setup Chrome Driver 
service = Service(executable_path="./chromedriver") 
driver = webdriver.Chrome(service=service)
driver.get("https://openguessr.com/")  

wait = WebDriverWait(driver, 10)
map_el = wait.until(EC.presence_of_element_located((By.ID, "map")))

alert_script = "console.log('Alert via selenium')"
fail = "console.log('Failed')"
time.sleep(5)
iframe = driver.find_element(By.ID, "PanoramaIframe")
iframe.screenshot("./screenshots/streetview_iframe.png")
while True:
    try:
        # print("Start")
        # iframes = driver.find_elements(By.TAG_NAME, 'iframe')
        # print(f"Found {len(iframes)} iframe(s)")
        # for i, f in enumerate(iframes):
        #     print(f"[{i}] ID: {f.get_attribute('id')}, src: {f.get_attribute('src')}")

        # REFIND the iframe (each round could reload it)
        iframe = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "PanoramaIframe"))
        )
        driver.execute_script(alert_script) 
        # Switch to iframe context
        driver.switch_to.frame(iframe)

        map_el = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.gmnoprint.SLHIdE-sv-links-control")))
        control_svg_paths = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'path[aria-label]'))
        )

        # Extract info from each direction path
        for path in control_svg_paths:
            label = path.get_attribute("aria-label")
            transform = path.get_attribute("transform")
            print(f"{label} at {transform}")     # Reset back to the main page DOM
        driver.switch_to.default_content()

    except Exception as e:
        print("Error:", e)
        driver.execute_script(fail) 

        driver.switch_to.default_content()
        time.sleep(0.5)
