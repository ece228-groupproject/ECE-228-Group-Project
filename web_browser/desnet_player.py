from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from PIL import Image
from pathlib import Path
import yaml 
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.action_chains import ActionChains

import torch
import torchvision as tv
import torchvision.transforms.v2 as v2
from model import country_coord
from model.our_datasets import Country_images

from scipy.interpolate import interp1d
from math import log, tan, pi, radians


USE_GPU = True
if USE_GPU and torch.cuda.is_available():
    device = torch.device('cuda')
else:
    device = torch.device('cpu')
#get models
print(f"Using {device} device")

batch_size = 16
weights = tv.models.DenseNet201_Weights.DEFAULT
transform = v2.Compose([weights.transforms(), ])

dataset_path = "../data/compressed_dataset"
d = Country_images("web_browser/model/dataset/country.csv",dataset_path,transform=transform)
num_classes = d.get_num_classes()
model = tv.models.densenet201(num_classes=num_classes)
checkpoint = torch.load(os.path.join( model.path,model.name+"-Best.pth"),map_location=torch.device(device))
model.load_state_dict(checkpoint)


model = model.to(device)


RED     = "\033[91m"
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
BLUE    = "\033[94m"
MAGENTA = "\033[95m"
CYAN    = "\033[96m"
BOLD    = "\033[1m"
RESET   = "\033[0m"

def ai_player(model, img_path, round_nu):    
    img = d.transform(torchvision.io.read_image(img_path))
    pred = model(img)    
    pred = country_coord.ctry2coord(d.country_dict, pred) #lat, long
    
    output = {
        'meta': {
            'round': round_num,
            'status': 'processed'
        },
        'location': {
            'lat': pred[0],
            'lon': pred[1]
        }
    },
    output_path = Path(f"./processed/round_{round_num:02}_output.yaml")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Dump only current collected rounds
    with open(output_path, "w") as f:
        yaml.dump(output, f)
    
    print(f"Round {output['meta']['round']} written to {output_path}")
    
    return pred

def wait_for_output(output_path: Path, round_num: int, timeout: float = 60.0):
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
    return path

def has_confirm_active(driver):
    try:
        element = driver.find_element(By.ID, "confirmButton")
        return "confirmActive" in element.get_attribute("class")
    except:
        return False
def countdown(t_length): 
    for i in range(t_length, 0, -1):
        print(f"\r{YELLOW}Time till next round: {i}...{RESET}", end='', flush=True)
        time.sleep(1)
    print("\rTime till next round: 0   ")

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
driver.execute_script("document.body.style.zoom='64%'")

lat_up =73.958420
long_low = -181.102949

lat_low = -75.299304
long_up = 179.235395

round_num = 1
image_path = Path(f"./screenshots/round_{round_num:02}.png")

image_path.parent.mkdir(parents=True, exist_ok=True)


print(f"{GREEN}\n\n========================\nGAME BEGIN\n========================{RESET}")

# Run for multiple rounds
for round_num in range(1, 101):  # or while True

    print('\n\n' + '=' * 10 + f' ROUND {round_num} START ' + '=' * 10 + '\n\n')


    ###################### IMAGE CAPTURE ######################
    # Wait for new map load
    map_el = wait.until(EC.presence_of_element_located((By.ID, "map")))
    time.sleep(2)  # let dynamic elements load

    # HIDE everything
    toggle_elements(driver, selectors=selectors_main, ids=ids_main, hide=True)
    toggle_elements(driver, selectors=selectors_iframe, inside_iframe=True, iframe_selector=iframe_selector, hide=True)

    # Capture screenshot
    image_path = capture_map_screenshot(driver, round_num)

    # UNHIDE everything
    toggle_elements(driver, selectors=selectors_main, ids=ids_main, hide=False)
    toggle_elements(driver, selectors=selectors_iframe, inside_iframe=True, iframe_selector=iframe_selector, hide=False)
    print(f"{YELLOW}Image capture done...{RESET}")

    ###################### GAMEPLAY ######################
    output_path = Path(f"./processed/round_{round_num:02}_output.yaml")
    result = ai_player(model=model, img_path=image_path, round_num=round_num)
    #result = wait_for_output(output_path, round_num)
    print("Got result:", result)

    lat = result['location']['lat']
    lon = result['location']['lon']
    round_num+=1
    long_conv = interp1d([long_low,long_up],[-327,327])
    lat_conv = interp1d([lat_up,lat_low],[-200,200])
    x = long_conv(lon)
    y = lat_to_mercator_y(lat, lat_up, lat_low, 400)
    # Wait for guess to occur
    print("Waiting for 'confirmActive' class to appear...")
    ActionChains(driver).move_to_element_with_offset(map_el, 0,0).click().perform()
    time.sleep(1)
    ActionChains(driver).move_to_element_with_offset(map_el, 0,0).click().perform()
    time.sleep(1)
    ActionChains(driver).move_to_element_with_offset(map_el, x,y).click().perform()
    time.sleep(5)


    ###################### NEXT ROUND ######################

    # Wait until the class 'confirmActive' is present on the confirmButton
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