import time
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import os, sys
# Take the main path of AutomatizacionOnboarding and use it as normal
sys.path.insert(1, "/".join(os.path.realpath(__file__).split("/")[0:-2]))

# To get the current date
from datetime import date

# Measure timing of the event
start_time = time.time()

# Global variables
current_date = date.today()

# Slack service API
client = WebClient(token=services.slack_token)

'''
Libraries
gspread
oauth2client
time
datetime
slack_sdk
os
sys
python-dotenv
'''
# Javier channel id U027NPX0PPZ
# Leo channel id U01K27N7MK4

# This file has the functions to monitor the weekly 
# This file asumes you run it on a monday and check the past week

def send_slack_message(message:str, users:list):
    # The message contains all the people with hours greater than 40.00
    for channel_id in users:
        try:
            client.chat_postMessage(channel=channel_id, text=message)
            print(f"Mensaje enviado a Slack con éxito al canal {channel_id}.")
        except SlackApiError as e:
            print(f"Error al enviar mensaje a Slack: {e.response['error']}")
    

# This takes the data from the individual monthly sheet
def monitor_week_monthly(monthly_link:str, hours:int=40, slack_users:list=[""]):
    print(slack_users)
    print("Monitoring week")
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(f"{os.getcwd()}/creds/create-monthly.json", scope)
    client = gspread.authorize(credentials)

   # Get the spreadsheet id automatically
    worksheet_id = monthly_link.split("/")
    for i in range(len(worksheet_id)):
        if worksheet_id[i] == 'd':
            worksheet_id = worksheet_id[i+1]
            break

    base_datos = client.open_by_url(monthly_link)
    individual_monthly = base_datos.sheet1

    print("Found and opened monthly")

    # First find the current date you are running this code in column B and grab the cell number
    execution_date = current_date.strftime('%d-%m-%Y')
    execution_date = '06-05-2024'
    column_values = individual_monthly.col_values(2)
    date_placement = {}
    for k in range(len(column_values)):
        if execution_date == column_values[k]:
            date_placement['row'] = k + 1
            date_placement['column'] = 'B'
            break
    # Now we know the row number of today's date
    print(date_placement)
    # Check if there is enough space to check
    # row 12 is the first row of the table, you cannot go further than that
    space_available = date_placement["row"] - 12
    if (space_available >= 7):
        print(f'There is enough space {space_available}')
        days_range = range(1,8)
        print(days_range)
    else:
        print(f'There is not enough space to check, you can check only the available days {space_available}')
        days_range = range(1,space_available + 1)
        print(days_range)
    # Check the work hours per day column of the previous 7 days
    total_week_hours = 0
    for days in days_range:
        checked_day = date_placement['row'] - days
        # Attempt to get the numeric value from the cell
        day_hours = individual_monthly.acell(f'F{checked_day}').numeric_value
        
        # Check if day_hours is None and handle accordingly
        if day_hours is None:
            print(f"No hours recorded for day row F{checked_day}. Assuming 0 hours.")
            day_hours = 0  # Treat missing data as 0 hours

        # Add the hours of that day to the total week hours register
        total_week_hours += day_hours
    # Display the total week hours
    print(f"Total week hours: {total_week_hours}")

    # Now display an alert when the hours are greater than 40
    if total_week_hours >= hours:
        print(f"Work hours this past week are greater than {hours}")
        # Send a slack message
        print(f"El numero de horas de XX es mayor a {hours}")



