import os
from dotenv import load_dotenv
from create_mail import create_workmail_user
from enable_mail import enable_workmail_user
from workmail_text_message import send_email
# Load environment variables from the specified path
creds_path = r"{}\creds\.env".format(os.getcwd())
print(f"Creds path:\n{creds_path}")
load_dotenv(dotenv_path=creds_path)


'''
requirements:

boto3
google
dotenv
oauth2client
gspread
google-api-python-client
requests


'''


# This file contains the functions to create a new email account and send the credentials via email to a particular user
# Global variables to access the service
access_key = os.getenv('ACCESS_KEY')
secret_key = os.getenv('SECRET_KEY')
region = os.getenv('AWS_REGION', 'us-east-1')  # Default to 'us-east-1' if not specified

# Connect to the database
def database_get_template(employee_name, recruiter_name, workmail_email, workmail_password, company='wot'):
    print("Conectando con base de datos")

    print("Buscando plantilla")

    print("Plantilla encontrada")

    print("Buscando datos del empleado")

    print("Datos encontrados")

    print("Rellenando plantilla")

    print("Texto generado!")
    # Return the template

def create_user_automation(username, company='wot'):
    creds_email = ""
    # Create the username logic

    # Decide where this
    if company == 'bot':
        print('Creating user for thebotdev.com')
        # Get the organization id
        organization_id = os.getenv('BOT_ORGANIZATION_ID')
        # Generate the user email
        user_email = f'{username}@thebotdev.com'  # Replace with the actual email
        display_name = user_email.split('@')[0] #return the things to the right of the @
        # Fetch the data from our database
        creds_email = f"Buenos días {username}, ¡Bienvenido a Bot Dev!"
    else:
        print('Creating user for wotdev.com')
        # Get the organization id
        organization_id = os.getenv('WOT_ORGANIZATION_ID')
        # Generate the user email
        user_email = f'{username}@wotdev.com'  # Replace with the actual email
        display_name = user_email.split('@')[0] #return the things to the right of the @
        # Fetch and make the email body
        creds_email = f"Buenos días {username}, ¡Bienvenido a WotDev!"
    
    # Create the user account
    payload = create_workmail_user(organization_id, user_email, display_name, access_key, secret_key, region)
    user_id = payload.get('UserId') # Get the user id from the payload
    email_password = payload.get('password') # The payload contains the password
    # Enable the user account
    if user_id:
        # If the user id exists then the request was successful
        response = enable_workmail_user(organization_id, user_id, user_email, access_key, secret_key, region)
        status = response.get('ResponseMetadata').get('HTTPStatusCode')
        if status == 200:
            print(f"Sucessful workmail creation! You can now send mails to this address: {user_email}")
            # Continue to send the email
            subject = f"{company.capitalize()}dev onboarding"
            body = creds_email #You have to put the password here because it is missing from the body!
            recipients = [user_email]  # List of email recipients
            sender = 'javieras@wotdev.com'  # This address is generally the same so it can be constant

            res = send_email(subject, body, recipients, sender, access_key, secret_key, region)
            print(res)

        else:
            print(f"You might need to enable manually this user {user_email}")
            return "error"
    else:
        print("There was an error while getting the user id, the user creation process failed!")
        return "error"

# Tests
username ="prueba.automation6"
create_user_automation(username=username,company='wot')