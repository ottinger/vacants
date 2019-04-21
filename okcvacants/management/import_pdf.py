'''
import_pdf.py

Import data from the abandoned buildings registry PDF.
'''

import PyPDF2
import requests
import io
import re
import datetime

### test ###
import os
import vacants_project

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vacants_project.settings")
import django

django.setup()
### ###

import okcvacants.models

# Get the file, and use BytesIO to make it accessible from memory like a real file
r = requests.get("https://www.okc.gov/home/showdocument?id=5517", stream=True)
pdf_data = io.BytesIO()
pdf_data.write(r.content)

# Create PyPDF2 reader
reader = PyPDF2.PdfFileReader(pdf_data)

case_number_regex = r'^C[0-9]{2}-[0-9]{5}$'
date_regex = r'^[0-9]{1,2}\/[0-9]{1,2}\/[0-9]{4}$'
ward_number_regex = r'^[0-9]+$'  # support >1 digit for flexibility though there are 8 wards

# for i in range(reader.getNumPages()):
for i in [0]:
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
            p = okcvacants.models.Property()
            p.case_number = l
            p.address = ""
            case_number_found = True  # we're processing a record now
        # If we're here and haven't gotten the date yet, it's an address line.
        elif case_number_found and not date_found and not re.match(date_regex, l):
            print("xx" + l)
            p.address += l + " "
        elif case_number_found and re.match(date_regex, l):
            date_found = True
            p.declared_date = datetime.datetime.strptime(l, "%m/%d/%Y").date()
            pass  # we need to process date
        elif case_number_found and not p.ward_number:
            p.ward_number = int(l)
        elif case_number_found and not p.parcel_number:
            p.parcel_number = int(l)
            case_number_found = False  # done processing record
            date_found = False
            p.save()
            print(vars(p))
