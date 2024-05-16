import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import calendar
import locale
import string
import time
import os
from gspread_formatting import CellFormat, Color, format_cell_range

# Configurar la localización a español
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

# Definir el alcance
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Función para encontrar el archivo de credenciales
def find_credentials_file(file_name):
    for root, dirs, files in os.walk("."):
        if file_name in files:
            return os.path.join(root, file_name)
    raise FileNotFoundError(f"No se encontró el archivo {file_name}")

credentials_path = find_credentials_file("wot_automation.json")
outDir = os.path.dirname(credentials_path)


def authenticate():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
    return gspread.authorize(credentials)

client = authenticate()

base_datos_url = "https://docs.google.com/spreadsheets/d/1PKOguOYbnSRFUNuf8G5f73RDorkQZ2Z5GhPBYp5sCQY/edit#gid=0"
base_datos = client.open_by_url(base_datos_url)
hoja_base_datos = base_datos.sheet1 

fila = 2
wait_time = 60  

default_emails = ["juanvalenzuela4business@gmail.com","carla.hernandez.wot@gmail.com"]

def create_new_sheet(client, nombre_hoja, correos):
    while True:
        try:
            spreadsheet = client.create(nombre_hoja)
            for correo in correos:
                spreadsheet.share(correo, perm_type="user", role="writer")
            return spreadsheet
        except gspread.exceptions.APIError as e:
            if e.response.status_code in [403, 429]:
                print(f"Error de permiso o cuota excedida al crear la hoja: {e.response.content}. Esperando {wait_time} segundos antes de reintentar...")
                time.sleep(wait_time)
            else:
                raise

def open_source_spreadsheet(client, source_spreadsheet_url):
    while True:
        try:
            # Extraer ID de la hoja de cálculo desde la URL
            sheet_id = source_spreadsheet_url.split('/d/')[1].split('/')[0]
            print(f"Abriendo la hoja de cálculo con ID: {sheet_id}")
            return client.open_by_key(sheet_id)
        except gspread.exceptions.APIError as e:
            if e.response.status_code in [403, 429]:
                print(f"Error de permiso o cuota excedida al abrir la hoja de cálculo fuente: {e.response.content}. Esperando {wait_time} segundos antes de reintentar...")
                time.sleep(wait_time)
            else:
                raise
        except PermissionError as e:
            print(f"Error de permiso al abrir la hoja de cálculo fuente: {e}. Esperando {wait_time} segundos antes de reintentar...")
            time.sleep(wait_time)

