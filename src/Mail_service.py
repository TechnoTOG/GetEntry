#-------Code for "Mail Service" to be generated,modified and updated by @Devaah07-------
#-----------------Code to be then verified by @devkiraa and @TechnoTOG------------------

from flask import Flask, request, jsonify
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from email.mime.base import MIMEBase
from email import encoders

app = Flask(__name__)

# Email app settings
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = 'tenny.smart@gmail.com'
SENDER_PASSWORD = 'gfxfctjwwfzowocv'

def send_email(subject, to_email, message, attachment_path=None):
    try:
        # Set up the MIME object
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        # Attach the file, if specified
        if attachment_path:
            attachment = open(attachment_path, 'rb')
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(attachment_path)}"')
            msg.attach(part)

        # Connect to the SMTP server and send the email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print("Error:", e)
        return False

@app.route('/send_email', methods=['POST'])
def send_email_endpoint():
    data = request.json

    if not all(key in data for key in ['subject', 'to_email', 'message']):
        return jsonify({'error': 'Missing required fields'}), 400

    subject = data['subject']
    to_email = data['to_email']
    message = data['message']
    attachment_path = data.get('attachment_path')  # Get attachment path, if provided

    if send_email(subject, to_email, message, attachment_path):
        return jsonify({'message': 'Email sent successfully'})
    else:
        return jsonify({'error': 'Failed to send email'}), 500


if __name__ == '__main__':
    app.run(debug=True)