"""
Email client for sending horror movie reviews with an optional poster image.

Sends both:
- Plain text and HTML body
- Inline image and file attachment (poster)
"""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

class EmailClient:
    def __init__(self, email_address, email_password):
        self.email_address = email_address
        self.email_password = email_password

    def send(self, subject, body, recipient, image_path=None):
        msg = MIMEMultipart('related')
        msg['From'] = self.email_address
        msg['To'] = recipient
        msg['Subject'] = subject

        alt = MIMEMultipart('alternative')
        msg.attach(alt)

        alt.attach(MIMEText(body, 'plain'))

        html_body = f"<html><body><p>{body.replace(chr(10), '<br>')}</p>"
        if image_path:
            html_body += '<img src="cid:image1"><br>'
        html_body += "</body></html>"

        alt.attach(MIMEText(html_body, 'html'))

        if image_path and os.path.exists(image_path):
            with open(image_path, 'rb') as img_file:
                img_data = img_file.read()
                img = MIMEImage(img_data)
                img.add_header('Content-ID', '<image1>')
                img.add_header('Content-Disposition', 'inline', filename=os.path.basename(image_path))
                msg.attach(img)

        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login(self.email_address, self.email_password)
            smtp.send_message(msg)

        print(f"📧 Email sent to {recipient}")
