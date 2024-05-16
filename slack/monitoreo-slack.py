import requests
import time
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os

# Configuración de Slack
slack_token = os.environ.get("SLACK_BOT_TOKEN", "")
client = WebClient(token=slack_token)

# IDs de canal para las conversaciones directas de las tres personas
person_1_channel_id = os.environ.get("PERSON_1_CHANNEL_ID", "")
person_2_channel_id = os.environ.get("PERSON_2_CHANNEL_ID", "")
person_3_channel_id = os.environ.get("PERSON_3_CHANNEL_ID", "")

# Lista de URLs a monitorear
urls = ["https://thebotdev.com/", "https://repuestosus.com/", "https://wotdev.com/"]


def verificar_sitio(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print(
                f"{time.strftime('%Y-%m-%d %H:%M:%S')} - El sitio {url} está activo.\n"
            )
        else:
            message = f"{time.strftime('%Y-%m-%d %H:%M:%S')} - El sitio {url} está inactivo. Código de estado: {response.status_code}\n"
            enviar_mensaje_slack(message)
    except requests.RequestException as e:
        message = f"{time.strftime('%Y-%m-%d %H:%M:%S')} - No se pudo acceder al sitio {url}. Error: {e}\n"
        enviar_mensaje_slack(message)


def enviar_mensaje_slack(message):
    channel_ids = [person_1_channel_id, person_2_channel_id, person_3_channel_id]
    for channel_id in channel_ids:
        try:
            client.chat_postMessage(channel=channel_id, text=message)
            print(f"Mensaje enviado a Slack con éxito al canal {channel_id}.")
        except SlackApiError as e:
            print(f"Error al enviar mensaje a Slack: {e.response['error']}")


# Monitorear los sitios una vez al iniciar el script
for url in urls:
    verificar_sitio(url)
