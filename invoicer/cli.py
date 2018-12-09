from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-t", "--test", dest="testmode", action="store_true", help="run in test mode")
parser.add_argument("-x", "--no-mail", dest="nomail", action="store_true", help="do not send email")
args = parser.parse_args()
