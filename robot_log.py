import logging
from datetime import date
import os
# This is the robot name, customize it in every bot
robot_name = "Email automation"
# Configuration of the logging system

# find out if there is a folder and if it is missing then create it
def delete_old_logs(folder_path, date):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if date not in file:
                os.remove(os.path.join(root, file))
def create_folder():
    logs_folder = r"{}\logs".format(os.getcwd())
    if not(os.path.exists(logs_folder)):
        os.mkdir(logs_folder)
def start_logger(nit:str=''):
    # First get the current date
    today = date.today()
    # Save log by date
    d1 = today.strftime("%Y%m%d") + ".log"
    # Save log by date and nit
    # d1 = r"{}_{}.log".format(today.strftime("%Y%m%d"),nit)
    d2 = r"{}\logs\{}".format(os.getcwd(),d1)
    # Check for the folder
    create_folder()
    # Configure the filename
    logging.basicConfig(filename=d2, format=f"%(asctime)s - {robot_name} - %(message)s", level=logging.INFO)


# End result
# 2024-01-10 14:43:30 - INCUMPLIMIENTOS - Llamada a API de incumplimientos con los siguientes valores: [datos que se van a enviar a la API]
# 2024-01-10 14:43:30 - INCUMPLIMIENTOS - Respuesta de API de incumplimientos: [datos que se reciben de la API]

# Tests
# start_logger(robot_name)

# response = """{ 'test1': 'sample'}"""
# logging.info(f"Respuesta de API de incumplimientos: {response}")


# To do list
# que ya no se genere el log.txt con los logs de excel - 
# arreglar el error de fallo de convertir string a float - listo
# agregar el nit al nombre del log - listo
# borrar los logs cada dia diferente en la carpeta de logs - listo