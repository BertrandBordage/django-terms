# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='Variants of the name can be specified with a \u201c|\u201d separator (e.g. \u201cname|names|to name\u201d).', unique=True, max_length=100, verbose_name='name')),
                ('case_sensitive', models.BooleanField(default=False, verbose_name='case sensitive')),
                ('definition', models.TextField(help_text='Accepts HTML tags.', verbose_name='definition', blank=True)),
                ('url', models.CharField(help_text='Address to which the term will redirect (instead of redirecting to the definition).', max_length=200, verbose_name='link', blank=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'term',
                'verbose_name_plural': 'terms',
            },
            bases=(models.Model,),
        ),
    ]
