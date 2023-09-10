import mysql.connector
import glob
import os
import csv

db_config = {
    'host': 'localhost',
    'user': 'scott',
    'password': 'tiger123',
    'database': 'sprint'
}


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

    # Connect to the MySQL database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    with open(csv_file_path, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip header row
        for row in csv_reader:
            qr_data_list.append(row[0])  # Assuming QR data is in the first column

     # Insert data into the database
        for row in csv_reader:
            cursor.execute("INSERT INTO qr_codes (qr_id,roll_no,name,batch,event) VALUES (%s, %s, %s,%s,%s)", row)

    # Commit changes and close the connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()