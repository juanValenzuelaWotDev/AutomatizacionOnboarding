from oauth2client.service_account import ServiceAccountCredentials
import gspread
from gspread_formatting import CellFormat, Color, format_cell_range
import os, sys
import pandas as pd
# Take the main path of AutomatizacionOnboarding and use it as normal
sys.path.insert(1, "/".join(os.path.realpath(__file__).split("/")[0:-2]))

import bot_paths
from fill_word_document.database import save_info_to_database
from num2words import num2words


def fill_quickplay_checklist(values:dict):
    print("starting worksheet")
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(f"{os.getcwd()}/creds/create-monthly.json", scope)
    client = gspread.authorize(credentials)

    quickplay_sheet = "https://docs.google.com/spreadsheets/d/1_sipxFWV2jrthFp9Mq-eueiID_qXdCw49m4DGnuhdj4/edit#gid=0"
    spreadsheet_id = "1_sipxFWV2jrthFp9Mq-eueiID_qXdCw49m4DGnuhdj4"
    base_datos = client.open_by_url(quickplay_sheet)
    hoja_quickplay = base_datos.sheet1

    print("opened worksheet")

    # Duplicate the first sheet
    edit_quickplay = hoja_quickplay.duplicate(new_sheet_name="Quickplay checklist copy")
    quickplay_id = edit_quickplay.id
    # Change to the second sheet
    # using edit_quickplay because it is the new sheet
    # Edit the copy
    edit_quickplay.update_acell("B2",values.get("name"))
    edit_quickplay.update_acell("B3",values.get("last_name"))
    edit_quickplay.update_acell("B4",values.get("email"))
    edit_quickplay.update_acell("B5",values.get("birthdate"))
    edit_quickplay.update_acell("B6",values.get("address"))
    edit_quickplay.update_acell("B7",values.get("phone"))

    edit_quickplay.update_acell("B18",values.get("start_date"))
    # Download the copy
    # At the end it is much simpler to put the worksheet into a dataframe and export it locally
    dataframe = pd.DataFrame(edit_quickplay.get_all_records())
    # Export the data into a local file
    full_name = f'{values.get("name")} {values.get("last_name")}'.replace(" ","_")
    save_path = r"{}\quickplay_checklist_{}.xlsx".format(bot_paths.download_path, full_name)
    dataframe.to_excel(save_path, index=False)
    
    # Delete the duplicated sheet and leave only the original
    print("Deleting copy")
    base_datos.del_worksheet_by_id(quickplay_id)


    print(f"Document generated in \n {bot_paths.download_path}")

    # Todas las columnas de esta tabla
    columnas = hoja_quickplay.row_values(1)
    


