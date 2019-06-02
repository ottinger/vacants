# Generated by Django 2.2 on 2019-06-02 02:51

from django.db import migrations, models
from django.apps import apps

import re


def forwards(app, schema_editor):
    Property = apps.get_model('okcvacants', 'Property')

    address_regex = r'^(.*[a-zA-Z0-9])\s+OKLAHOMA CITY'

    for p in Property.objects.all():
        address_match = re.match(address_regex, p.address, re.IGNORECASE)
        if address_match:
            p.short_address = address_match.group(1)
        else:
            p.short_address = p.address
        p.save(update_fields=['short_address'])


class Migration(migrations.Migration):
    dependencies = [
        ('okcvacants', '0013_auto_20190516_0208'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='short_address',
            field=models.CharField(default='', max_length=150),
            preserve_default=False,
        ),
        migrations.RunPython(forwards, reverse_code=migrations.RunPython.noop)
    ]
