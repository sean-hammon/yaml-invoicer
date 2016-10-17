"""
Reads YAML files from disk and turns them into YAML objects
"""

import fnmatch
import os
from collections import namedtuple

import arrow
import ruamel.yaml

Location = namedtuple('Location', ['invoices', 'recurring', 'pending', 'clients'])
LOCATION = Location('invoices', 'recurring', 'pending', 'clients')

CURRENT_DIR = os.path.abspath(".")


def read(recurring=False):
    """
    Read YAML files from disk and parse them into YAML objects

    :param recurring: boolean - include recurring invoices
    :return list of parsed yaml objects
    """

    invoice_files = []

    #   Manually created invoices
    file_list = os.listdir(os.path.join(CURRENT_DIR, LOCATION.invoices))
    file_names = fnmatch.filter(file_list, "*.yaml")
    for file in file_names:
        invoice_files.append(os.path.join(CURRENT_DIR, LOCATION.invoices, file))

    if recurring:
        invoice_files.extend(read_recurring())

    invoices = []
    for file in invoice_files:
        with open(file) as inv_file:
            inv = import_yaml(inv_file)
            invoices.append(inv)

    return invoices


def read_recurring():
    """
    Get the file names of recurring invoices due this month

    :return list of file names
    """

    now = arrow.now('local')

    pattern = '{0}-*.yaml'.format(now.month)
    file_list = os.listdir(os.path.join(CURRENT_DIR, LOCATION.recurring))
    file_names = fnmatch.filter(file_list, pattern)

    invoice_files = []
    for file in file_names:
        invoice_files.append(os.path.join(CURRENT_DIR, LOCATION.recurring, file))

    return invoice_files


def import_yaml(file_handle):
    """
    Read in the YAML files and read data from file referenced by invoices

    :param file_handle: a file handle returned from open()
    :return a dictionary with invoice data
    """

    inv = ruamel.yaml.load(file_handle.read())

    client_yaml = os.path.join(CURRENT_DIR, LOCATION.clients, inv['client'] + ".yaml")
    with open(client_yaml) as client:
        inv['client'] = ruamel.yaml.load(client.read())

    return inv
    