import requests
import time


def verificar_sitio(url):
    start_time = time.time()
    try:
        # Establece un timeout de 10 segundos
        response = requests.get(url, timeout=10)
        response_time = time.time() - start_time
        if response.status_code == 200:
            message = f"{time.strftime('%Y-%m-%d %H:%M:%S')} - El sitio {url} está activo. Tiempo de respuesta: {response_time:.2f} segundos\n"
        else:
            message = f"{time.strftime('%Y-%m-%d %H:%M:%S')} - El sitio {url} está inactivo. Código de estado: {response.status_code}. Tiempo de respuesta: {response_time:.2f} segundos\n"
    except requests.RequestException as e:
        response_time = time.time() - start_time
        message = f"{time.strftime('%Y-%m-%d %H:%M:%S')} - No se pudo acceder al sitio {url}. Error: {e}. Tiempo de respuesta: {response_time:.2f} segundos\n"

    with open("log_monitoreo.txt", "a") as file:
        file.write(message)
    print(message)


url = "http://thebotdev.com/"  # Reemplaza con tu URL
intervalo = 60  # Intervalo en segundos

while True:
    verificar_sitio(url)
    time.sleep(intervalo)
