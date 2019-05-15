'''
import_pdf.py

Import data from the abandoned buildings registry PDF.
'''

import PyPDF2
import requests
import io
import re
import datetime

import os
import django
from django.core.management.base import BaseCommand

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vacants_project.settings")
django.setup()

from okcvacants.models import Property


class Command(BaseCommand):
    help = "Imports data from the OKC abandoned building registry PDF."

    def add_arguments(self, parser):
        parser.add_argument('-u', '--url', type=str, help='URL for the location of the abandoned properties PDF')
        parser.add_argument('-f', '--filename', type=str, help='Filename for the abandoned properties PDF')
    def handle(self, *args, **options):
        if options['filename']:
            f = open(options['filename'], "rb")
        elif options['url']:
            url = options['url']
        else:
            url = "https://www.okc.gov/home/showdocument?id=5517"

        if options['filename']:
            self.parse_pdf(f)
        else:
            # Get the file, and use BytesIO to make it accessible from memory like a real file
            r = requests.get(url, stream=True)
            pdf_data = io.BytesIO()
            pdf_data.write(r.content)
            self.parse_pdf(pdf_data)

    def parse_pdf(self, pdf_data):
        # Create PyPDF2 reader
        reader = PyPDF2.PdfFileReader(pdf_data)

        case_number_regex = r'^C[0-9]{2}-[0-9]{5}$'
        date_regex = r'^[0-9]{1,2}\/[0-9]{1,2}\/[0-9]{4}$'
        ward_number_regex = r'^[0-9]+$'  # support >1 digit for flexibility though there are 8 wards

        pdf_property_list = []  # We'll store the Propertys in this list temporarily
        for i in range(reader.getNumPages()):
            # Now do our magic!
            pageObj = reader.getPage(i)
            split_lines = str.splitlines(pageObj.extractText())

            '''
            The iterator will give us lines like this:
            1. Case number (in format in case_number_regex)
            2. Address (line 1)
            2a. Address (line 2 - not on most entries)
            3. Declared date (in format in date_regex)
            4. Ward number
            5. Parcel number
            '''
            p = None
            case_number_found = False
            date_found = False
            for l in split_lines:
                # Case number means we're starting on a new record. Create a new record.
                if re.match(case_number_regex, l):
                    print(l)
                    p = Property()
                    p.case_number = l
                    p.address = ""
                    case_number_found = True  # we're processing a record now
                # If we're here and haven't gotten the date yet, it's an address line.
                elif case_number_found and not date_found and not re.match(date_regex, l):
                    p.address += l + " "
                elif case_number_found and re.match(date_regex, l):
                    date_found = True
                    p.declared_date = datetime.datetime.strptime(l, "%m/%d/%Y").date()
                    pass  # we need to process date
                elif case_number_found and not p.ward_number:
                    try:
                        p.ward_number = int(l)
                    except:
                        print("Exception on converting ward_number for case_number: " + p.case_number)
                        p.ward_number = -1
                elif case_number_found and not p.parcel_number:
                    try:
                        p.parcel_number = int(l)
                    except:
                        # There is at least one parcel number that is in invalid format. It has pound/# signs
                        # in it so I am assuming it's a mistake. This can be changed later if it's not
                        print("Exception on converting parcel_number for case_number: " + p.case_number)
                        p.parcel_number = -1

                    case_number_found = False  # done processing record
                    date_found = False
                    pdf_property_list.append(p)
                    print(vars(p))

        # Now we'll go through pdf_property_list, and existing Property objects in the table.
        db_case_numbers = [p.case_number for p in Property.objects.all()]
        pdf_case_numbers = [p.case_number for p in pdf_property_list]

        # Find existing Property objects that are NOT in the PDF list, and remove them
        for p in Property.objects.all():
            if p.case_number not in pdf_case_numbers:
                Property.objects.filter(case_number=p.case_number).delete()
        # Find Property case numbers from the PDF that are NOT existing, and add them.
        for p in pdf_property_list:
            if p.case_number not in db_case_numbers:
                p.save()


        self.stdout.write("PDF parsing completed")
