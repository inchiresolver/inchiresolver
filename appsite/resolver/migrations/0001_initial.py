# Generated by Django 2.2.11 on 2020-08-02 16:57

from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MediaType',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=1024, unique=True)),
                ('description', models.TextField(blank=True, max_length=32768, null=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=32768)),
                ('abbreviation', models.CharField(blank=True, max_length=32, null=True)),
                ('category', models.CharField(choices=[('regulatory', 'Regulatory'), ('government', 'Government'), ('academia', 'Academia'), ('company', 'Company'), ('vendor', 'Vendor'), ('research', 'Research'), ('publishing', 'Publishing'), ('provider', 'Provider'), ('public', 'Public'), ('society', 'Society'), ('charity', 'Charity'), ('other', 'Other'), ('none', 'None')], default='none', max_length=16)),
                ('href', models.URLField(blank=True, max_length=4096, null=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='resolver.Organization')),
            ],
            options={
                'unique_together': {('parent', 'name')},
            },
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('category', models.CharField(choices=[('entity', 'Entity'), ('service', 'Service'), ('network', 'Network'), ('division', 'Division'), ('group', 'Group'), ('person', 'Person'), ('other', 'Other'), ('none', 'None')], default='none', max_length=16)),
                ('name', models.CharField(max_length=1024)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('address', models.CharField(blank=True, max_length=8192, null=True)),
                ('href', models.URLField(blank=True, max_length=4096, null=True)),
                ('orcid', models.URLField(blank=True, max_length=4096, null=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('organization', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='publishers', to='resolver.Organization')),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='resolver.Publisher')),
            ],
            options={
                'unique_together': {('organization', 'parent', 'name', 'href', 'orcid')},
            },
        ),
        migrations.CreateModel(
            name='EntryPoint',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('category', models.CharField(choices=[('self', 'Self'), ('site', 'Site'), ('api', 'API'), ('resolver', 'Resolver')], default='site', max_length=16)),
                ('href', models.URLField(max_length=4096)),
                ('entrypoint_href', models.URLField(blank=True, max_length=4096, null=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, max_length=32768, null=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='resolver.EntryPoint')),
                ('publisher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='entrypoints', to='resolver.Publisher')),
            ],
            options={
                'unique_together': {('parent', 'publisher', 'href')},
            },
        ),
        migrations.CreateModel(
            name='Inchi',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('version', models.IntegerField(db_index=True, default=1)),
                ('block1', models.CharField(db_index=True, max_length=14)),
                ('block2', models.CharField(db_index=True, max_length=10)),
                ('block3', models.CharField(db_index=True, max_length=1)),
                ('key', models.CharField(blank=True, max_length=27, null=True)),
                ('string', models.CharField(blank=True, max_length=32768, null=True)),
                ('is_standard', models.BooleanField(default=False)),
                ('safe_options', models.CharField(db_index=True, default=None, max_length=2, null=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('entrypoints', models.ManyToManyField(related_name='inchis', to='resolver.EntryPoint')),
            ],
            options={
                'verbose_name': 'InChI',
                'unique_together': {('block1', 'block2', 'block3', 'version', 'safe_options')},
            },
        ),
        migrations.CreateModel(
            name='EndPoint',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('uri', models.CharField(max_length=32768)),
                ('category', models.CharField(choices=[('schema', 'Schema'), ('uritemplate', 'URI Template (RFC6570)'), ('documentation', 'Documentation (HTML, PDF)')], default='uritemplate', max_length=16)),
                ('request_methods', multiselectfield.db.fields.MultiSelectField(choices=[('GET', 'GET'), ('HEAD', 'HEAD'), ('POST', 'POST'), ('PUT', 'PUT'), ('DELETE', 'DELETE'), ('CONNECT', 'CONNECT'), ('OPTIONS', 'OPTIONS'), ('TRACE', 'TRACE'), ('PATCH', 'PATCH')], default=['GET'], max_length=52)),
                ('description', models.TextField(blank=True, max_length=32768, null=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('accept_header_media_types', models.ManyToManyField(related_name='accepting_endpoints', to='resolver.MediaType')),
                ('content_media_types', models.ManyToManyField(related_name='delivering_endpoints', to='resolver.MediaType')),
                ('entrypoint', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='endpoints', to='resolver.EntryPoint')),
                ('request_schema_endpoint', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='schema_requesting_endpoints', to='resolver.EndPoint')),
                ('response_schema_endpoint', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='schema_responding_endpoints', to='resolver.EndPoint')),
            ],
            options={
                'unique_together': {('entrypoint', 'uri')},
            },
        ),
    ]
