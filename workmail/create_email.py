import boto3

def create_workmail_user(organization_id, user_name, display_name, password):
    client = boto3.client('workmail')
    try:
        response = client.create_user(
            OrganizationId=organization_id,
            Name=user_name,
            DisplayName=display_name,
            Password=password
        )
        print("User created successfully:", response['UserId'])
        return response['UserId']
    except Exception as e:
        print("An error occurred:", str(e))

def assign_email_address(organization_id, user_id, email):
    client = boto3.client('workmail')
    try:
        response = client.register_to_work_mail(
            OrganizationId=organization_id,
            EntityId=user_id,
            Email=email
        )
        print("Email assigned successfully:", response)
    except Exception as e:
        print("Failed to assign email:", str(e))



# Example usage
organization_id = 'o-c0nz3grfqp'  # You need to replace this with your real Organization ID
user_name = 'juan.testing'
display_name = 'Juan Pablo Test'
password = 'StrongPassword123!'  # Ensure you comply with your organization's password policy
user_id = create_workmail_user(organization_id, user_name, display_name, password)


# Example usage Assign an email
# user_id = 'A1234567890123456789012345'  # Replace with the UserId from the create_user response
email = f'{user_name}@wotdev.com'  # Replace with the desired email address
assign_email_address(organization_id, user_id, email)

