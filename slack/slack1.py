import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Configura el token de tu bot aquí
slack_token = os.environ.get("SLACK_BOT_TOKEN", "-")
client = WebClient(token=slack_token)

# Lista para almacenar los IDs de conversación
channel_ids = []

# Solicita los IDs de usuario y abre las conversaciones
for i in range(3):
    user_id = input(f"Ingresa el ID del usuario {i+1}: ")
    try:
        # Llama al método conversations.open usando el WebClient
        response = client.conversations_open(users=[user_id])
        channel_id = response["channel"]["id"]
        channel_ids.append(channel_id)
        print(f"ID de la conversación con el usuario {user_id}: {channel_id}")
    except SlackApiError as e:
        print(f"Error al abrir conversación con {user_id}: {e.response['error']}")

# Ahora channel_ids contiene los IDs de las conversaciones de los 3 usuarios
print("IDs de las conversaciones:", channel_ids)
