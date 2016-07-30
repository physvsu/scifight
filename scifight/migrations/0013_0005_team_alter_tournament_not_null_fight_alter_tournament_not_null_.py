# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-30 12:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scifight', '0012_create_fake_tournament'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fight',
            name='tournament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scifight.Tournament'),
        ),
        migrations.AlterField(
            model_name='team',
            name='tournament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scifight.Tournament'),
        ),
    ]