"""
Send the PDF file to the client
"""

from os.path import basename
from smtplib import SMTP_SSL
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText;
from email.mime.application import MIMEApplication

import cli


def send(smtp_config, invoice, pdf_path):

    recipients = {
        "to": ['{} <{}>'.format(
            invoice['client']['principle']['name'],
            invoice['client']['principle']['email']
        )],
        "cc": ['{} <{}>'.format(
            smtp_config['from']['name'],
            smtp_config['from']['email']
        )]
    }
    send_to = [
        invoice['client']['principle']['email'],
        smtp_config['from']['email']
    ]

    if 'billing_contact' in invoice['client']:
        recipients['to'].append("{} <{}>".format(
            invoice['client']['billing_contact']['name'],
            invoice['client']['billing_contact']['email']
        ))
        send_to.append(invoice['client']['billing_contact']['email'])

    msg = MIMEMultipart()
    msg['From'] = '{} <{}>'.format(
        smtp_config['from']['name'],
        smtp_config['from']['email']
    )
    msg['Cc'] = ", ".join(recipients['cc'])
    msg['To'] = ", ".join(recipients['to'])
    msg['Subject'] = 'Invoice for {} -- {}'.format(
        invoice["client"]["company"]["name"],
        invoice["title"]
    )

    client_name = invoice['client']['principle']['name'].split(' ').pop(0)
    if 'billing_contact' in invoice['client']:
        client_name = invoice['client']['billing_contact']['name'].split(' ').pop(0)


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
    pdf_file = open(pdf_path, 'rb')
    attachment = MIMEApplication(pdf_file.read(), _subtype="pdf")
    pdf_file.close()
    filename = basename(pdf_path)
    attachment.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(attachment)

    if not cli.args.nomail:
        with SMTP_SSL(smtp_config['host'], smtp_config['port']) as smtp:
            smtp.ehlo()
            smtp.login(smtp_config['user'],smtp_config['password'])
            smtp.sendmail(smtp_config['from']['email'], send_to, msg.as_string())
            smtp.quit()
