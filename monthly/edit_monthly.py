from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from gspread_formatting import CellFormat, Color, Border, Borders, format_cell_range
import string
from datetime import datetime, timedelta
from calendar import monthrange
import gspread
import locale
import calendar
import time
import re
import os

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

# Definir el alcance y autenticarse
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

# Función para encontrar el archivo de credenciales
def find_credentials_file(file_name):
    for root, dirs, files in os.walk("."):
        if file_name in files:
            return os.path.join(root, file_name)
    raise FileNotFoundError(f"No se encontró el archivo {file_name}")

credentials_path = find_credentials_file("wot_automation.json")
credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)

client = gspread.authorize(credentials)
service = build('sheets', 'v4', credentials=credentials)
spreadsheet_id = '1PKOguOYbnSRFUNuf8G5f73RDorkQZ2Z5GhPBYp5sCQY'    

def get_month_name():
    today = datetime.now()
    if today.day >= 28:
        next_month = today.replace(day=28) + timedelta(days=4)
        return next_month.strftime('%B %y').capitalize()
    else:
        return today.strftime('%B %y').capitalize()

links_and_month_sheets = {}
processed_links = set()
def procesar_enlaces_monthly(spreadsheet_id, empresa,nombre,correo):
    global links_and_month_sheets
    global processed_links
    
    range_name = 'Hoja 1!H2:H'
    result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get('values', [])

    if not values:
        print('No se encontraron más datos.')
    else:
        for row in values:
            if row:
                url = row[0]
                linked_spreadsheet_id = re.search(r'/spreadsheets/d/([a-zA-Z0-9-_]+)', url).group(1) if re.search(r'/spreadsheets/d/([a-zA-Z0-9-_]+)', url) else None
                if linked_spreadsheet_id:
                    month_name = get_month_name()
                    if url not in processed_links:
                        try:
                            linked_sheets_metadata = service.spreadsheets().get(spreadsheetId=linked_spreadsheet_id).execute()
                            existing_sheets = [s['properties']['title'].capitalize() for s in linked_sheets_metadata['sheets']]
                            if month_name not in existing_sheets:
                                # Verificar el número de días en el mes
                                days_in_month = monthrange(datetime.now().year, datetime.now().month)[1]
                                # Seleccionar el documento fuente basado en la empresa
                                if empresa == "Wot":
                                    source_spreadsheet_url = "https://docs.google.com/spreadsheets/d/1sTKB6-AMfsUcKc4noHKVO7pAQ0STsgLwlV2-6Y26hFY/edit#gid=2135775601"
                                elif empresa == "Bot":
                                    source_spreadsheet_url = "https://docs.google.com/spreadsheets/d/1sfTtG9fDJJWaHc9UbS9ERT2qDbuDVjGmh_CoM_o4m5E/edit#gid=1289690781"
                                elif empresa == "WotBot" or empresa == "BotWot":
                                    source_spreadsheet_url = "https://docs.google.com/spreadsheets/d/1nllo1Ic-QsL5efUE2S0GaEwS6tjSLIsISNxIKGlW5-0/edit#gid=1718690455"

                                # Abrir el documento fuente que contiene las hojas de 28, 29, 30, 31 días
                                source_spreadsheet = client.open_by_url(source_spreadsheet_url)
                                # Seleccionar la hoja correspondiente al número de días del mes
                                source_worksheet = source_spreadsheet.worksheet(f"{days_in_month} días")
                                # Duplicar la hoja correspondiente al nuevo libro de Google Sheets
                                new_sheet = source_worksheet.copy_to(linked_spreadsheet_id)
                                new_sheet_id = new_sheet['sheetId']
                                new_sheet_title = month_name

                                # Renombrar la nueva hoja con el nombre del mes adecuado
                                requests = [{
                                    'updateSheetProperties': {
                                        'properties': {
                                            'sheetId': new_sheet_id,
                                            'title': new_sheet_title
                                        },
                                        'fields': 'title'
                                    }
                                }]
                                body = {
                                    'requests': requests
                                }
                                service.spreadsheets().batchUpdate(spreadsheetId=linked_spreadsheet_id, body=body).execute()
                                print(f"Hoja de {new_sheet_title} creada y renombrada en el libro {linked_spreadsheet_id}")
                                # Mover la hoja copiada a la primera posición (izquierda)
                                service.spreadsheets().batchUpdate(
                                    spreadsheetId=linked_spreadsheet_id,
                                    body={
                                        "requests": [
                                            {
                                                "updateSheetProperties": {
                                                    "properties": {
                                                        "sheetId": new_sheet['sheetId'],
                                                        "index": 0
                                                    },
                                                    "fields": "index"
                                                }
                                            }
                                        ]
                                    }
                                ).execute()

                                # Abrir la hoja recién creada y renombrada
                                worksheet = client.open_by_key(linked_spreadsheet_id).worksheet(new_sheet_title)

                                # Actualizar la hoja con el nombre del mes y los encabezados
                                actualizar_hoja_mes(worksheet, month_name, datetime.now().year, datetime.now().month)

                                links_and_month_sheets[url] = month_name
                            else:
                                print(f"Hoja de {month_name} ya existía en {url}")
                                links_and_month_sheets[url] = month_name
                        except Exception as e:
                            print(f"Error al acceder o modificar la hoja de cálculo vinculada en {url}: {e}")
                        processed_links.add(url)
                   
                else:
                    print(f"URL no válida o no encontrada en la fila: {row}")
                links_and_month_sheets[url] = month_name
                processed_links.add(url)
                    
                worksheet = client.open_by_key(linked_spreadsheet_id).worksheet(month_name) 
                worksheet.update_acell('B6', nombre)

