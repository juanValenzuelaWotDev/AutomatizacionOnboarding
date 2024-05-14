import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Configura el token de tu bot aquí
slack_token = os.environ.get("SLACK_BOT_TOKEN", "-")
client = WebClient(token=slack_token)

# ID de la conversación obtenido previamente
member_id = "U049LKDBKDM"

try:
    # Enviar un mensaje al ID de la conversación específico
    response = client.chat_postMessage(
        channel=member_id,
        text="¡Hola! Este es un mensaje de prueba",
    )
    print("Mensaje enviado con éxito.")
except SlackApiError as e:
    print(f"Error al enviar mensaje: {e.response['error']}")