while True:
    try:
        nombre_editor = hoja_base_datos.cell(fila, 1).value
        correo_editor = hoja_base_datos.cell(fila, 2).value
        empresa = hoja_base_datos.cell(fila, 4).value
        project_code = hoja_base_datos.cell(fila, 5).value
        date_of_joining = hoja_base_datos.cell(fila, 6).value
        manager = hoja_base_datos.cell(fila, 7).value
        spreadsheet_link = hoja_base_datos.cell(fila, 8).value
        correo_adicional = hoja_base_datos.cell(fila, 15).value  

        if not nombre_editor:
            print("No hay más nombres en la columna A. Deteniendo la ejecución.")
            break

        if not spreadsheet_link:
            print(f"No se encontró enlace para {nombre_editor}, creando nueva hoja...")
            nombre_hoja = f"Monthly {nombre_editor}"
            correos = [correo_editor]   + default_emails + ([correo_adicional] if correo_adicional else [])
            spreadsheet = create_new_sheet(client, nombre_hoja, correos)

            hoy = datetime.datetime.now()
            if hoy.day >= 28:
                siguiente_mes = hoy.replace(day=1) + datetime.timedelta(days=32)
                siguiente_mes = siguiente_mes.replace(day=1)
            else:
                siguiente_mes = hoy

            year = siguiente_mes.year
            month = siguiente_mes.month
            nombre_mes = siguiente_mes.strftime("%B %y").title()
            days_in_month = calendar.monthrange(year, month)[1]

            if empresa == "Wot":
                source_spreadsheet_url = "https://docs.google.com/spreadsheets/d/1sTKB6-AMfsUcKc4noHKVO7pAQ0STsgLwlV2-6Y26hFY/edit#gid=2135775601"
            elif empresa == "Bot":
                source_spreadsheet_url = "https://docs.google.com/spreadsheets/d/1sfTtG9fDJJWaHc9UbS9ERT2qDbuDVjGmh_CoM_o4m5E/edit#gid=1289690781"
            elif empresa in ["WotBot", "BotWot"]:
                source_spreadsheet_url = "https://docs.google.com/spreadsheets/d/1nllo1Ic-QsL5efUE2S0GaEwS6tjSLIsISNxIKGlW5-0/edit#gid=1718690455"
            else:
                print(f"Empresa desconocida: {empresa}. Saltando fila.")
                fila += 1
                continue

            print(f"Abriendo el documento fuente para la empresa {empresa}")
            source_spreadsheet = open_source_spreadsheet(client, source_spreadsheet_url)

            source_worksheet = source_spreadsheet.worksheet(f"{days_in_month} días")
            source_worksheet.copy_to(spreadsheet.id)

            worksheet = spreadsheet.get_worksheet(0)
            spreadsheet.del_worksheet(worksheet)
            worksheet = spreadsheet.get_worksheet(0)
            worksheet.update_title(nombre_mes)
            
            
            worksheet.update_acell('B6', nombre_editor)
            worksheet.update_acell('B7', manager)
            worksheet.update_acell('B8', date_of_joining)
            worksheet.update_acell('G6', project_code)
            worksheet.update_acell('A10', nombre_mes)

            num_dias = calendar.monthrange(year, month)[1]
            numeros_dias = [[str(i)] for i in range(1, num_dias + 1)]
            fechas_dias = [[datetime.datetime(year, month, i).strftime("%d-%m-%Y")] for i in range(1, num_dias + 1)]
            dias_semana = [[datetime.datetime(year, month, i).strftime("%a")] for i in range(1, num_dias + 1)]

            worksheet.update(range_name=f'A12:A{11 + num_dias}', values=numeros_dias)
            worksheet.update(range_name=f'B12:B{11 + num_dias}', values=fechas_dias)
            worksheet.update(range_name=f'C12:C{11 + num_dias}', values=dias_semana)

            weekend_color = Color(0.714, 0.714, 0.714) 
            weekend_format = CellFormat(backgroundColor=weekend_color)

            for i in range(1, num_dias + 1):
                fecha = datetime.datetime(year, month, i)
                if fecha.weekday() in [5, 6]:
                    format_cell_range(worksheet, f'A{11+i}:J{11+i}', weekend_format)

            fechas = [
                "01-01-2024", "29-03-2024", "30-03-2024", "01-05-2024", "01-07-2024",
                "15-08-2024", "15-09-2024", "20-10-2024", "01-11-2024", "25-12-2024", "31-12-2024"
            ]

            gray_format = CellFormat(backgroundColor=Color(0.714, 0.714, 0.714))
            date_cells = worksheet.range('B12:B' + str(11 + num_dias))

            for cell in date_cells:
                if cell.value in fechas:
                    row_number = cell.row 
                    format_range = f'A{row_number}:G{row_number}'  
                    format_cell_range(worksheet, format_range, gray_format) 

            # Verificar y formatear si hay datos en la celda L6
            datos_celda_L6 = worksheet.acell('L6').value
            if datos_celda_L6:
                for i in range(1, num_dias + 1):
                    fecha = datetime.datetime(year, month, i)
                    if fecha.weekday() in [5, 6]:
                        format_cell_range(worksheet, f'L{11+i}:U{11+i}', weekend_format)

                date_cells = worksheet.range('M12:M' + str(11 + num_dias))
                for cell in date_cells:
                    if cell.value in fechas:
                        row_number = cell.row
                        format_range = f'L{row_number}:U{row_number}'
                        format_cell_range(worksheet, format_range, gray_format)

            spreadsheet_url = spreadsheet.url
            cell_label = f'H{fila}'  
            hoja_base_datos.update_acell(cell_label, spreadsheet_url)
            
            print(f"Insertado el link en {cell_label} con el enlace a {nombre_hoja}")
            time.sleep(20)
        else:
            print(f"Ya existe un enlace para {nombre_editor}, omitiendo la creación de la hoja.")

    except gspread.exceptions.APIError as e:
        if e.response.status_code in [403, 429]:
            print(f"Error de permiso o cuota excedida: {e.response.content}. Reautenticando y esperando {wait_time} segundos antes de reintentar...")
            client = authenticate()
            time.sleep(wait_time)
        else:
            raise
    except PermissionError as e:
        print(f"Error de permiso: {e}. Reautenticando y esperando {wait_time} segundos antes de reintentar...")
        client = authenticate()
        time.sleep(wait_time)

    fila += 1
    time.sleep(30)
