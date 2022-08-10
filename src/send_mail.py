import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from pathlib import Path
from docxtpl import DocxTemplate
import jinja2
import os


def increase(value):
    return value + 1


jinja_env = jinja2.Environment()
jinja_env.filters["increase"] = increase
jinja2.filters.FILTERS["increase"] = increase


def create_report(context):
    document = DocxTemplate("template.docx")
    document.render(context, jinja_env)
    file_name = f"{context['yibf']}_test_cekici_tutanak.docx"
    document.save(file_name)

    return file_name


def send_mail(template_context):
    try:
        yibf = template_context["yibf"]
        bore_axises = template_context["bore_axises"]
        building_element = template_context["building_element"]
        mail_content = f"""
            Yibf No : {yibf}
            Karot Alınan Elemanlar : {', '.join(bore_axises)}
        """
        # The mail addresses and password
        sender_address = "fkerandevu@gmail.com"
        sender_pass = "chxuoodzhrjporkh"
        receiver_address = "fkebetontest@gmail.com"
        # Setup the MIME
        message = MIMEMultipart()
        message["From"] = sender_address
        message["To"] = receiver_address
        message[
            "Subject"
        ] = f"{yibf} Yibf No'lu Yapının {building_element} Test Çekici Tutanağı."  # The subject line
        # The body and the attachments for the mail
        message.attach(MIMEText(mail_content, "plain"))
        part = MIMEBase("application", "octet-stream")
        path = create_report(template_context)
        with open(path, "rb") as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition", "attachment; filename={}".format(Path(path).name)
        )
        message.attach(part)
        # Create SMTP session for sending the mail
        session = smtplib.SMTP("smtp.gmail.com", 587)  # use gmail with port
        session.starttls()  # enable security
        session.login(sender_address, sender_pass)  # login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        os.remove(path)
        return True, ""
    except Exception as e:
        print(e)
        return False, e
