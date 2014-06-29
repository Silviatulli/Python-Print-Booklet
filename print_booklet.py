#!/usr/bin/env python
# -*- coding: utf-8 -*-
# usage: print_booklet.py input_path.pdf

########################
# Python print booklet #
########################

from PyPDF2 import PdfFileWriter, PdfFileReader
from datetime import datetime
import sys

def main():

    ### Variables
    input_pdf_path = sys.argv[1]

    # Printing mode
    verbose = bool(raw_input('Verbose: True or False? '))

    # Signature number
    signature_number = int(raw_input('Signatures number: '))

    # Mode (regular, irregular)
    mode = raw_input('Signature pages number: regular or irregular? ')

    # Signature pages number (if irregular)
    if mode == 'irregular':
        signature_list = raw_input('If the signature pages number is irregular, insert your signature pages sequence (separated by comma): ').split(',')
        signature_list = [int(x) for x in signature_list]

    elif mode == 'regular':
        pass
    
    else:
        print 'input error'
        sys.exit()

    ### Program
    output_pdf_path = input_pdf_path[:-4] + '_IMPOSED.pdf'

    # Opening input file
    input_pdf = PdfFileReader(file(input_pdf_path, 'rb'))
    if verbose == True: print('Pages amount: %01d' % input_pdf.getNumPages())

    # Output writer
    output_pdf = PdfFileWriter()

    # Pages sequence list
    if mode == 'regular':
        signature_list = [input_pdf.getNumPages() / signature_number]* signature_number

    # Values verifying
    for each_value in signature_list:
        if each_value % 4 == 0:
            pass
        else:
            print "Number pages error!"
            sys.exit()

    # Creating the pages matrix
    pages_list = range(0, input_pdf.getNumPages())
    pages_matrix = []

    for signature_pages_amount in signature_list:
        signature_pages = []

        for signature_page_index in range(0, signature_pages_amount):
            signature_pages.append(pages_list.pop(0))

        pages_matrix.append(signature_pages)

    # Iterating over signatures
    for i, each_signature in enumerate(pages_matrix):
        i = i+1
        if verbose == True: print('\n Signature %01d' % i)

        # Iterating over spread to impose
        for each_spread_number in range(1, len(each_signature)/2 +1):
            if verbose == True: print('\t Spread: %01d' % each_spread_number)

            # Extracting pages to impose
            last = each_signature.pop(-1)
            first = each_signature.pop(0)

            # odd spreads 
            if each_spread_number % 2 == 1:

                # extracting last page
                starting_page = input_pdf.getPage(last)

                # extracting first page
                toMerge_page = input_pdf.getPage(first)
                if verbose == True: print('\t\t Pages: %01d %01d' % (last, first))


            # even spreads
            else:
                # extracting first page
                starting_page = input_pdf.getPage(first)

                # extracting last page
                toMerge_page = input_pdf.getPage(last)
                if verbose == True: print('\t\t Pages: %01d %01d' % (first, last))

            # Merging pages
            starting_page.mergeScaledTranslatedPage(toMerge_page, 1, int(starting_page.trimBox.getUpperRight_x()), 0, expand=True)

            # Appending pages to output
            output_pdf.addPage(starting_page)

    # Exporting and saving output file
    outputStream = file(output_pdf_path, "wb")
    output_pdf.write(outputStream)
    print("done!")

# Launch!
if __name__ == "__main__":
    main()
