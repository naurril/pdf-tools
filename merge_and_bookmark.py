from argparse import ArgumentParser
from glob import glob
from PyPDF2 import PdfMerger
import os


def readcsv(file):
    with open(file) as f:
        lines = f.readlines()
        return [x.strip().split(",") for x in lines]
    
def merge(path, output_filename):
    merger = PdfMerger(strict=False)
    files = glob(path + os.sep + '*.pdf')
    files.sort()

    csv = readcsv(path + os.sep + 'content.csv')
    print(csv)

    for item in csv: 
        pdffile = path + os.sep + item[0]
        print(f"Appending: '{pdffile}'")
        bookmark = os.path.basename(item[1])
        res = merger.append(pdffile, bookmark)
        print(res)
    merger.write(output_filename)
    merger.close()

if __name__ == "__main__":
    parser = ArgumentParser()
    # Add more options if you like
    parser.add_argument("-o", "--output",
                        dest="output_filename",
                        default="/home/lie/Documents/Test.pdf",
                        help="write merged PDF to FILE",
                        metavar="FILE")
    parser.add_argument("-p", "--path",
                        dest="path",
                        default="/home/lie/Documents/openscenario2",
                        help="path of source PDF files")
    args = parser.parse_args()
    merge(args.path, args.output_filename)