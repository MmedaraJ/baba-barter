# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2022-02-25 23:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('baba_barter', '0002_auto_20220221_0141'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='baba_barter.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Swappable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('short_description', models.TextField(max_length=50)),
                ('long_description', models.TextField()),
                ('notes', models.TextField()),
                ('value', models.IntegerField(default=0)),
                ('score', models.IntegerField(default=100)),
                ('condition', models.IntegerField(default=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_swappables', to='baba_barter.Category')),
                ('subcategories', models.ManyToManyField(related_name='all_swappables', to='baba_barter.SubCategory')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='score',
            field=models.IntegerField(default=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='description',
            field=models.TextField(max_length=255),
        ),
        migrations.AddField(
            model_name='swappable',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_swappables', to='baba_barter.User'),
        ),
    ]
