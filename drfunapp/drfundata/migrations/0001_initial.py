# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-29 18:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WebResource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('uri', models.URLField(max_length=2000)),
            ],
            options={
                'verbose_name': 'Web Resource',
            },
        ),
        migrations.CreateModel(
            name='WebResourceType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'verbose_name': 'Web Resource Type',
            },
        ),
        migrations.AddField(
            model_name='webresource',
            name='resource_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='drfundata.WebResourceType', verbose_name='Resource Type'),
        ),
    ]
