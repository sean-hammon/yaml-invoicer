"""
Main program file
"""

import io
import sys

import datafiles
import pdffiles


def main(include_recurring):
    with io.open("./invoice_num.txt", 'r') as fh:
        next_invoice_num = int(fh.read())

    invoices = datafiles.read(include_recurring)
    for invoice in invoices:
        print("Processing invoice {} for {}".format(config['next_invoice'], invoice['client']['company']['name']))
        invoice["number"] = next_invoice_num
        pdffiles.generate_pdf(invoice)
        next_invoice_num += 1

    with io.open("./invoice_num.txt", "w") as fh:
        fh.write(str(next_invoice_num))


if __name__ == "__main__":
    include_recurring = '--recurring' in sys.argv
    main(include_recurring)
