# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db  import migrations
from scifight   import models


def create_fake_tournament(apps, schema_editor):
    if models.Team.objects.count() > 0 or models.Fight.objects.count() > 0:
        fake_tournament = models.Tournament(name="--- FAKE MIGRATION TOURNAMENT, DELETE ASAP ---")
        fake_tournament.save()
    if models.Team.objects.all():
        models.Team.objects.update(tournament=fake_tournament)
    if models.Fight.objects.all():
        models.Fight.objects.update(tournament=fake_tournament)


class Migration(migrations.Migration):

    dependencies = [
        ('scifight', '0011_firght_alter_tournament_nullable_team_alter_tournament_nullable'),
    ]

    operations = [
        migrations.RunPython(
            create_fake_tournament,
            reverse_code=migrations.RunPython.noop),
    ]
