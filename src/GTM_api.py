#Entire code to be verified and accepted by @devkiraa, @TechnoTOG and 

import os
import csv
import qrcode
import random
import glob
import subprocess
import string
from tqdm import tqdm
from PIL import Image
from flask import Flask, request, jsonify
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from email.mime.base import MIMEBase
from email import encoders
import requests

#--------Code block for "QR generation" to be Generated,modified and updated by @GowriParvathyy--------

def generate_qr_code(data, filename):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2,
    )
    qr.add_data(data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_img.save(filename)

#--------Code block for "Ticket generation" to be Generated,modified and updated by @niranjana_2004--------

def tgen():
    qr_images_folder = "QRImages"
    ticket_output_folder = "Ticket"
    ticket_design_path = "custom_ticket.png"

    if not os.path.exists(ticket_output_folder):
        os.makedirs(ticket_output_folder)

    ticket_design = Image.open(ticket_design_path)

    # Ticket size
    ticket_width = ticket_design.width
    ticket_height = ticket_design.height

    # Calculate the size of the QR code based on the specified height
    qr_size = (ticket_height // 2)-2

    # Get a list of all QR code image files in the QRImages folder
    qr_code_files = sorted(file for file in os.listdir(qr_images_folder) if file.endswith(".png"))

    with tqdm(total=len(qr_code_files), desc="Generating Tickets") as pbar:
        # Loop through each QR code image
        for qr_file in qr_code_files:
            # Construct the path to the QR code image
            qr_code_path = os.path.join(qr_images_folder, qr_file)

            # Load and resize the QR code
            qr_code = Image.open(qr_code_path)
            qr_code = qr_code.resize((qr_size, qr_size))

            # Calculate the position to place the QR code at the bottom right
            x = ticket_width - qr_size-80
            y = ticket_height - qr_size-160

            # Create a copy of the ticket design to avoid modifying the original
            ticket_with_qr = ticket_design.copy()

            # Paste the QR code onto the ticket copy
            ticket_with_qr.paste(qr_code, (x, y))

            # Construct the output path for the generated ticket
            ticket_name = os.path.splitext(qr_file)[0] + "_ticket.png"
            output_path = os.path.join(ticket_output_folder, ticket_name)

            # Save the generated ticket image with QR code
            ticket_with_qr.save(output_path)
            pbar.update(1)

    print("Tickets generated and saved in the 'Ticket' folder.")
    send_mail()

#--------Code block for "Mailing Service" to be Generated,modified and updated by @Devaah07--------
def send_mail():
    try:
        auto_mailer = "src\Mail_service.py"
        auto_mail_process = subprocess.Popen(['python', auto_mailer])
    except:
        print("Unable to start Mail Service!!")
    url = 'http://localhost:5000/send_email'

    data = {
        "subject": "Test Email",
        "to_email": "youaedrin@gmail.com",
        "message": "This is a test email sent from the API.",
        "attachment_path": "F:\TicketWave\TicketWave\Ticket\qr_1_ticket.png"
    }

    response = requests.post(url, json=data)

    if response.status_code == 200:
        auto_mail_process.terminate()
        print("Email sent successfully")
    else:
        auto_mail_process.terminate()
        print("Failed to send email")
        print("Response:", response.text)

#Main function to be updated by @GowriParvathyy, @Niranjana_2004 and @Devaah07

def main():
    # Path to the folder where you want to save the generated QR
    qr_output_folder = "QRImages"

    if not os.path.exists(qr_output_folder):
        os.makedirs(qr_output_folder)

    # Find all CSV files in the current directory
    csv_files = glob.glob("*.csv")

    if len(csv_files) == 0:
        print("No CSV files found in the current directory.")
        exit()

    # Assuming there is only one CSV file, you can take the first one
    csv_file_path = csv_files[0]

    qr_data_list = []

    with open(csv_file_path, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip header row
        for row in csv_reader:
            qr_data_list.append(row[0])  # Assuming QR data is in the first column

    with tqdm(total=len(qr_data_list), desc="Generating QR Codes") as pbar:
        for qr_data in qr_data_list:
            qr_code_filename = os.path.join(qr_output_folder, f"qr_{pbar.n + 1}.png")
            generate_qr_code(qr_data, qr_code_filename)
            pbar.update(1)

    print("QR code generation completed.")
    tgen()
    print("hello")

if __name__ == "__main__":
    main()