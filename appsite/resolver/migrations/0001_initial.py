# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-14 21:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Inchi',
            fields=[
                ('uid', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('version', models.IntegerField(blank=True, null=True)),
                ('is_standard', models.BooleanField(default=False)),
                ('block1', models.CharField(max_length=14)),
                ('block2', models.CharField(max_length=10)),
                ('block3', models.CharField(max_length=1)),
                ('key', models.CharField(blank=True, max_length=27, null=True)),
                ('string', models.CharField(blank=True, max_length=32768, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('uid', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=32768, unique=True)),
                ('abbreviation', models.CharField(blank=True, max_length=32, null=True)),
                ('url', models.URLField(blank=True, max_length=4096, null=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='resolver.Organization')),
            ],
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('uid', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=32768)),
                ('group', models.CharField(blank=True, max_length=32768, null=True)),
                ('contact', models.CharField(blank=True, max_length=32768, null=True)),
                ('url', models.URLField(blank=True, max_length=4096, null=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='resolver.Organization')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='resolver.Publisher')),
            ],
        ),
        migrations.CreateModel(
            name='UriEndPoint',
            fields=[
                ('uid', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('uri', models.CharField(max_length=32768)),
                ('description', models.TextField(blank=True, max_length=32768, null=True)),
                ('media_type', models.CharField(blank=True, max_length=1024, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UrlEntryPoint',
            fields=[
                ('uid', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('url', models.URLField(max_length=4096)),
                ('description', models.TextField(blank=True, max_length=32768, null=True)),
                ('is_inchi_resolver', models.BooleanField(default=False)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='resolver.UrlEntryPoint')),
                ('publisher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resolver.Publisher')),
            ],
        ),
        migrations.AddField(
            model_name='uriendpoint',
            name='entrypoint',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resolver.UrlEntryPoint'),
        ),
        migrations.AlterUniqueTogether(
            name='inchi',
            unique_together=set([('block1', 'block2', 'block3', 'version')]),
        ),
        migrations.AlterUniqueTogether(
            name='urlentrypoint',
            unique_together=set([('parent', 'publisher', 'url', 'is_inchi_resolver')]),
        ),
        migrations.AlterUniqueTogether(
            name='uriendpoint',
            unique_together=set([('entrypoint', 'uri')]),
        ),
        migrations.AlterUniqueTogether(
            name='publisher',
            unique_together=set([('parent', 'organization', 'name', 'group', 'contact')]),
        ),
    ]
