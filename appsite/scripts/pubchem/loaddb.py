from os import sys, path, environ

from resolver.models import *

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
sys.path.append('/home/app')

from client.lib.pubchem_client import PubchemClient

def run():

    Organization.objects.all().delete()
    Inchi.objects.all().delete()
    Publisher.objects.all().delete()
    EntryPoint.objects.all().delete()

    client = PubchemClient()

    o1 = Organization.create(
        name="U.S. National Institutes of Health",
        abbreviation="NIH",
        href="https://www.nih.gov",
        parent=None
    )
    o1.save()

    o2 = Organization.create(
        name="U.S. National Library of Medicine",
        abbreviation="NLM",
        href="https://www.nlm.nih.gov",
        parent=o1
    )
    o2.save()

    o3 = Organization.create(
        name="U.S. National Center for Biotechnology Information",
        abbreviation="NCBI",
        href="https://www.ncbi.nlm.nih.gov",
        parent=o2
    )
    o3.save()

    p1 = Publisher.create(
        name="PubChem",
        group="PubChem group",
        contact="pubchem-help@ncbi.nlm.nih.gov",
        href="https://pubchemdocs.ncbi.nlm.nih.gov/contact",
        organization=o2
    )
    p1.save()

    e1 = EntryPoint.create(
        name="PubChem PUG REST",
        description="PUG (Power User Gateway), a web interface for accessing PubChem data and services",
        category="service",
        href="https://pubchem.ncbi.nlm.nih.gov/rest/pug",
        publisher=p1
    )
    e1.save()

    e2 = EntryPoint.create(
        name="InChI Trust Root Resolver",
        description="Root InChI Resolver at InChI Trust",
        category="resolver",
        href="http://root.inchi-resolver.org",
        publisher=p1
    )
    e2.save()

    # x1 = EndPoint.create(
    #     entrypoint=e1,
    #     category="uripattern",
    #     uri="{+stdinchi|+stdinchikey}/smiles",
    #     description="Standard InChI to SMILES conversion",
    #     content_media_type="text/plain",
    # )
    # x1.save()

    for j in range(1, 30):

        ilist = client.fetch_inchi(range(j * 10, j * 10 + 10))

        for cid, i in ilist:
            print("Loading: %s" % (i,))
            try:
                inchi = Inchi.create(
                    string=i
                )
                print('{} {}'.format(inchi, inchi.added))
                inchi.save()
                inchi.entrypoints.add(e1)
            except Exception as e:
                print(e)
