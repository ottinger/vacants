from django.test import TestCase
from okcvacants.models import Property
from django.core.management import call_command

from vacants_project.settings import BASE_DIR
import os
import datetime


# Create your tests here.
class ImportPDFTestCase(TestCase):
    def setUp(self):
        # Fake Property for testing purposes (Devon Tower). We won't save it yet though.
        self.test_p = Property(case_number="C99-99999", address="333 W SHERIDAN AVE OKLAHOMA CITY, OK 73102",
                               declared_date=datetime.date(2016, 1, 1), ward_number=6, parcel_number=9999999)

    # Add first page of records, and ensure the count is correct.
    def test_correct_count(self):
        call_command('import_pdf', filename=os.path.join(BASE_DIR, "abandoned_first_page.pdf"))

        self.assertEquals(36, Property.objects.all().count())

    # Test to ensure that when a property list is imported, that properties no longer on the list
    # are deleted. Add an address that is NOT in the pdf, and make sure it is not there after
    # import_pdf is run.
    def test_removed_property_is_deleted(self):
        # Add properties from the test page, then add test_p. We should have 37 properties
        call_command('import_pdf', filename=os.path.join(BASE_DIR, "abandoned_first_page.pdf"))
        self.assertEquals(36, Property.objects.all().count())
        self.test_p.save()  # Add test_p
        self.assertEquals(37, Property.objects.all().count())

        # Run import_pdf again with the test page. We should have 36, as the devon tower one will be removed
        call_command('import_pdf', filename=os.path.join(BASE_DIR, "abandoned_first_page.pdf"))
        self.assertEquals(36, Property.objects.all().count())

    # Run import_pdf to add properties, remove one, and run import_pdf again. We should have
    # 36 properties again.
    def test_missing_property_is_added(self):
        call_command('import_pdf', filename=os.path.join(BASE_DIR, "abandoned_first_page.pdf"))
        self.assertEquals(36, Property.objects.all().count())
        Property.objects.filter(case_number="C15-05764").delete()
        self.assertEquals(35, Property.objects.all().count())

        call_command('import_pdf', filename=os.path.join(BASE_DIR, "abandoned_first_page.pdf"))
        self.assertEquals(36, Property.objects.all().count())
