# Generated by Django 2.2.11 on 2020-07-27 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resolver', '0002_auto_20200727_2134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='endpoint',
            name='accept_header_media_types',
            field=models.ManyToManyField(null=True, related_name='accepting_endpoints', to='resolver.MediaType'),
        ),
        migrations.AlterField(
            model_name='endpoint',
            name='content_media_types',
            field=models.ManyToManyField(null=True, related_name='delivering_endpoints', to='resolver.MediaType'),
        ),
    ]
