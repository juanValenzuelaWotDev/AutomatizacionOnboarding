from oauth2client.service_account import ServiceAccountCredentials
import gspread
from gspread_formatting import CellFormat, Color, format_cell_range
import os, sys
# Take the main path of AutomatizacionOnboarding and use it as normal
sys.path.insert(1, "/".join(os.path.realpath(__file__).split("/")[0:-2]))

import bot_paths
from fill_word_document.database import save_info_to_database
from num2words import num2words
# To get the current date
from datetime import date

# Global variables
current_date = date.today()

# Function definition
def month2text(month_number:int):
    # In spanish
    mappings = {
        1:"enero",
        2:"febrero",
        3:"marzo",
        4:"abril",
        5:"mayo",
        6:"junio",
        7:"julio",
        8:"agosto",
        9:"septiembre",
        10:"octubre",
        11:"noviembre",
        12:"diciembre"
    }
    # For english mappings you can use a standard library
    return mappings[month_number]

# This function downloads the whole table
def download_data(row=2, export=False):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(f"{os.getcwd()}/creds/create-monthly.json", scope)
    client = gspread.authorize(credentials)

    base_datos_url = "https://docs.google.com/spreadsheets/d/19WkLk17u0IIvu6-7Nd2CXdOU0R9HflParD_YVUU_wSY/edit#gid=0"
    spreadsheet_id = "19WkLk17u0IIvu6-7Nd2CXdOU0R9HflParD_YVUU_wSY"
    base_datos = client.open_by_url(base_datos_url)
    hoja_base_datos = base_datos.sheet1

    print("Found hoja base datos")

    columnas = hoja_base_datos.col_values
    numero_filas = hoja_base_datos.row_count #todas las filas del documento aunque no esten vacias
    print(f"Numero de filas {numero_filas}")
    
    # Do a for loop to look for the data that you want

    fecha_inicio = hoja_base_datos.acell(f'I{row}').value
    fecha_inicio = fecha_inicio.split("/")

    pago_mes = int(hoja_base_datos.acell(f'W{row}').value)
    pago_mes_quetzales = int(hoja_base_datos.acell(f'X{row}').value)
    pago_hora = hoja_base_datos.acell(f'U{row}').value
    database_filename = hoja_base_datos.acell(f'A{row}').value.replace(" ","_")

    data_to_replace_empleado = {
        'nombre_empleado' : hoja_base_datos.acell(f'A{row}').value,
        'anio': str(current_date.year),
        'mes': month2text(current_date.month),
        'dia': str(current_date.day),
        'puesto': hoja_base_datos.acell(f'R{row}').value,
        'cliente': hoja_base_datos.acell(f'S{row}').value,
        'dia_inicio': fecha_inicio[0],
        'mes_inicio': month2text(int(fecha_inicio[1])),
        'anio_inicio': f"20{fecha_inicio[2]}",
        'duracion_puesto': hoja_base_datos.acell(f'Q{row}').value,
        'pago_texto_hora': num2words(pago_hora, lang='es'),
        'pago_hora': pago_hora,
        'pago_texto_mes': num2words(pago_mes, lang='es'),
        'pago_mes': str(pago_mes),
        'pago_texto_mes_quetzales': num2words(pago_mes_quetzales, lang='es'),
        'pago_mes_quetzales': str(pago_mes_quetzales),
        'modalidad': hoja_base_datos.acell(f'T{row}').value,
    }
    # save as a json file
    if (export):
        save_info_to_database(str(data_to_replace_empleado).replace("'",'"'),f'info_empleado_{database_filename}.json')

    return data_to_replace_empleado

def get_person_data(search_name:str, export:bool = False):
    # Get the worksheet
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(f"{os.getcwd()}/creds/create-monthly.json", scope)
    client = gspread.authorize(credentials)

    base_datos_url = "https://docs.google.com/spreadsheets/d/19WkLk17u0IIvu6-7Nd2CXdOU0R9HflParD_YVUU_wSY/edit#gid=0"
    base_datos = client.open_by_url(base_datos_url)
    hoja_base_datos = base_datos.sheet1

    # Get all the column names
    columnas = hoja_base_datos.row_values(1)
    
    # Find the person in the first column
    nombres = hoja_base_datos.col_values(1)
    print(f"Personas en la base de datos {nombres}")
    person_placement = {}
    for i in range(0, len(nombres)):
        if (nombres[i].lower() == search_name.lower()):
            print("Encontro el nombre")
            person_placement["nombre"] = nombres[i]
            person_placement["id"] = i + 1
    
    # Get the entire row of the person
    person_info_list = hoja_base_datos.row_values(person_placement['id'])
    # Put everything in a dictionary
    person_info = {}
    if (len(columnas) == len(person_info_list)):
        # If both lists have the same size then everything went well
        for k in range(0,len(columnas)):
            new_key = columnas[k].replace(" ","_").lower().replace("($)","dolares").replace("(q)","quetzales")
            person_info[new_key] = person_info_list[k]
    else:
        print("Error, check which column was fetched! The sizes don't match")
        return False
    # Optional (export to database file)
    if (export):
        filename_db = person_info["nombre_completo"].replace(" ","_")
        save_info_to_database(str(person_info).replace("'",'"'),f'info_empleado_{filename_db}.json')
    # Return the dictionary with all the data
    print(person_info)
    return person_info


# save as a json file
# save_info_to_database(str(data_to_replace_empleado).replace("'",'"'),'info_empleado_neww.json')
# Chatgpt libraries google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client pandas openpyxl

# Convertir este script en una funcion que retorne los datos para reemplazar (podría ser una lista)