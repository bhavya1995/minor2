# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='results',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('userId', models.IntegerField()),
                ('bookId', models.CharField(max_length=255)),
                ('rating', models.IntegerField()),
            ],
        ),
    ]
