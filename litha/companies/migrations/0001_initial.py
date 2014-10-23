# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import companies.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50, validators=[django.core.validators.MinLengthValidator(2), django.core.validators.RegexValidator(b'^[a-zA-Z]+[a-zA-Z0-9_ ]?\\w$'), companies.validators.stop_list_validator])),
                ('description', models.CharField(max_length=350, blank=True)),
                ('mobile', models.CharField(blank=True, max_length=12, validators=[django.core.validators.RegexValidator(b'^\\+?[0-9]{3}-?[0-9]{6,12}$')])),
                ('phone1', models.CharField(max_length=12, validators=[django.core.validators.RegexValidator(b'^\\+?[0-9]{3}-?[0-9]{6,12}$')])),
                ('phone2', models.CharField(blank=True, max_length=12, validators=[django.core.validators.RegexValidator(b'^\\+?[0-9]{3}-?[0-9]{6,12}$')])),
                ('website', models.URLField(blank=True)),
                ('address', models.TextField()),
                ('logo', models.ImageField(blank=True, upload_to=b'', validators=[companies.validators.validate_image_size])),
                ('status', models.CharField(default=b'active', max_length=10, choices=[(b'active', b'ACTIVE'), (b'blocked', b'BLOCKED'), (b'deleted', b'DELETED')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
