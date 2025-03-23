import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL_ADDRESS = "your_email@gmail.com"
EMAIL_PASSWORD = "your_password"

def send_email(to_email, agency_name, decision):
    subject = f"{agency_name} - Agency Signup {decision}"
    body = f"Dear {agency_name},\n\nWe have {decision.lower()} your signup request.\n\nBest,\nMozilor Team"

    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())

# Example usage:
if __name__ == "__main__":
    send_email("agency@example.com", "Digital Silk", "Approved")
