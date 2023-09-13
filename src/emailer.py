import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def read_config(file_path="../config.txt"):
    """
    Read email and password from the configuration file.

    Args:
    - file_path (str): Path to the configuration file.

    Returns:
    - tuple: (email, password)
    """
    with open(file_path, 'r') as f:
        lines = f.readlines()
        email = lines[0].split('=')[1].strip()
        password = lines[1].split('=')[1].strip()
    return email, password

def send_email(subject, body, to_email, csv_file_path=None):
    """
    Send an email with optional CSV attachment.

    Args:
    - subject (str): Email subject.
    - body (str): Email body content.
    - to_email (str): Recipient email address.
    - csv_file_path (str, optional): Path to the CSV file to attach. Defaults to None.

    Returns:
    - bool: True if email sent successfully, False otherwise.
    """
    from_email, password = read_config()

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Attach CSV file if provided
    if csv_file_path:
        with open(csv_file_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename= {csv_file_path}")
            msg.attach(part)

    # Send email
    try:
        server = smtplib.SMTP('smtp.example.com', 587)  # Replace with your SMTP server and port
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False