import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Establece el token de tu bot aquí
slack_token = os.environ.get("SLACK_BOT_TOKEN", "-")

client = WebClient(token=slack_token)

try:
    # Llama al método conversations.list usando el WebClient
    result = client.conversations_list()
    conversations = result["channels"]  # Asume que la respuesta está paginada simple

    for conversation in conversations:
        # Imprime los detalles del canal
        print(f"ID: {conversation['id']}, Nombre: {conversation['name']}")

except SlackApiError as e:
    print(f"Error: {e.response['error']}")  # Muestra el error específico de Slack
