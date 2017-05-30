"""
Send the PDF file to the client
"""

from smtplib import SMTP_SSL
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText;
from email.mime.application import MIMEApplication


def send(smtp_config, invoice, pdf_path):

    msg = MIMEMultipart()
    msg['From'] = ''
    msg['To'] = ''
    msg['Subject'] = ''

    # The main body is just another attachment
    body = """
    Hi, {}.
    
    Here is your invoice for {}. The total amount is ${:.2f}.
    
    If you have any questions, let me know.
    
    -Sean
    """.format(
        client_name,
        invoice['title'],
        invoice['total']
    )

    mime_body = MIMEText(body)
    msg.attach(mime_body)

    # PDF attachment
    pdf_file = open(pdf_path,'rb')
    attachment = MIMEApplication(pdf_file.read(),_subtype="pdf")
    pdf_file.close()
    attachment.add_header('Content-Disposition','attachment',filename=filename)
    msg.attach(attachment)

    with SMTP_SSL(smtp_config['host'], smtp_config['port']) as smtp:
        smtp.ehlo()
        smtp.login(smtp_config['user'],smtp_config['password'])
        smtp.sendmail(msg['From'], [''], msg.as_string())
        smtp.quit()