def actualizar_hoja_mes(worksheet, nombre_mes, year, month):
    # Actualizar la celda con el nombre del mes
    worksheet.update_acell('A10', nombre_mes)


# Calcular el número de días del mes
    num_dias = calendar.monthrange(year, month)[1]

# Crear lista de números, fechas y días
    numeros_dias = [[str(i)] for i in range(1, num_dias + 1)]
    fechas_dias = [[datetime(year, month, i).strftime("%d-%m-%Y")] for i in range(1, num_dias + 1)]

    locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')
    dias_semana = [[datetime(year, month, i).strftime("%a")] for i in range(1, num_dias + 1)]
    print("Editando")
    # Rellenar la columna A con los números
    worksheet.update(range_name=f'A12:A{11 + num_dias}', values=numeros_dias)

        # Rellenar la columna B con las fechas
    worksheet.update(range_name=f'B12:B{11 + num_dias}', values=fechas_dias)

        # Rellenar la columna C with los días de la semana
    worksheet.update(range_name=f'C12:C{11 + num_dias}', values=dias_semana)

        # Estilo de borde
    border = Border("SOLID", Color(0, 0, 0))
    borders = Borders(border, border, border, border)

   

        # Obtener todas las letras mayúsculas del alfabeto
    column_letters = {i: letter for i, letter in enumerate(string.ascii_uppercase, start=1)}
        # Aplicar formato para los días sábado y domingo
    weekend_color = Color(0.714, 0.714, 0.714)  # Gris
    weekend_format = CellFormat(backgroundColor=weekend_color)

        # Identificar y marcar todos los sábados y domingos del mes
    for i in range(1, num_dias + 1):
            fecha = datetime(year, month, i)
            if fecha.weekday() == 5 or fecha.weekday() == 6:
                format_cell_range(worksheet, f'A{11+i}:G{11+i}', weekend_format)
    fechas = [
            "01-01-2024",
            "29-03-2024",
            "30-03-2024",
            "01-05-2024",
            "01-07-2024",
            "15-08-2024",
            "15-09-2024",
            "20-10-2024",
            "01-11-2024",
            "25-12-2024",
            "31-12-2024"
        ]
        

    gray_format = CellFormat(backgroundColor=Color(0.714, 0.714, 0.714))
        # Obtener todas las fechas en la columna "Date" desde la fila 12
    date_cells = worksheet.range('B12:B' + str(worksheet.row_count))

        # Aplicar el formato a las filas completas que tienen fechas coincidentes
    for cell in date_cells:
            if cell.value in fechas:
                row_number = cell.row 
                format_range = f'A{row_number}:G{row_number}'  
  
                format_cell_range(worksheet, format_range, gray_format) 
    # Primero, verifica si hay datos en la celda L6
    datos_celda_L6 = worksheet.acell('L6').value

    if datos_celda_L6: 
        # Identificar y marcar todos los sábados y domingos del mes
        for i in range(1, num_dias + 1):
            fecha = datetime(year, month, i)
            # Comprueba si el día es sábado (5) o domingo (6)
            if fecha.weekday() == 5 or fecha.weekday() == 6:
                # Formatea el rango de celdas para ese día específico
                format_cell_range(worksheet, f'L{11+i}:U{11+i}', weekend_format)
      
        # Obtener todas las fechas en la columna "Date" desde la fila 12
        date_cells = worksheet.range('M12:M' + str(worksheet.row_count))

        # Aplicar el formato a las filas completas que tienen fechas coincidentes
        for cell in date_cells:
            if cell.value in fechas:
                row_number = cell.row
                format_range = f'L{row_number}:U{row_number}'
                format_cell_range(worksheet, format_range, gray_format)

 
    time.sleep(20)
    

# Abrir la hoja de cálculo de la base de datos
base_datos_url = "https://docs.google.com/spreadsheets/d/1PKOguOYbnSRFUNuf8G5f73RDorkQZ2Z5GhPBYp5sCQY/edit#gid=0"
base_datos = client.open_by_url(base_datos_url)
# Seleccionar la hoja donde están los datos
hoja_base_datos = base_datos.sheet1
nombres = hoja_base_datos.col_values(1)[1:]
correos = hoja_base_datos.col_values(2)[1:]
empresas = hoja_base_datos.col_values(4)[1:]
project_code = hoja_base_datos.col_values(5)[1:]
date_of_joining = hoja_base_datos.col_values(6)[1:]
reporting_manager = hoja_base_datos.col_values(7)[1:]
spreadsheet_links = hoja_base_datos.col_values(8)[1:]



for empresa, nombre,reporting_manager in zip(empresas, nombres,reporting_manager):
    procesar_enlaces_monthly(spreadsheet_id, empresa, nombre,reporting_manager)
    
    