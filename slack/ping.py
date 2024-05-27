import os
import subprocess
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import time

# Configuración de Slack
slack_token = os.environ.get("SLACK_BOT_TOKEN", "-")
client = WebClient(token=slack_token)
channel_id = "D072P9R4JGM"  # Asegúrate de reemplazar esto con tu ID de canal de Slack


def enviar_mensaje_slack(message):
    try:
        client.chat_postMessage(channel=channel_id, text=message)
        print("Mensaje enviado a Slack con éxito.")
    except SlackApiError as e:
        print(f"Error al enviar mensaje a Slack: {e.response['error']}")


def realizar_ping(host):
    # Comando de ping, ajusta según tu sistema operativo
    # Ejemplo para Windows, cambia "ping -c 4" a "ping -n 4" si es necesario
    command = ["ping", "-c", "4", host]
    try:
        output = subprocess.run(command, capture_output=True, text=True, check=True)
        return True, output.stdout
    except subprocess.CalledProcessError:
        return False, None


# Host que deseas monitorear
host = "https://repuestosus.com/"
intervalo = 60 * 5  # Monitoreo cada 5 minutos

while True:
    success, result = realizar_ping(host)
    if not success:
        enviar_mensaje_slack(
            f"ALERTA: El host {host} no responde a ping. Por favor revisar la conectividad."
        )
    else:
        print(f"Ping exitoso a {host}: {result}")
    time.sleep(intervalo)
