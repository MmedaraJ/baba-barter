# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2022-03-16 16:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('baba_barter', '0012_swappableaddress'),
    ]

    operations = [
        migrations.RenameField(
            model_name='swappableaddress',
            old_name='postalcode',
            new_name='code',
        ),
    ]
