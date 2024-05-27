import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Configura el token de tu bot aquí
slack_token = os.environ.get("SLACK_BOT_TOKEN", "-")
client = WebClient(token=slack_token)

try:
    # Llama al método users.list usando el WebClient
    response = client.users_list()
    if response["ok"]:
        users = response["members"]
        with open("miembros_activos.txt", "w") as file:
            for user in users:
                if not user.get("deleted", False):  # Verifica si el usuario está activo
                    file.write(f"ID: {user['id']}, Nombre: {user['name']}\n")
        print("Los datos se han guardado en 'miembros_activos.txt'")
    else:
        print("Error al obtener la lista de usuarios: ", response["error"])

except SlackApiError as e:
    print(f"Error al intentar acceder a la API de Slack: {e.response['error']}")
