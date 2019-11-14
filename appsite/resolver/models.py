from __future__ import unicode_literals

import uuid
from urllib.parse import urljoin

from django.core.exceptions import FieldError
from rdkit import Chem

from django.db import models

from inchi.identifier import InChIKey, InChI


class Inchi(models.Model):
    uid = models.UUIDField(primary_key=True, editable=False)
    version = models.IntegerField(db_index=True, default=1)
    block1 = models.CharField(db_index=True, max_length=14)
    block2 = models.CharField(db_index=True, max_length=10)
    block3 = models.CharField(db_index=True, max_length=1)
    key = models.CharField(max_length=27, blank=True, null=True)
    string = models.CharField(max_length=32768, blank=True, null=True)
    is_standard = models.BooleanField(default=False)

    class Meta:
        unique_together = ('block1', 'block2', 'block3', 'version')

    @classmethod
    def create(cls, *args, **kwargs):

        if 'url_prefix' in kwargs:
            url_prefix = kwargs['url_prefix']
            inchiargs = kwargs.pop('url_prefix')
            inchi = cls(*args, inchiargs)
        else:
            url_prefix = None
            inchi = cls(*args, **kwargs)

        k = None
        s = None
        if 'key' in kwargs and kwargs['key']:
            k = InChIKey(kwargs['key'])

        if 'string' in kwargs and kwargs['string']:
            s = InChI(kwargs['string'])
            _k = InChIKey(Chem.InchiToInchiKey(kwargs['string']))
            if k:
                if not k.element['well_formatted'] == _k.element['well_formatted']:
                    raise FieldError("InChI key does not represent InChI string")
            else:
                k = _k

        inchi.key = k.element['well_formatted_no_prefix']
        inchi.version = k.element['version']
        inchi.is_standard = k.element['is_standard']
        inchi.block1 = k.element['block1']
        inchi.block2 = k.element['block2']
        inchi.block3 = k.element['block3']
        if s:
            inchi.string = s.element['well_formatted']
        if url_prefix:
            inchi.uid = uuid.uuid5(uuid.NAMESPACE_URL, urljoin(url_prefix, inchi.key))
        else:
            inchi.uid = uuid.uuid5(uuid.NAMESPACE_URL, inchi.key)

        return inchi

    def __str__(self):
        return self.key


class Organization(models.Model):
    uid = models.UUIDField(primary_key=True, editable=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, default=None, null=True)
    name = models.CharField(unique=True, max_length=32768)
    abbreviation = models.CharField(max_length=32, blank=True, null=True)
    url = models.URLField(max_length=4096, blank=True, null=True)
    added = models.DateTimeField(auto_now_add=True)
    modified= models.DateTimeField(auto_now=True)

    @classmethod
    def create(cls, *args, **kwargs):
        organization = cls(*args, **kwargs)
        organization.uid = uuid.uuid5(uuid.NAMESPACE_URL, kwargs.get('name'))
        return organization

    def __str__(self):
        return self.name


class Publisher(models.Model):
    uid = models.UUIDField(primary_key=True, editable=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, default=None)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=32768)
    group = models.CharField(max_length=32768, blank=True, null=True)
    contact = models.CharField(max_length=32768, blank=True, null=True)
    url = models.URLField(max_length=4096, blank=True, null=True)
    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('parent', 'organization', 'name', 'group', 'contact')

    class JSONAPIMeta:
        resource_name = "inchi"

    @classmethod
    def create(cls, *args, **kwargs):
        publisher = cls(*args, **kwargs)
        publisher.uid = uuid.uuid5(uuid.NAMESPACE_URL, "/".join([
            kwargs.get('name'),
            str(kwargs.get('organization', None)),
            str(kwargs.get('parent', None)),
            kwargs.get('group', None),
            kwargs.get('contact', None)
        ]))
        return publisher

    def __str__(self):
        return "%s[%s, %s]" % (self.name, self.group, self.contact)


class UrlEntryPoint(models.Model):
    uid = models.UUIDField(primary_key=True, editable=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, default=None)
    publisher = models.ForeignKey('Publisher', on_delete=models.CASCADE, default=None)
    url = models.URLField(max_length=4096)
    description = models.TextField(max_length=32768, blank=True, null=True)
    is_inchi_resolver = models.BooleanField(default=False)

    class Meta:
        unique_together = ('parent', 'publisher', 'url', 'is_inchi_resolver')

    @classmethod
    def create(cls, *args, **kwargs):
        entrypoint = cls(*args, **kwargs)
        entrypoint.uid = uuid.uuid5(uuid.NAMESPACE_URL, "/".join([
            str(kwargs.get('parent', None)),
            str(kwargs.get('publisher')),
            kwargs.get('url'),
            str(kwargs.get('is_inchi_resolver', False))
        ]))
        return entrypoint

    def __str__(self):
        return "%s[%s]" % (self.publisher, self.url)


class UriEndPoint(models.Model):
    uid = models.UUIDField(primary_key=True, editable=False)
    entrypoint = models.ForeignKey('UrlEntryPoint', on_delete=models.CASCADE, default=None)
    uri = models.CharField(max_length=32768)
    description = models.TextField(max_length=32768, blank=True, null=True)
    media_type = models.CharField(max_length=1024, blank=True, null=True)

    class Meta:
        unique_together = ('entrypoint', 'uri')

    @classmethod
    def create(cls, *args, **kwargs):
        endpoint = cls(*args, **kwargs)
        endpoint.uid = uuid.uuid5(uuid.NAMESPACE_URL, "/".join([
            str(kwargs.get('entrypoint')),
            kwargs.get('uri'),
            kwargs.get('media_type', None)
        ]))
        return endpoint

    def __str__(self):
        return "%s[%s]" % (self.uri, self.entrypoint)