# This takes the data from the general hours control sheet
def monitor_week_optimized(monthly_link:str, hours:int|float=40.01, slack_users:list=[]):
    # Global variables
    total_week_hours = 0 #reset the count for each person
    rows_dictionary = {}
    date_placement = {}
    people_report = {}
    api_calls = 0
    slack_messages = "" #This array has all the slack messages that you need to send to Javier
    # Execution
    # print("Monitoring week")
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(f"{os.getcwd()}/creds/create-monthly.json", scope)
    client = gspread.authorize(credentials)

   # Get the spreadsheet id automatically
    worksheet_id = monthly_link.split("/")
    for i in range(len(worksheet_id)):
        if worksheet_id[i] == 'd':
            worksheet_id = worksheet_id[i+1]
            break

    base_datos = client.open_by_url(monthly_link)
    hours_worksheet = base_datos.sheet1
    api_calls += 1

    # print("Found and opened monthly")

    # Get the number of columns there are in the document
    column_names = hours_worksheet.row_values(1)
    column_count = len(column_names)
    api_calls += 1

    # First find the current date you are running this code in column B and grab the cell number
    execution_date = current_date.strftime('%d-%m-%Y')
    execution_date = '27-05-2024'
    column_values = hours_worksheet.col_values(1)
    for k in range(len(column_values)):
        if execution_date == column_values[k]:
            date_placement['row'] = k + 1
            date_placement['column'] = 'A'
            break
    api_calls += 1
    # Now we know the row number of today's date
    # print(date_placement)
    # Check if there is enough space to check
    # row 2 is the first row of the table, you cannot go further than that
    space_available = date_placement["row"] - 2
    if (space_available >= 7):
        # print(f'There is enough space {space_available}')
        days_range = range(1,8)
    else:
        # print(f'There is not enough space to check, you can check only the available days {space_available}')
        days_range = range(1,space_available + 1)
    # Get the complete row data for all days
    for days in days_range: # This loops through a maximum of 7 times
        # Maximum of 7 API Calls
        checked_day = date_placement['row'] - days
        rows_dictionary[checked_day] = hours_worksheet.row_values(checked_day)
        # You could put a delay here so that it gives you more time
        api_calls += 1

        row_size = len(rows_dictionary[checked_day])
        # Zero pad until all the arrays have the same length as the column number
        number_missing_values = column_count - row_size
        if (row_size == 1):
            # If the row size has only one element that means that the whole row in empty
            # to save time is better to skip this row later
            # print(f"This row is empty {rows_dictionary[checked_day]}")
            pass
        elif (number_missing_values > 1):
            # If the number of missing values is greater than 1
            # that means that the whole row needs to be checked to fetch the person who put weekends
            # print("This row is missing values, needs to zero pad")
            # add the missing values to complete the full size, can be between 1 and 89
            for it in range(number_missing_values):
                rows_dictionary[checked_day].append('')


    # print(rows_dictionary)
    # Cycle through all the names of the people column_count + 1
    for current_column in range(2, column_count + 1 ):
        nombre_persona = column_names[current_column - 1] # the name of the person
        total_week_hours = 0 #reset the count for each person
        # This loop cycles through each day of the week and gets the data
        for days in days_range:
            checked_day = date_placement['row'] - days
            # Get the value from the array previously stored to minimize API CALLS
            if (len(rows_dictionary[checked_day]) == column_count) and (rows_dictionary[checked_day][current_column - 1] != ''):
                day_hours = float(rows_dictionary[checked_day][current_column - 1])
            else:
                # print(f"La fecha {rows_dictionary[checked_day][0]} no tiene registros, continuando")
                continue
            
            # Check if day_hours is None and handle accordingly
            if day_hours is None:
                # print(f"No hours recorded for day row {checked_day}. Assuming 0 hours.")
                day_hours = 0  # Treat missing data as 0 hours

            # Add the hours of that day to the total week hours register
            total_week_hours += day_hours
        # Display the total week hours
        # print(f"Total week hours: {total_week_hours}")

        # Now display an alert when the hours are greater than 40
        if total_week_hours > hours:
            # Optimize the person name
            nombre_persona_op = nombre_persona.lower().replace(' ','_').replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u')
            # Add the people that display 40 or more hours this week
            people_report[nombre_persona_op] = total_week_hours
            # Send a slack message
            # print(f"El numero de horas de {nombre_persona} es {total_week_hours} para la semana pasada")
            slack_messages += f"El numero de horas de {nombre_persona} es {total_week_hours} para la semana pasada\n"
    send_slack_message(slack_messages,slack_users)
    people_report['api_calls'] = api_calls
    print(people_report)
    # Measure timing
    execution_time = time.time() - start_time
    print(f"Execution time {execution_time}")
    return execution_time

monitor_week_optimized(monthly_link = "https://docs.google.com/spreadsheets/d/1eFUWJ9G3GTjaDAbvZTGbDg3iOtiSpnWwX9l3ssfd2Ho/edit#gid=390949190", hours=40.0, slack_users=['U066NERJBD2'])



