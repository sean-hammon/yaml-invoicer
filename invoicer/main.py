"""
Main program file
"""

import io
import sys

import ruamel.yaml

import datafiles
import pdffiles
import mailer


def main(include_recurring):
    with io.open("./config.yaml", 'r') as fh:
        config = ruamel.yaml.load(fh.read(), Loader=ruamel.yaml.Loader)

    invoices = datafiles.read(include_recurring)
    for invoice in invoices:
        print("Processing invoice {} for {}".format(config['next_invoice'], invoice['client']['company']['name']))
        invoice["number"] = config['next_invoice']
        pdf_path = pdffiles.generate_pdf(invoice)
        mailer.send(invoice, pdf_path)
        config['next_invoice'] += 1

    yaml_out = ruamel.yaml.dump(config, Dumper=ruamel.yaml.RoundTripDumper)
    with io.open("./config.yaml", "w") as fh:
        fh.write(yaml_out)


if __name__ == "__main__":
    include_recurring = '--recurring' in sys.argv
    main(include_recurring)
