from seleniumwire import webdriver
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

from seleniumwire.utils import decode
import json

service = Service(executable_path="./chromedriver")
options = {
    'exclude_hosts': ['cloudflare.com']  # Bypass Selenium Wire for these hosts
}
driver = webdriver.Chrome(
    service=service,
    seleniumwire_options=options
    )
driver.get("https://google.com/")
wait = WebDriverWait(driver, 15)


def format_response(response):
    formatted_response = {
        "status_code": response.status_code,
        "reason": response.reason,
        "headers": dict(response.headers),
        "date": response.date.strftime("%Y-%m-%d %H:%M:%S"),
        "body": response.body[:50].decode('utf-8')  # decode the body as it's encoded
    }
    return formatted_response

#request = driver.wait_for_request('play.google.com/')
for request in driver.requests:
    # if request.response:
    #     print(
    #         request.url,
    #         decode(request.response.body,request.response.headers.get('Content-Encoding', 'identity')),
    #         request.response.headers['Content-Type']
    #     )
    if "google.com/" in request.url:
        try:
            formatted_response = format_response(request.response)
            print(json.dumps(formatted_response, indent=2))
        except:
            a ;;;;nn
driver.quit()
        