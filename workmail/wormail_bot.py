# Import libraries
from RPA.Browser.Selenium import Selenium
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Logging
import logging
from robot_log import start_logger

# Global variables
user = ""
password = ""

body = "Body of the email"
subject = "Please send invoice"

sender_email = ""
app_password = ""
receiver_email = ""

url = "https://wotdev.awsapps.com/mail"

# Function prototypes

def serialize_string(text:str):
    '''
    This function takes a small text and separates the letters and puts them inside an array
    This is so that the bot can type letter by letter each word
    '''
    logging.info("Construyendo mensaje")
    buffer = []
    for letter in text:
        buffer.append(letter.upper())
    logging.info("Mensaje serializado")
    return buffer

def log_in(browser):
    # Write email //*[@id="wdc_username"]
    browser.input_text('//*[@id="wdc_username"]', sender_email.replace("@wotdev.com", ""))
    time.sleep(2)
    # Write password //*[@id="wdc_password"]
    browser.input_text('//*[@id="wdc_password"]', app_password)
    time.sleep(2)

    # Click sign in
    browser.click_button('//*[@id="wdc_login_button"]')
    time.sleep(20)

    # Check for invalid passwords
    check_invalid_password = browser.is_element_visible('//*[ contains (text(), "Authentication Failed" ) ]')
    mail_screen = browser.is_element_visible('//*[ contains (text(), "New item" ) ]')
    print(f"New item {mail_screen} Invalid password: {check_invalid_password}")
    return check_invalid_password or not (mail_screen)

def send_email(browser:Selenium, receiver_email, subject, body, CCO=""):
    # Start of the process
    logging.info("Construyendo correo")
    browser.click_element_if_visible('//*[ contains (text(), "New item" ) ]')
    time.sleep(2)
    browser.click_element_if_visible('//*[ contains (text(), "New email" ) ]')
    time.sleep(2)
    
    # Writing subject //*[@id="ext-comp-1239"]
    logging.info("Escribiendo asunto del correo")
    # browser.execute_javascript(f'document.querySelector("#ext-comp-1239").value = "{subject}"')
    browser.click_element_when_clickable('//*[@id="ext-comp-1140"]')
    letters = serialize_string(subject)
    for i in letters:
        browser.press_keys(None, i)
    time.sleep(2)

    # Writing body
    logging.info("Escribiendo cuerpo del correo")
    # iframe //*[@id="cke_1_contents"]/iframe
    browser.select_frame('//*[@id="cke_1_contents"]/iframe')
    # Modify the inner html of this element document.querySelector("body > p").innerHTML = "This is a sample email. \n formated"
    browser.execute_javascript(f'document.querySelector("body > p").innerHTML = "{body}"')
    time.sleep(2)

    # Writing sender email //*[@id="ext-gen402"]
    browser.unselect_frame()
    logging.info("Escribiendo correo destinatario")
    browser.click_element_when_visible('//*[@id="ext-gen402"]')
    # browser.input_text('//*[@id="ext-gen402"]', receiver_email)
    letters = serialize_string(sender_email)
    for i in letters:
        browser.press_keys(None, i.lower())
    time.sleep(2)
    
    # (optional) add C.C.O. (hidden copy to another email)
    if not(CCO==""):
        logging.info("Agregando con copia oculta")
    
    # Click send //*[@id="ext-gen327"]
    logging.info("Enviando correo")
    # browser.click_element_if_visible('//*[@id="ext-gen327"]')

def main():
    print("Executing mail automation")
    browser = Selenium()
    browser.open_available_browser(url=url, headless=False)
    # Wait some time for the page to load
    time.sleep(5)
    
    # Log in to the site
    check_invalid_password = log_in(browser)
    
    # Make a new email
    send_email(browser, receiver_email, subject, body)

    # Close all the browsers
    print("Closing browser")
    browser.close_all_browsers()

    # Handle the invalid password
    if (check_invalid_password == True):
        # In here show a message in tkinter
        print("Could not sign in with the username or password, check them before retrying")
        return False

# Email automation (Easy) https://www.youtube.com/watch?v=u0UoHR6j0ig
# Bot opens amazon work mail
# Bot starts a new email
# Bot gets the receiver email from a file
# Bot Writes the receiver email
# Bot writes the body of the mail
# Bot writes the subject
# Bot clicks send 
# Bot waits until the email is sent
# (optional) If there are multiple emails the bot starts a new email
# (optional) Bot repeats until there are no emails left
# Bot closes browser

# Show a progress bar
# Maybe add a pop up window in tkinter to show it finished

# Desktop app
# Make a portable exe file
# Load an excel file with the emails
# Have a send button
# (optional) Have something like a list of email bodies to add variety (different process)
# When the process finshes, reset the app to default state
# Use tkinter to make a pretty and basic UI

# Main code
# if __name__ == "__main__":
#     start_logger()
#     main()

def execute_email():
    try:
        start_logger()
        main()
        return True
    except:
        return False
    # Returns false if it could not get inside