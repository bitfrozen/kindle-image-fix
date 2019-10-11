import sys, argparse, bs4
from argparse import RawDescriptionHelpFormatter

# Guard against Py2
if sys.version_info[0] == 2:
    print("Need to use Python 3")
    sys.exit()

# Setup command line arguments
parser = argparse.ArgumentParser(description="Parses html files, looks for img tags and replaces them with a structure suitable for both mobi and non-mobi kindle files. <img> has to have attributes:\n  alt - All content of alt attribute is used as image caption.\n  width - Value inside width attribute is used to specify percentage of width of image on non-mobi devices and as a width percentage in pixels calculation for mobi devices.", formatter_class=RawDescriptionHelpFormatter)
parser.add_argument("filename", help="Name of the file containing html to parse", type=argparse.FileType('r'))
parser.add_argument("-c", "--captions", help="Add this option if you want alt attribute to be used for image captions", action="store_true")
args = parser.parse_args()
print(args.filename)
print(args.captions)