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
    pdf.setFont('Slabo27', 13)

    add_my_info(pdf)

    pdf.showPage()
    pdf.save()


def add_my_info(pdf):
    """
    Add address of the business creating the invoice to the PDF file.
    """

    #   Set the cursor to the top, middle of the page
    x = (PAGE_WIDTH / 2) + (PAGE_WIDTH / 4)
    y = PAGE_HEIGHT - MARGIN
    txt_object = pdf.beginText(x, y)
    txt_object.textLines("""
    Sean Hammon
    1121 Quarry View Way
    Sandy, UT 84094
    801-367-0038
    """)
    pdf.drawText(txt_object)
