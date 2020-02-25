from os import sys, path, environ

from resolver.models import *

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
sys.path.append('/home/app')

def run():

    Organization.objects.all().delete()
    InChI.objects.all().delete()
    Publisher.objects.all().delete()
    EntryPoint.objects.all().delete()


    o1 = Organization.create(
        name="InChI Trust",
        abbreviation="",
        href="https://www.inchi-trust.org/",
        parent=None
    )
    o1.save()

    p1 = Publisher.create(
        name="Markus Sitzmann",
        group="",
        contact="markus.sitzmann@gmail.com",
        href="http://inchi-resolver.org",
        organization=o1
    )
    p1.save()

    e2 = EntryPoint.create(
        name="NCI/CADD InChI Resolver",
        description="InChI Resolver of CADD group at NCI",
        category="inchiresolver",
        href="http://cactus.inchi-resolver.org",
        publisher=None
    )
    e2.save()

    # e2 = EntryPoint.create(
    #     name="PubChem InChI Resolver",
    #     description="InChI Resolver of PubChem group at NLM/NCBI",
    #     category="inchiresolver",
    #     href="http://pubchem.inchi-resolver.org",
    #     publisher=None
    # )
    # e2.save()






