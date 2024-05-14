import requests
import time
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os

# Configuración de Slack
slack_token = os.environ.get("SLACK_BOT_TOKEN", "-")
client = WebClient(token=slack_token)

# IDs de canal para las conversaciones directas de las tres personas
person_1_channel_id = "D072UHCMTE0"
person_2_channel_id = "D0736NJ44TD"
person_3_channel_id = "D07392K6VGU"


# Función para verificar el sitio web
def verificar_sitio(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            message = (
                f"{time.strftime('%Y-%m-%d %H:%M:%S')} - El sitio {url} está activo.\n"
            )
        else:
            message = f"{time.strftime('%Y-%m-%d %H:%M:%S')} - El sitio {url} está inactivo. Código de estado: {response.status_code}\n"
    except requests.RequestException as e:
        message = f"{time.strftime('%Y-%m-%d %H:%M:%S')} - No se pudo acceder al sitio {url}. Error: {e}\n"
    return message


# Función para enviar mensaje a Slack
def enviar_mensaje_slack(message):
    channel_ids = [person_1_channel_id, person_2_channel_id, person_3_channel_id]
    for channel_id in channel_ids:
        try:
            client.chat_postMessage(channel=channel_id, text=message)
            print(f"Mensaje enviado a Slack con éxito al canal {channel_id}.")
        except SlackApiError as e:
            print(f"Error al enviar mensaje a Slack: {e.response['error']}")


# URL del sitio que deseas monitorear
url = "https://wotdev.com/"
intervalo = 60 * 60  # Intervalo en segundos

while True:
    result = verificar_sitio(url)
    with open("log_monitoreo.txt", "a") as file:
        file.write(result)
    enviar_mensaje_slack(result)
    time.sleep(intervalo)
