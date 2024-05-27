# This file is used to acces the paths in an easier way
import os

# https://sentry.io/answers/import-files-from-a-different-folder-in-python/
# These are all the paths for easy access
download_path = r"{}\downloads".format(os.getcwd())
modified_document_path = r"{}\modified_documents".format(os.getcwd())
database_path = r"{}\database".format(os.getcwd())
creds_path = r"{}\creds".format(os.getcwd())
# Secondary paths
fill_word_document_path = r"{}\fill_word_document".format(os.getcwd())
monthly_path = r"{}\monthly".format(os.getcwd())
workmail_path = r"{}\workmail".format(os.getcwd())
slack_path = r"{}\slack".format(os.getcwd())


# Put here the functions that check if the folders exist and create them if not

def check_path(path):
    print(f"Checking {path}")
    if not(os.path.exists(path)):
        print("Path not found, creating path...")
        os.mkdir(path)
        print("Path created")
    else:
        print("Path found")

# Call this at the start of the main task
def check_paths():
    print("Verifying all app paths")
    check_path(download_path)
    check_path(modified_document_path)
    check_path(database_path)
    check_path(creds_path)
    # Add something to check if the creds files are in place

# Just for testing
# check_paths()