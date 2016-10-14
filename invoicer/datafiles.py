import os
import fnmatch
import arrow
from collections import namedtuple

Location = namedtuple('Location', ['invoices', 'recurring', 'pending'])
location = Location('invoices', 'recurring', 'pending')

current_dir = os.path.abspath(".")


def read(recurring=False):


	invoice_files = []

	#   Manually created invoices
	file_list = os.listdir(os.path.join(current_dir, location.invoices))
	invoice_files.extend(fnmatch.filter(file_list, "*.yaml"))

	if recurring:
		invoice_files.extend(read_recurring())

	return invoice_files


def read_recurring():

	now = arrow.now('local')

	pattern = '{0}-*.yaml'.format(now.month)
	file_list = os.listdir(os.path.join(current_dir, location.recurring))
	return fnmatch.filter(file_list, pattern)

