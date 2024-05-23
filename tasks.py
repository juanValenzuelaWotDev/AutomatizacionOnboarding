# Import libraries
# from RPA.Browser.Selenium import Selenium
# from selenium.webdriver.common.by import By
import pandas as pd
import time
import logging
import robot_log
import bot_paths
import services
from fill_word_document import fill_document, download_document, database
import workmail.workmail_v2 as workmail

# Path finding
import os, sys

# Start the logger function
robot_log.start_logger()

# Global variables

# Functions
def send_onboarding_document():
    '''
    This function sends the onboarding information to the new employee
    Sends from our corporate email to the email in the cv
    This function takes the information from the database, fills the document
    and sends it via email
    '''
    # Step 1 is to download the information
    data_to_fill = download_document.download_data()

    # Step 2 is to generate the new document
    
    # # Load Json file
    # json_path = r"{}\info_empleado_Testing 1.json".format(bot_paths.database_path)
    # with open(json_path, encoding="utf-8") as user_file:
    #   parsed_json = json.load(user_file)

    document_name = "Oportunidad Facturar Servicios Profesionales [Template].docx"
    pdf_name = fill_document.fill_document(document_name,fill_document.data_to_replace_empleado,data_to_fill,"wot")

    # Step 3 is to send the document via email

    # El archivo no puede tener tildes
    attachment_path = os.path.join(os.getcwd(), "modified_documents", pdf_name)
    
    # Send the pdf you just generated through email
    workmail.send_email_with_attachment(
        subject="Hello with Attachment",
        body="This is a test email with attachment from AWS SES.",
        recipients=["juan.valenzuela@wotdev.com", "carla.hernandez.wot@gmail.com"],
        sender="javieras@wotdev.com",
        file_path=attachment_path,
        access_key=services.access_key,
        secret_key=services.secret_key
    )


# Main function
if __name__ == "__main__":
    # Check if the folder paths exist
    bot_paths.check_paths()
    # Import creds
    services.load_creds()
    # Send automatic email
    send_onboarding_document()

    print("Hello world")
    logging.info("Starting consumer")
    logging.info("Finished run")