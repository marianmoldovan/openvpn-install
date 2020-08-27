import csv
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


def send_email(client_name, email, key_name):
    msg = MIMEMultipart()
    msg['From'] = "Marian Moldovan <marian@cloudlink.pw>"
    msg['To'] = email
    msg['Subject'] = "Invitation VPN DearDoc"

    client_name = "Marian"
    body = f"""Hi {client_name},
    
You are invited to use the DearDoc's VPN. 
    
You can find attached a file called {key_name}.ovpn that contains everything you need to connect to the VPN. This is a private key that should be not shared with any other users.
    
First, you need to download a client for the VPN, here you have a couple of options:
    
    - Windows: The official OpenVPN community client
    https://openvpn.net/index.php/download/community-downloads.html.
    - macOS: Tunnelblick https://tunnelblick.net, Viscosity https://www.sparklabs.com/viscosity.
    - Android: OpenVPN for Android https://play.google.com/store/apps/details?id=3Dde.blinkt.openvpn.
    - iOS: The official OpenVPN Connect client https://itunes.apple.com/us/app/openvpn-connect/id590379981.
    
After installing the VPN client, you just have to drag and drop the {key_name}.ovpn file. 
    
If you have any issues, let me know, responding to this mail.
    
Kind regards,
Marian Moldovan"""

    msg.attach(MIMEText(body, 'plain'))

    filename = f"{key_name}.ovpn"
    attachment = open(f"/root/keys/{filename}", "rb")
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("user@gmail.com", "password")
    text = msg.as_string()
    s.sendmail("user@gmail.com", email, text)
    s.quit()

def create_openvpn_client(key_name):
    os.system(f"sudo ./add.sh {key_name}")


with open('users.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        client_name = row[1].split(",")[-1]
        email = row[2]
        key_name = email.split("@")[0]
        create_openvpn_client(key_name)
        send_email(client_name, email, key_name)

