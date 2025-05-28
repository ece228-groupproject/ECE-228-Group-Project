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

#  Wait for map to load - 20 Second timeout
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.ID, "map"))
)
map_el = driver.find_element(By.ID, "map")

#  Define the latitude and longitude
lat = 37.7749     # San Francisco
lon = -122.4194

# TODO: Method to convert into transform3d(x,y,z) coordinates 
# Run JS to move the marker

time.sleep(5)


js = """
const markerPane = document.getElementsByClassName("leaflet-pane leaflet-marker-pane")[0];
const markerIcon = markerPane.querySelector("img");
if (markerIcon) {
    markerIcon.style.transform = "translate3d(100px, 50px, 0px)";
    alert("Injection success!");

}
"""
driver.execute_script(js)

print("JS Executed")

time.sleep(10)

driver.quit()
'''

Grabs zoom level 
// Select the element
const proxyEl = document.querySelector('.leaflet-proxy');

// Get the computed transform style (more robust than .style)
const transformStr = window.getComputedStyle(proxyEl).transform;

// Extract the scale factor
let scale = 1;
if (transformStr.includes('matrix')) {
  // matrix(a, b, c, d, tx, ty) → a and d are scaleX and scaleY
  const match = transformStr.match(/matrix\(([^,]+),[^,]+,[^,]+,([^,]+),/);
  if (match) {
    scale = parseFloat(match[1]); // or match[2] for Y scale
  }
} else if (transformStr.includes('scale')) {
  const match = transformStr.match(/scale\(([\d.]+)\)/);
  if (match) {
    scale = parseFloat(match[1]);
  }
}

console.log("Current scale factor:", scale);


place icon, but not change coordinates at which controls whats sent to whatever, also doesnt place it first if element doesnt exist (user clicks first)

const markerPane = document.getElementsByClassName("leaflet-pane leaflet-marker-pane")[0];
const markerIcon = markerPane.querySelector("img");
markerIcon.style.transform = "translate3d(200px, 50px, 0px)";


'''