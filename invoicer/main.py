import sys
import datafiles

def main(include_recurring):
	invoices = datafiles.read(include_recurring)
	print(invoices)


if __name__ == "__main__":
	include_recurring = '--recurring' in sys.argv
	main(include_recurring)
