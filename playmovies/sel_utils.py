import random
import time

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import proxy


def initWebdriver():
    ip_port = proxy.generateProxy()
    print("Using US IP: {}".format(ip_port))

    chrome_option = webdriver.ChromeOptions()
    chrome_option.add_argument("--proxy-server={}".format(ip_port))

    driver = webdriver.Chrome(chrome_options=chrome_option)
    driver.maximize_window()
    time.sleep(random.randint(2,3))
    return driver
    

def scrollToBottom(driver):
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight;")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(random.randint(3,4))
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight;")
        if new_height == last_height:
            break
        last_height = new_height



def isPresent(driver, by, value):
    # Check if the element is present
    # return True or False
    try:
        WebDriverWait(driver,15).until(EC.visibility_of_element_located((by, value)))
        if len(driver.find_elements(by, value)) > 0:
            print("Element is present..")
            return True
        else:
            print("Element not found..")
            return False

    except Exception as e:
        return False
