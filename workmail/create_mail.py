import boto3
import os
from dotenv import load_dotenv
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError
from password_generator import generate_password

# Load environment variables from the specified path
creds_path = r"{}\creds\.env".format(os.getcwd())
print(f"Creds path:\n{creds_path}")
load_dotenv(dotenv_path=creds_path)

def create_workmail_user(organization_id, user_email, display_name, access_key, secret_key, region):
    try:
        # Configuring the client with specified credentials and region
        client = boto3.client(
            'workmail',
            region_name=region,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )
        
        response = client.create_user(
            OrganizationId=organization_id,
            Name=user_email.split('@')[0],  # Assuming the email prefix as username
            DisplayName=display_name,
            Password=generate_password(16)  # Ensure to follow security best practices
        )
        print(f"User created successfully: {response['UserId']}")
        return response
    except NoCredentialsError:
        print("Credentials are not available.")
        return {}
    except PartialCredentialsError:
        print("Incomplete credentials passed.")
        return {}
    except ClientError as e:
        print(f"An AWS service error occurred: {e}")
        return {}
    except Exception as e:
        print(f"Failed to create user: {str(e)}")
        return {}

# # Example usage
# organization_id = os.getenv('WOT_ORGANIZATION_ID')  # Replace with your actual organization ID
# access_key = os.getenv('ACCESS_KEY')
# secret_key = os.getenv('SECRET_KEY')
# region = os.getenv('AWS_REGION', 'us-east-1')  # Default to 'us-west-2' if not specified
# user_email = 'prueba.automation3@wotdev.com'  # Replace with the actual email
# display_name = 'prueba.automation3'

# # Remember this creates the user but you have to enable it inmediately after
# payload = create_workmail_user(organization_id, user_email, display_name, access_key, secret_key, region)
