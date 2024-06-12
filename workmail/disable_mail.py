import boto3
import os
from dotenv import load_dotenv
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

# Load environment variables from the specified path
creds_path = r"{}\creds\.env".format(os.getcwd())
print(f"Creds path:\n{creds_path}")
load_dotenv(dotenv_path=creds_path)

def disable_workmail_user(organization_id, user_id, access_key, secret_key, region):
    try:
        # Configuring the client with specified credentials and region
        client = boto3.client(
            'workmail',
            region_name=region,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )
        
        response = client.deregister_from_work_mail(
            OrganizationId=organization_id,
            EntityId=user_id  # User ID of the account to be disabled
        )
        print(f"User disabled successfully: {response}")
        return response
    except ClientError as e:
        print(f"An AWS service error occurred: {e}")
        return {}
    except Exception as e:
        print(f"Failed to disable user: {str(e)}")
        return {}

# Example usage
organization_id = os.getenv('WOT_ORGANIZATION_ID')  # From your .env file
access_key = os.getenv('ACCESS_KEY')
secret_key = os.getenv('SECRET_KEY')
region = os.getenv('AWS_REGION', 'us-east-1')
user_id = 'd4a76c69-d488-4bb6-a1d8-aa8e638e6ee4'  # You need to provide the User ID

disable_workmail_user(organization_id, user_id, access_key, secret_key, region)
