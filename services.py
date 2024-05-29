import os, sys
from dotenv import load_dotenv

# Store the credentials in global variables for easy access
slack_token = ""
# Amazon workmail credentials
workmail = ""
workmail_user = ""
workmail_password = ""
# Google cloud API credentials (same email as in workmail)
google_password  = ""
# AWS SES keys of the IAM user with access
access_key = ""
secret_key = ""
# WotDev
organization_id = ""

# Slack bot member id
slack_bot_member_id = ""

def load_creds(env:str="stag"):
    global slack_token, workmail, workmail_user, workmail_password, google_password, access_key, secret_key, organization_id, slack_bot_member_id
    # Standard procedure for staging or production
    if env == "prod":
        print("Loading production access keys")
    else:
        print("loading staging access keys")
        env_path = r"{}\creds\.env".format(os.getcwd())
        load_dotenv(dotenv_path=env_path)
        # Update global variables
        # Slack bot
        slack_token = os.getenv('SLACK_TOKEN_JAVIERAS')
        # slack_bot_member_id = os.getenv('SLACK_BOT_MEMBER_ID')
        slack_bot_member_id = os.getenv('JP_MEMBER_ID')

        # Workmail automation
        workmail = os.getenv('WORKMAIL')
        workmail_user = os.getenv('WORKMAIL_USER')
        workmail_password = os.getenv('WORKMAIL_PASSWORD')

        # Google sheets automation
        google_password = os.getenv('GOOGLE_PASSWORD')

        # AWS automation (SES)
        access_key = os.getenv('ACCESS_KEY')
        secret_key = os.getenv('SECRET_KEY')
        organization_id = os.getenv('ORGANIZATION_ID')
        