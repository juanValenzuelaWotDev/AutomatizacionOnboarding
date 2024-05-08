import tkinter as tk
import os, re
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfile

from tasks import execute_email

# global variables
email_body = ""
email_subject = ""
sender_email = ""
password = ""
email_list = []


# Application object
root = tk.Tk()
# Set the window size
# canvas = tk.Canvas(root, width=600, height=400)
# canvas.grid(columnspan=3)

# Logo
# logo = Image.open("logo-wot/logo.png")
# logo = ImageTk.PhotoImage(logo)
# logo_label = tk.Label(image=logo)
# logo_label.grid(column=1, row=0)

# Envio de correos automatizados
# Ingresa tu contraseña y tu correo para iniciar sesion
# Ingresa el texto para enviar a la lista de correos
# Ingresa la lista de correos para escribirles

# instructions
instructions = tk.Label(root, text='Instructions', font='Raleway')
instructions.grid(columnspan=3, column=0, row=0, padx=200, pady=10)

# Function to open a file
def open_file():
    excel_input.set("Loading...")
    file = askopenfile(parent=root, mode='rb', title="Choose a file", filetypes=[("Excel type file", "*.xls, *.xlsx, *.csv")])
    if (file):
        excel_input.set("Load emails")
        # open the file with pandas
        # extract emails and store them in a variable (can be a list)
    else:
        excel_input.set("Load emails")

# Function to send emails
def send_emails():
    print("Sending emails")

# Execute automation
def automate():
    # Get the path
    extraccionRTU = os.path.abspath(os.path.join("..", "Extraccion%20RTU"))
    print("ExtractorDatosRTU directory is", extraccionRTU)

    os.chdir(extraccionRTU)
    task = re.sub(r"[\n\t\s]*", "", str(task))
    # log the task
    os.system(f'.\\rcc.exe run "{task}" stag --space second --silent')

def automatic_email():
    execute_email()

# Add a button that loads an excel spreadsheet
excel_input = tk.StringVar()
excel_btn = tk.Button(root, textvariable=excel_input, command=lambda:open_file(), font='Raleway', bg='white', fg='#20bebe', height=2, width=15)
excel_input.set('Load emails')
excel_btn.grid(column=2, row=1)

# Add a button to send emails
send_email_text = tk.StringVar()
send_email_btn = tk.Button(root, textvariable=send_email_text, command=lambda:automatic_email(), font='Raleway', bg='white', fg='black', height=2, width=15)
send_email_text.set('Send email')
send_email_btn.grid(column=2, row=4)

# Add an input box to write sender email
sender_email_inputbox_text = tk.Entry()
sender_email_label = tk.Label(text='Your email')
sender_email_label.grid(column=0, row=1)
sender_email_inputbox_text.grid(column=0, row=2)

# Add an input box to write your password to sign in
password_inputbox_text = tk.Entry()
password_label = tk.Label(text='Your password')
password_label.grid(column=0, row=3)
password_inputbox_text.grid(column=0, row=4)

# Add an input box to write the email subject
email_subject_inputbox_text = tk.Entry(width=60)
email_subject_inputbox_label = tk.Label(text='Write the email subject')
email_subject_inputbox_label.grid(column=1, row=5, pady=10)
email_subject_inputbox_text.grid(column=0, row=6, columnspan=3)

# Add an input box to write the email body
email_body_inputbox_text = tk.Text(height=4, width=45)
email_body_label = tk.Label(text='Write your email body')
email_body_label.grid(column=1, row=7, pady=5)
email_body_inputbox_text.grid(column=0, row=8, columnspan=3, pady=5)

# Add a progress bar

# Run the application
root.mainloop()

# To do
# Turn this into a class based app
# Call the bot/function when clicking the send email button
# Export the app to a .exe portable file https://www.youtube.com/watch?v=QWqxRchawZY