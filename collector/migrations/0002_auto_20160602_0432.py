# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-02 04:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DBStatusModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField()),
            ],
        ),
        migrations.AlterField(
            model_name='restaurantmodel',
            name='expensivelevel',
            field=models.TextField(),
        ),
    ]