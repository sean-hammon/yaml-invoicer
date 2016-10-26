"""
Generate PDF file based on YAML Objects
"""

import os
import re

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

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
