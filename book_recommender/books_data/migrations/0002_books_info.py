# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books_data', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='books_info',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('bookId', models.CharField(max_length=255)),
                ('bookName', models.CharField(max_length=255)),
                ('bookAuthor', models.CharField(max_length=255)),
                ('year', models.IntegerField()),
                ('publisher', models.CharField(max_length=255)),
                ('img1', models.CharField(max_length=255)),
                ('img2', models.CharField(max_length=255)),
                ('img3', models.CharField(max_length=255)),
            ],
        ),
    ]
