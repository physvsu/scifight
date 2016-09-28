# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-28 14:51
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scifight', '0002_add_userprofile_model'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Jury',
            new_name='Juror',
        ),
        migrations.RenameField(
            model_name='fight',
            old_name='juries',
            new_name='jury',
        ),
        migrations.RenameField(
            model_name='jurypoints',
            old_name='jury',
            new_name='juror',
        ),
        migrations.RenameField(
            model_name='leadertojury',
            old_name='jury',
            new_name='juror',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='scifight_extra', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='jurypoints',
            unique_together=set([('fight_stage', 'juror')]),
        ),
        migrations.AlterUniqueTogether(
            name='leadertojury',
            unique_together=set([('leader', 'juror')]),
        ),
        migrations.RenameModel(
            old_name='JuryPoints',
            new_name='JurorPoints',
        ),
        migrations.RenameModel(
            old_name='LeaderToJury',
            new_name='LeaderToJuror',
        ),
    ]
