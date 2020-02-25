from os import sys, path, environ

from resolver.models import *

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
sys.path.append('/home/app')

from client.lib.cactus_client import CactusClient

def run():

    Organization.objects.all().delete()
    InChI.objects.all().delete()
    Publisher.objects.all().delete()
    EntryPoint.objects.all().delete()

    client = CactusClient()

    o1 = Organization.create(
        name="National Institutes of Health",
        abbreviation="NIH",
        href="https://www.nih.gov",
        parent=None
    )
    o1.save()

    o2 = Organization.create(
        name="National Cancer Institute",
        abbreviation="NCI",
        href="https://www.cancer.gov",
        parent=o1
    )
    o2.save()

    p1 = Publisher.create(
        name="Marc Nicklaus",
        group="NCI/CADD group",
        contact="marc.nicklaus@email.com",
        href="https://ccr2.cancer.gov/resources/CBL/Scientists/Nicklaus.aspx",
        organization=o2
    )
    p1.save()

    e1 = EntryPoint.create(
        name="Chemical Identifier Resolver",
        description="This service works as a resolver for different chemical structure identifiers and allows the conversion of a given structure identifier into another representation or structure identifier. It can be used via a web form or a simple URL API.",
        category="service",
        href="http://cactus.nci.nih.gov/chemical/structure",
        publisher=p1
    )
    e1.save()

    x1 = EndPoint.create(
        entrypoint=e1,
        category="uripattern",
        uri="{+stdinchi|+stdinchikey}/smiles",
        description="Standard InChI to SMILES conversion",
        media_type="text/plain",
    )
    x1.save()

    x2 = EndPoint.create(
        entrypoint=e1,
        category="uripattern",
        uri="{+stdinchi,+stdinchikey}/iupac_name",
        description="Standard InChI to IUPAC name conversion",
        media_type="text/plain",
    )
    x2.save()

    x3 = EndPoint.create(
        entrypoint=e1,
        category="uripattern",
        uri="{+stdinchi,+stdinchikey}/image",
        description="InChI to SMILES conversion",
        media_type="image/gif"
    )
    x3.save()

    x4 = EndPoint.create(
        entrypoint=e1,
        category="uripattern",
        uri="{+smiles}/stdinchi",
        description="SMILES to stdinchi conversion",
        media_type="text/plain",
    )
    x4.save()

    x5 = EndPoint.create(
        entrypoint=e1,
        category="uripattern",
        uri="{+smiles}/stdinchikey",
        description="SMILES to stdinchikey conversion",
        media_type="text/plain",
    )
    x5.save()

    for j in range(1, 30):

        ilist = client.fetch_inchi(range(j * 10, j * 10 + 10))

        for cid, i in ilist:
            print("Loading: %s" % (i,))
            try:
                inchi = InChI.create(
                    string=i
                )
                print('{} {}'.format(inchi, inchi.added))
                inchi.save()
                inchi.entrypoints.add(e1)
            except Exception as e:
                print(e)
