from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import math
RED     = "\033[91m"
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
BLUE    = "\033[94m"
MAGENTA = "\033[95m"
CYAN    = "\033[96m"
BOLD    = "\033[1m"
RESET   = "\033[0m"
# Create screenshot directory
os.makedirs("./screenshots", exist_ok=True)

def toggle_elements(driver, selectors=None, ids=None, inside_iframe=False, iframe_selector=None, hide=True):
    if inside_iframe and iframe_selector:
        try:
            iframe = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, iframe_selector))
            )
            driver.switch_to.frame(iframe)
        except Exception as e:
            print(f"{RED}Failed to switch to iframe {e}:{RESET}")

    # Toggle by selector
    if selectors:
        for selector in selectors:
            js = f"""
                document.querySelectorAll('{selector}')
                    .forEach(el => el.style.display = {'"none"' if hide else '""'});
            """
            driver.execute_script(js)

    # Toggle by ID
    if ids:
        for el_id in ids:
            js = f"""
                var el = document.getElementById('{el_id}');
                if (el) el.style.display = {'"none"' if hide else '""'};
            """
            driver.execute_script(js)

    if inside_iframe:
        driver.switch_to.default_content()

def capture_map_screenshot(driver, round_num=1):
    path = f"./screenshots/round_{round_num:03d}.png"
    driver.save_screenshot(path)
    print(f"Screenshot saved to: {path}")

service = Service(executable_path="./chromedriver")
driver = webdriver.Chrome(service=service)
driver.get("https://openguessr.com/")
wait = WebDriverWait(driver, 15)

# Selectors and IDs to toggle
selectors_main = [
    '.adsTextResult', '.noAdvertsText', '.svelte-p9o8f0',
    'button.standardButton.white', '[role="button"]',
    '.gmnoprint.gm-bundled-control.gm-bundled-control-on-bottom',
    '.fc-ccpa-root', '.fc-button-background', '.bottomFooterAds'
]
ids_main = [
    'confirmButton', 'mapHolder', 'standardButton', 'chatContainer', 'BottomBar',
    'bottomFooterAds', 'topButtonAre', 'mapDiv', 'svelte-announcer'
]
selectors_iframe = [
    '.gm-compass', '.gmnoprint',
    '.gmnoprint.gm-bundled-control.gm-bundled-control-on-bottom'
]
iframe_selector = "#PanoramaIframe"


print(f"{GREEN}\n\n========================\nGAME BEGIN\n========================{RESET}")

# Run for multiple rounds
for round_num in range(1, 6):  # or while True

    print(f"\nStarting Round {round_num}")

    # Wait for new map load
    wait.until(EC.presence_of_element_located((By.ID, "map")))
    time.sleep(2)  # let dynamic elements load

    # HIDE everything
    toggle_elements(driver, selectors=selectors_main, ids=ids_main, hide=True)
    toggle_elements(driver, selectors=selectors_iframe, inside_iframe=True, iframe_selector=iframe_selector, hide=True)

    # Capture screenshot
    capture_map_screenshot(driver, round_num)

    # UNHIDE everything
    toggle_elements(driver, selectors=selectors_main, ids=ids_main, hide=False)
    toggle_elements(driver, selectors=selectors_iframe, inside_iframe=True, iframe_selector=iframe_selector, hide=False)

    print("Done with round", round_num)
    time.sleep(15)  # Wait until next round loads (adjust as needed)