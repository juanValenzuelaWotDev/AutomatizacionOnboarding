# Import libraries
from RPA.Browser.Selenium import Selenium
from selenium.webdriver.common.by import By
# to avoid bot detectors
import time
# to make folders and paths
import os
import sys
# Take the main path of AutomatizacionOnboarding and use it as normal
sys.path.insert(1, "/".join(os.path.realpath(__file__).split("/")[0:-2]))

import bot_paths

# Create a new instance of Selenium
browser = Selenium()

# Browser configuration
def browser_config():
    # Options to help clean up the renderer orphaned processes
    options = {
    "arguments": [
        "--disable-background-timer-throttling",
        "--disable-backgrounding-occluded-windows",
        "--disable-renderer-backgrounding"
    ]
    }
    return options

def download_document(company=None):
    if (company == "wot"):
        print("Descargando documento de WOT")
    elif (company == "bot"):
        print("Descargando documento de bot")
    elif (company == "quickplay"):
        print("Descargando documento de quickplay")
    
    # Browser object fully configured
    browser.open_chrome_browser(url="https://docs.google.com/document/d/1fTSS-ZkSQVT5XBx0lQxZfeoMmHUrl03w/edit", headless=False, preferences=browser_config())
    time.sleep(2)

    browser.click_element("//*[@id='docs-file-menu']")
    time.sleep(1)

    browser.click_element("//*[@id=':38']")
    time.sleep(1)

    browser.click_element("//*[contains(text(),'(.docx)')]")
    time.sleep(10)
    

try:
    download_document()
except:
    # Close all browsers
    browser.close_all_browsers()