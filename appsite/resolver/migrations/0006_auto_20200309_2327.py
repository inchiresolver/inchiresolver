# Generated by Django 2.2.10 on 2020-03-09 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resolver', '0005_auto_20200309_2226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrypoint',
            name='category',
            field=models.CharField(choices=[('site', 'site'), ('service', 'service'), ('resolver', 'resolver')], default='site', max_length=16),
        ),
    ]
