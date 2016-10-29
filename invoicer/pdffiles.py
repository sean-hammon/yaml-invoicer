"""
Generate PDF file based on YAML Objects
"""

import os
import re

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Table, TableStyle

INCH = 72
MARGIN = INCH / 4
PAGE_WIDTH, PAGE_HEIGHT = letter


def generate_pdf(invoice):
    """
    Generate the PDF file

    :param invoice: the invoice data read from a YAML file
    """

    filename = (str(invoice["number"]) + "-" +
                re.sub(r'\W', '', invoice["client"]["company"]["name"]) +
                ".pdf")
    filename = os.path.join(".", "pending", filename)

    ttf_file = os.path.join(".", "Slabo27px-Regular.ttf")
    pdfmetrics.registerFont(TTFont("Slabo27", ttf_file))

    pdf = canvas.Canvas(filename, pagesize=letter)

    add_my_info(pdf)
    add_invoice_num(pdf, invoice["number"])
    add_client_info(pdf, invoice["client"])
    add_invoice_lines(pdf, invoice)

    pdf.showPage()
    pdf.save()


def add_invoice_num(pdf, invoice_number):
    """
    Add the invoice number to the PDF file.

    :param pdf: the canvas object
    :param invoice_number: the number of the invoice.
    :return:
    """

    pdf.setFont('Slabo27', 18)

    x = MARGIN
    y = PAGE_HEIGHT - MARGIN

    pdf.drawString(x, y, "Invoice: " + str(invoice_number))


def add_my_info(pdf):
    """
    Add address of the business creating the invoice to the PDF file.
    """

    #   Set the cursor to the top, middle of the page
    x = (PAGE_WIDTH / 2) + (PAGE_WIDTH / 4)
    y = PAGE_HEIGHT - MARGIN
    txt_object = pdf.beginText(x, y)
    txt_object.setFont('Slabo27', 11)

    txt_object.setLeading(16)
    txt_object.textLine("Remit to:")
    txt_object.setFont('Slabo27', 13)
    txt_object.setLeading(12)
    txt_object.textLine('Sean Hammon')
    txt_object.textLine('1121 Quarry View Way')
    txt_object.textLine('Sandy, UT 84094')
    txt_object.textLine('801-367-0038')

    pdf.drawText(txt_object)


def add_client_info(pdf, client):
    """
    Add client information to the PDF

    :param pdf: the canvas object
    :param client:
    :return:
    """
    x = MARGIN
    y = PAGE_HEIGHT - MARGIN - 24

    txt_object = pdf.beginText(x, y)
    txt_object.setFont('Slabo27', 14)
    txt_object.setLeading(14)

    contact = client['principle']['name']
    if 'billing_contact' in client:
        contact = client['billing_contact']['name']
    txt_object.textLine(contact)

    txt_object.textLine(client['company']['name'])
    txt_object.textLines(client['company']['address'])

    pdf.drawText(txt_object)


def add_invoice_lines(pdf, invoice):
    """
    Add the invoice line items to the PDF file

    :param pdf: The canvas object
    :param invoice: The invoice dictionary
    :return:
    """
    x = MARGIN
    y = MARGIN * 3

    column_widths = [INCH * .5, INCH * 5.7, INCH * .90, INCH * .90]
    table_data = [["Qty", "Description", "Price Each", "Total Price"]]
    subtotal = 0
    for row in invoice["lines"]:
        price = float(row["quantity"]) * float(row["price_each"])
        data_row = [
            row["quantity"],
            row["description"],
            '${0:.2f}'.format(row["price_each"]),
            '${0:.2f}'.format(price)
        ]
        subtotal += price
        table_data.append(data_row)

    total_lines = 28
    incoming_lines = len(invoice["lines"])
    blank_lines = total_lines - incoming_lines
    for i in range(0, blank_lines):
        table_data.append(['', '', '', ''])

    table_data.append(['', '', 'Subtotal:', '${0:.2f}'.format(subtotal)])
    tax = invoice["tax_rate"] * subtotal
    table_data.append(['', '', 'Tax:', '${0:.2f}'.format(tax)])
    total = subtotal + tax
    invoice["total"] = total
    table_data.append(['', '', 'Total:', '${0:.2f}'.format(total)])

    table = Table(table_data, column_widths)
    table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('ALIGN', (2, 0), (3, -1), 'RIGHT'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(0x555555)),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor(0xFFFFFF)),
        ('GRID', (0, 0), (-1, -4), 0.25, colors.HexColor(0x333333)),
        ('GRID', (-2, -3), (-1, -1), 0.25, colors.HexColor(0x333333))
    ]))
    table.wrapOn(pdf, x, y)
    table.drawOn(pdf, x, y)
