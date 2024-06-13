import boto3
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError
from dotenv import load_dotenv

# Load environment variables from the specified path
# creds_path = r"{}\creds\.env".format(os.getcwd())
# print(f"Creds path:\n{creds_path}")
# load_dotenv(dotenv_path=creds_path)

def send_email(subject, body, recipients, sender, access_key, secret_key, region='us-east-1'):
    # Create a multipart message
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)

    # Attach the body with MIMEText
    msg.attach(MIMEText(body, 'plain'))

    # Convert the message to a string
    raw_message = msg.as_string()

    try:
        # Initialize SES client
        client = boto3.client('ses', region_name=region, aws_access_key_id=access_key, aws_secret_access_key=secret_key)
        # Send the email
        response = client.send_raw_email(
            Source=sender,
            Destinations=recipients,
            RawMessage={'Data': raw_message}
        )
        print("Email sent successfully! Message ID:", response['MessageId'])
        return response
    except ClientError as e:
        print("Failed to send email:", e)

# # Example usage
# subject = "Hello from WorkMail"
# body = "This is a test email from AWS WorkMail."
# recipients = ['prueba.automation1@wotdev.com','prueba.automation2@wotdev.com']  # List of email recipients
# sender = 'javieras@wotdev.com'  # Your WorkMail email address
# access_key = os.getenv('ACCESS_KEY')
# secret_key = os.getenv('SECRET_KEY')
# region = os.getenv('AWS_REGION', 'us-east-1') #default to 'us-east-1'

# send_email(subject, body, recipients, sender, access_key, secret_key, region)
