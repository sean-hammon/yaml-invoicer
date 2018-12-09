"""
Main program file
"""

import io
import sys

import ruamel.yaml

import datafiles
import pdffiles
import mailer
import arrow


def main():
    with io.open("./config.yaml", 'r') as fh:
        config = ruamel.yaml.load(fh.read(), Loader=ruamel.yaml.Loader)

    today = arrow.now('US/Mountain').day
    include_recurring = today == 1

    print("\ntoday: {}, include recurring: {}", today, include_recurring)
    invoices = datafiles.read(include_recurring)
    for invoice in invoices:
        print("Processing invoice {} for {}".format(config['next_invoice'], invoice['client']['company']['name']))
        invoice["number"] = config['next_invoice']
        pdf_path = pdffiles.generate_pdf(invoice)
        mailer.send(config["smtp"], invoice, pdf_path)
        config['next_invoice'] += 1

    yaml_out = ruamel.yaml.dump(config, Dumper=ruamel.yaml.RoundTripDumper)
    with io.open("./config.yaml", "w") as fh:
        fh.write(yaml_out)


if __name__ == "__main__":
    main()
