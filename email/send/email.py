import smtplib, os, json
from email.message import EmailMessage

"""
    This function sends an email notification to the user after an image is edited.

    Args:
        message (str): The message containing information from the queue about the edited image.
"""
def notification(message):
    message = json.loads(message)

    edited_image_fid = message["edited_image_fid"]
    filter_type = message["filter_type"]
    receiver_address = message["username"]

    sender_address = os.environ.get("EMAIL_ADDRESS")
    sender_password = os.environ.get("EMAIL_PASSWORD")

    msg = EmailMessage()
    msg.set_content(f"Filter \"{filter_type}\" applied to uploaded file.\nDownload link: http://editimage.com/download?fid={edited_image_fid}")
    msg["Subject"] = "Download Edited Image"
    msg["From"] = sender_address
    msg["To"] = receiver_address

    session = smtplib.SMTP("smtp-mail.outlook.com", 587)
    session.starttls()
    session.login(sender_address, sender_password)
    session.send_message(msg, sender_address, receiver_address)
    session.quit()
    print("Mail Sent")