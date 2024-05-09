import os
import json
import sys
# Take the main path of AutomatizacionOnboarding and use it as normal
sys.path.insert(1, "/".join(os.path.realpath(__file__).split("/")[0:-2]))

import bot_paths

# save information to file
def save_info_to_database(text,file_name):
    print(f'saving info to file {file_name}')
    # path to the database folder
    database_path = f'{bot_paths.database_path}/{file_name}'
    # store the text in a file so the console is not saturated
    file = open(database_path, "w", encoding="utf-8")
    file.write(text)
    file.close()
    return True

# How to save a json object
# object = '''
# {
#     "id": 1
# }
# '''
#                       data string  object type (persona, empresa, sociedad)
# save_info_to_database(str(object),"database.json")

