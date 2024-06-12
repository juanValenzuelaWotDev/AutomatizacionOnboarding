import boto3
import os
from dotenv import load_dotenv
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

# Load environment variables from the specified path
creds_path = r"{}\creds\.env".format(os.getcwd())
print(f"Creds path:\n{creds_path}")
load_dotenv(dotenv_path=creds_path)

def enable_workmail_user(organization_id, user_id, user_email, access_key, secret_key, region):
    try:
        # Configuring the client with specified credentials and region
        client = boto3.client(
            'workmail',
            region_name=region,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )
        
        response = client.register_to_work_mail(
            OrganizationId=organization_id,
            EntityId=user_id,  # User ID of the account to be enabled
            Email=user_email  # Email of the user to be enabled
        )
        print(f"User enabled successfully: {response}")
        return response
    except ClientError as e:
        print(f"An AWS service error occurred: {e}")
        return {}
    except Exception as e:
        print(f"Failed to enable user: {str(e)}")
        return {}

# Example usage
organization_id = os.getenv('WOT_ORGANIZATION_ID')  # From your .env file
access_key = os.getenv('ACCESS_KEY')
secret_key = os.getenv('SECRET_KEY')
region = os.getenv('AWS_REGION', 'us-east-1')
user_id = 'ca8ad72d-0dde-49e8-a936-e14c32dde7e8'  # You need to provide the User ID
user_email = 'prueba.automation2@wotdev.com'  # User email to register to WorkMail

# enable_workmail_user(organization_id, user_id, user_email, access_key, secret_key, region)
