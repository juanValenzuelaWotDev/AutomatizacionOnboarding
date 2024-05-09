# Import libraries
from docx import Document
from docx2pdf import convert
import os
import sys
# Take the main path of AutomatizacionOnboarding and use it as normal
sys.path.insert(1, "/".join(os.path.realpath(__file__).split("/")[0:-2]))

import bot_paths

# turn numbers to words for contract fill
from num2words import num2words



# import the bot that downloads the contract
# from download_contract import download_contract, clean_dir, picture_path



# Functions that turns integrers into words
# https://es.stackoverflow.com/questions/584184/convertir-n%C3%BAmeros-a-palabras-con-python    
def simplify_num(num: str):
    """
    This function divides the number in chunks of 3 digits
    These chunks are much easier to process and assign the correct word
    """
    cui_number = num[:]
    
    # first erase the spaces between numbers
    if " " in cui_number:
        return cui_number.split(" ")

    # next split the numbers into three standard chunks
    return [cui_number[0:4], cui_number[4:9], cui_number[9:14]]

def num_to_words(number:str):
    num_list = simplify_num(number)
    num_buffer = []
    word_buffer = []
    for item in num_list:
        if item[0] == '0':
            num_buffer.append(int(item[0]))
            num_buffer.append(int(item[1:]))
            word_buffer.append(num2words(int(item[0]), lang='es'))
            word_buffer.append(num2words(int(item[1:]),lang='es'))
        else:
            num_buffer.append(int(item))
            word_buffer.append(num2words(int(item),lang='es'))    
    # print(num_buffer)
    # print(word_buffer)    
    # Return a single string containing all the numbers in word form
    return ', '.join(word_buffer)


# Test data, this data will come from a data base
# Data to replace
data_to_replace = {
    'arrendante' : 'NOMBRE_ARRENDANTE',
    'letras_arrendante' : 'DPI_ARRENDANTE_LETRAS',
    'dpi_arrendante': 'DPI_ARRENDANTE_NUMERO',
    'profesion_arrendante': 'PROFESION_ARRENDANTE',
    'arrendatario': 'NOMBRE_ARRENDATARIO',
    'letras_arrendatario' : 'DPI_ARRENDATARIO_LETRAS',
    'dpi_arrendatario' : 'DPI_ARRENDATARIO_NUMERO',
    'profesion_arrendatario': 'PROFESION_ARRENDATARIO',
    'fecha_actual': 'FECHA_CONTRATO',
    'fecha_inicio': 'FECHA_INICIO',
    'fecha_fin': 'FECHA_FIN'
}

# Data that gets replaced 'dos mil quinientos veintisiete, treinta y nueve mil novecientos sesenta y cinco, cero ciento uno'
replaced_data = {
    'arrendante' : 'JUAN PABLO ISAAC VALENZUELA SARAVIA',
    'letras_arrendante' : num_to_words('3049 08509 0116'),
    'dpi_arrendante': '3049 08509 0116',
    'profesion_arrendante': 'Doctor en Informática',
    'arrendatario': 'LEONARDO AUGUSTO ROSALES ARREAGA',
    'letras_arrendatario' : num_to_words('2423 67984 0101'),
    'dpi_arrendatario' : '2423 67984 0101',
    'profesion_arrendatario': 'Empresario',
    'fecha_actual': '30 de enero de 2024',
    'fecha_inicio': '1 de marzo de 2024',
    'fecha_fin': '1 de noviembre de 2024'
}

# ----------------------------------------------------------------------------------------------------
# Ejemplo de datos de WOT
data_to_replace_empleado = {
    'nombre_empleado' : 'NOMBRE_EMPLEADO',
    'anio': 'FECHA_ANIO',
    'mes': 'FECHA_MES',
    'dia': 'FECHA_DIA',
    'puesto': 'PUESTO_EMPLEADO',
    'cliente': 'CLIENTE_PROYECTO',
    'dia_inicio': 'DIA_INICIO',
    'mes_inicio': 'MES_INICIO',
    'anio_inicio': 'ANIO_INICIO',
    'duracion_puesto': 'DURACION_PUESTO',
    'pago_texto_hora': 'PAGO_TEXTO_HORA',
    'pago_hora': 'PAGO_NUMERO_HORA',
    'pago_texto_mes': 'PAGO_TEXTO_MES',
    'pago_mes': 'PAGO_NUMERO_MES',
    'pago_texto_mes_quetzales': 'PAGO_TEXTO_MES_QUETZALES',
    'pago_mes_quetzales': 'PAGO_NUMERO_MES_QUETZALES',
    'modalidad': 'MODALIDAD_TRABAJO',
}

