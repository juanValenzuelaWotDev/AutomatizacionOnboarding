import os
import boto3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from botocore.exceptions import ClientError

def send_email_with_attachment(subject, body, recipients, sender, file_path, access_key, secret_key):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)

    msg.attach(MIMEText(body, 'plain'))

    try:
        with open(file_path, "rb") as attachment:
            part = MIMEApplication(attachment.read(), Name=os.path.basename(file_path))
            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            msg.attach(part)
    except IOError:
        print(f"Could not open attachment file {file_path}.")
        return

    raw_message = msg.as_string()

    try:
        client = boto3.client('ses', region_name='us-east-1', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
        response = client.send_raw_email(Source=sender, Destinations=recipients, RawMessage={'Data': raw_message})
        print("Email sent successfully! Message ID:", response['MessageId'])
    except ClientError as e:
        print("Failed to send email:", e)

