from os import sys, path, environ

from resolver.models import *

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
sys.path.append('/home/app')

def run():

    Organization.objects.all().delete()
    Inchi.objects.all().delete()
    Publisher.objects.all().delete()
    EntryPoint.objects.all().delete()


    o1 = Organization.create(
        name="InChI Trust",
        abbreviation="",
        href="https://www.inchi-trust.org/",
        category="charity",
        parent=None,
    )
    o1.save()

    p1 = Publisher.create(
        name="InChI Resolver Group",
        category="group",
        email="root.inchiresolver@gmail.com",
        organization=o1
    )
    p1.save()

    p2 = Publisher.create(
        name="Markus Sitzmann",
        category="person",
        email="markus.sitzmann@gmail.com",
        href="https://inchi-resolver.org",
        orcid="0000-0001-5346-1298",
        parent=p1
    )
    p2.save()

    e0 = EntryPoint.create(
        name="InChI Root Resolver",
        description="Demonstration InChI Root Resolver",
        category="self",
        href="http://root.inchi-resolver.org/",
        entrypoint_href="http://root.inchi-resolver.org/_self",
        publisher=p1
    )
    e0.save()

    e1 = EntryPoint.create(
        name="NCI/CADD InChI Resolver",
        description="Demonstration InChI Resolver of the NCI/CADD group",
        category="inchiresolver",
        href="http://cactus.inchi-resolver.org",
        entrypoint_href="http://cactus.inchi-resolver.org/_self",
        publisher=None,
        parent=e0
    )
    e1.save()

    e2 = EntryPoint.create(
        name="PubChem InChI Resolver",
        description="Demonstration InChI Resolver for PubChem",
        category="inchiresolver",
        href="http://pubchem.inchi-resolver.org",
        entrypoint_href="http://pubchem.inchi-resolver.org/_self",
        publisher=None,
        parent=e0
    )
    e2.save()