replaced_data_empleado = {
    'nombre_empleado' : 'JUAN PABLO VALENZUELA',
    'anio': '2024',
    'mes': 'mayo',
    'dia': '8',
    'puesto': 'PUESTO_EMPLEADO',
    'cliente': 'CLIENTE_PROYECTO',
    'dia_inicio': 'DIA_INICIO',
    'mes_inicio': 'MES_INICIO',
    'anio_inicio': 'ANIO_INICIO',
    'duracion_puesto': 'DURACION_PUESTO',
    'pago_texto_hora': 'PAGO_TEXTO_HORA',
    'pago_hora': 'PAGO_NUMERO_HORA',
    'pago_texto_mes': 'PAGO_TEXTO_MES',
    'pago_mes': 'PAGO_NUMERO_MES',
    'pago_texto_mes_quetzales': 'PAGO_TEXTO_MES_QUETZALES',
    'pago_mes_quetzales': 'PAGO_NUMERO_MES_QUETZALES',
    'modalidad': 'MODALIDAD_TRABAJO',
}


# This function replaces one word
def replace_one_word(file_path, search_word, replace_word):
    """
    This function replaces one word in a document
    file path is the path where it looks for the template
    search word is the word that this looks for
    replace word is the word that this puts in place of the search word
    """

    # # Open an existing document
    print("opening document...")
    doc = Document(f'.../downloads/{file_path}')

    for paragraph in doc.paragraphs:
        if search_word in paragraph.text:
            # this stores the format of the text
            inline = paragraph.runs
            for i in range(len(inline)):
                if search_word in inline[i].text:
                    text= inline[i].text.replace(search_word, replace_word)
                    inline[i].text = text


    # # Save the modified document
    print("saving document...")
    doc.save('modified_document.docx')
    print("saved!")
    # in here just delete the input file so it doesn't duplicate the next run

# works for multiple words in one document
def fill_contract(file_path, search_data:dict, replace_data:dict, type:str="wot"):
    """
    This function replaces multiple keywords in a document 
    file path is the path where it looks for the template
    search word is the word that this looks for
    replace word is the word that this puts in place of the search word
    """
    # Download contract
    if type.lower()=="wot":
        # download_contract()
        print("descargando archivo de wot")
    elif type.lower()=="bot":
        print("descargando archivo de bot")
    else:
        print("tipo de contrato no valido")
    # # Open an existing document
    print("opening document...")
    doc = Document(f'{bot_paths.download_path}/{file_path}')
    for k in search_data:
        search_word = search_data[k]
        replace_word = replace_data[k]
        print(f"Key: {k}")
        print(f"Look for: {search_word}")
        print(f"Replace with: {replace_word}")
        for paragraph in doc.paragraphs:
            if search_word in paragraph.text:
                # this stores the format of the text
                inline = paragraph.runs
                for i in range(len(inline)):
                    if search_word in inline[i].text:
                        text= inline[i].text.replace(search_word, replace_word)
                        inline[i].text = text
                        print('replaced')


    # # Save the modified document
    print("saving document...")
    temporary_name = r"{}\modified_document.docx".format(bot_paths.modified_document_path)
    doc.save(temporary_name)
    convert(temporary_name, r'{}\{}.pdf'.format(bot_paths.modified_document_path, file_path))
    # Delete the temporary docx file
    if (os.path.exists(temporary_name)):
        os.remove(temporary_name)
        # clean_dir(picture_path) #clean the download directory to avoid errors
    print("saved!")
    # in here just delete the input file so it doesn't duplicate the next run


# Tests
# persona-persona
# Get document path
# document_path = "CONTRATO_ARRENDAMIENTO_OFICINA.docx"
# word = data_to_replace['arrendante']
# replace_word = replaced_data['arrendante']
# fill_contract(document_path, data_to_replace, replaced_data)

# empresa-empresa
document_name = "Oportunidad Facturación Servicios Profesionales [Template].docx"
fill_contract(document_name,data_to_replace_empleado,replaced_data_empleado,"wot")
