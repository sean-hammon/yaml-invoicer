"""
Main program file
"""

import io

import ruamel.yaml

import cli
import datafiles
import pdffiles
import mailer
import arrow


def main():

    config_file = "./config.yaml"
    if cli.args.testmode:
        config_file = "./config-test.yaml"

    with io.open(config_file, 'r') as fh:
        config = ruamel.yaml.load(fh.read(), Loader=ruamel.yaml.Loader)

    today = arrow.now('US/Mountain').day
    include_recurring = today == 1

    print("\ntoday: {}, include recurring: {}".format(today, include_recurring))
    invoices = datafiles.read(include_recurring)
    for invoice in invoices:
        print("Processing invoice {} for {}".format(config['next_invoice'], invoice['client']['company']['name']))
        invoice["number"] = config['next_invoice']
        pdf_path = pdffiles.generate_pdf(invoice)
        mailer.send(config["smtp"], invoice, pdf_path)
        config['next_invoice'] += 1

    yaml_out = ruamel.yaml.dump(config, Dumper=ruamel.yaml.RoundTripDumper)
    with io.open(config_file, "w") as fh:
        fh.write(yaml_out)


if __name__ == "__main__":
    main()
