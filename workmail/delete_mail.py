import boto3
import os
from dotenv import load_dotenv
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

# Load environment variables from the specified path
creds_path = r"{}\creds\.env".format(os.getcwd())
print(f"Creds path:\n{creds_path}")
load_dotenv(dotenv_path=creds_path)


def delete_workmail_user(organization_id, user_id, access_key, secret_key):
    try:
        # Configuring the client with specified credentials and region
        client = boto3.client(
            'workmail',
            region_name='us-east-1',  # Using your specified AWS region
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )
        
        response = client.delete_user(
            OrganizationId=organization_id,
            UserId=user_id  # User ID of the account to be deleted
        )
        print(f"User deleted successfully: {response}")
    except ClientError as e:
        print(f"An AWS service error occurred: {e}")
    except Exception as e:
        print(f"Failed to delete user: {str(e)}")

# Example usage
organization_id = os.getenv('WOT_ORGANIZATION_ID')  # From your .env file
access_key = os.getenv('ACCESS_KEY')
secret_key = os.getenv('SECRET_KEY')
user_id = 'user_id_of_the_account_to_delete'  # You need to provide the User ID

delete_workmail_user(organization_id, user_id, access_key, secret_key)
