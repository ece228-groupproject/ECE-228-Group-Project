from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
# platform specific issues... solve by first including script to determine host OS & include dynamic path selection to proper chromedriver 
service = Service(executable_path="./chromedriver")
driver = webdriver.Chrome(service=service)

driver.get("https://orteil.dashnet.org/cookieclicker/")

# https://orteil.dashnet.org/cookieclicker/

cookie_id = "bigCookie"
cookies_id = "cookies"
product_price_prefix = "productPrice"
product_prefix = "product"

WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'English')]"))
)

language = driver.find_element(By.XPATH, "//*[contains(text(), 'English')]")
language.click()

WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.ID, cookie_id))
)

cookie = driver.find_element(By.ID, cookie_id)

while True:
    try:
        cookie = driver.find_element(By.ID, cookie_id)
        cookie.click()

        cookies_count = driver.find_element(By.ID, cookies_id).text.split(" ")[0]
        cookies_count = int(cookies_count.replace(",", ""))

        for i in range(4):
            product_price_element = driver.find_element(By.ID, product_price_prefix + str(i))
            product_price = product_price_element.text.replace(",", "")

            if not product_price.isdigit():
                continue

            product_price = int(product_price)

            if cookies_count >= product_price:
                product = driver.find_element(By.ID, product_prefix + str(i))
                product.click()
                break
    except Exception as e:
        print(f"Exception occurred: {e}")
        continue
