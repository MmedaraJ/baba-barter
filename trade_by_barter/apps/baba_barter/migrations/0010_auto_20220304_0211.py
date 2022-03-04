# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2022-03-04 02:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('baba_barter', '0009_auto_20220303_2317'),
    ]

    operations = [
        migrations.AddField(
            model_name='swappable',
            name='is_banned',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='swappable',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='swappable',
            name='is_flagged',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_banned',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_flagged',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='category',
            field=models.ForeignKey(default='other', on_delete=django.db.models.deletion.SET_DEFAULT, related_name='subcategories', to='baba_barter.Category'),
        ),
        migrations.AlterField(
            model_name='swappable',
            name='category',
            field=models.ForeignKey(default='other', on_delete=django.db.models.deletion.SET_DEFAULT, related_name='category_swappables', to='baba_barter.Category'),
        ),
    ]
