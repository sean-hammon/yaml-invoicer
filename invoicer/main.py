import sys
import pprint
import datafiles

PP = pprint.PrettyPrinter(indent=4)

def main(include_recurring):
	invoices = datafiles.read(include_recurring)
	PP.pprint(invoices)


if __name__ == "__main__":
	include_recurring = '--recurring' in sys.argv
	main(include_recurring)
