from django.test import TestCase
from okcvacants.models import Property
from django.core.management import call_command

from vacants_project.settings import BASE_DIR
import os


# Create your tests here.
class ImportPDFTestCase(TestCase):
    def test_correct_count(self):
        call_command('import_pdf', filename=os.path.join(BASE_DIR, "abandoned_first_page.pdf"))

        self.assertEquals(36, Property.objects.all().count())
