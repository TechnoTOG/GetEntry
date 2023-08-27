#Entire code to be verified and accepted by @devkiraa and @TechnoTOG

import os
import csv
import qrcode
import random
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

    # Path to the folder where you want to save the generated QR
    output_folder = "QRImages"

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Load data from CSV file
    csv_file_path = "input.csv"  # Replace with your CSV file path
    qr_data_list = []

    with open(csv_file_path, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip header row
        for row in csv_reader:
            qr_data_list.append(row[0])  # Assuming QR data is in the first column

    with tqdm(total=len(qr_data_list), desc="Generating QR Codes") as pbar:
        for qr_data in qr_data_list:
            qr_code_filename = os.path.join(output_folder, f"qr_{pbar.n + 1}.png")
            generate_qr_code(qr_data, qr_code_filename)
            pbar.update(1)

    print("QR code generation completed.")

#--------Code block for "Ticket generation" to be Generated,modified and updated by @niranjana_2004--------



#--------Code block for "Mailing Service" to be Generated,modified and updated by @Devaah07--------
