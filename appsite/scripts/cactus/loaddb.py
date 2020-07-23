from os import sys, path, environ

from resolver.models import *

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
sys.path.append('/home/app')

from client.lib.cactus_client import CactusClient

def run():

    Organization.objects.all().delete()
    Inchi.objects.all().delete()
    Publisher.objects.all().delete()
    EntryPoint.objects.all().delete()
    MediaType.objects.all().delete()

    client = CactusClient()

    m1 = MediaType.create(
        name="text/plain",
        description="plain text media type"
    )
    m1.save()

    m2 = MediaType.create(
        name="image/gif",
        description = "GIF image",
    )
    m2.save()


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
        name="NCI Computer-Aided Drug Design (CADD) Group",
        category="group",
        organization=o2
    )
    p1.save()

    p2 = Publisher.create(
        name="Marc Nicklaus",
        category="person",
        email="marc.nicklaus@email.com",
        address="Frederick, MD 21702-1201, USA",
        href="https://ccr2.cancer.gov/resources/CBL/Scientists/Nicklaus.aspx",
        orcid="https://orcid.org/0000-0002-4775-7030",
        organization=o2,
        parent=p1
    )
    p2.save()

    # p3 = Publisher.create(
    #     name="John Doe",
    #     category="person",
    #     email="john.doe@email.com",
    #     address="Frederick, MD 21702-1201, USA",
    #     href="https://ccr2.cancer.gov/resources/CBL/Scientists/Nicklaus.aspx",
    #     orcid="https://orcid.org/xyz",
    #     organization=o2,
    #     parent=p1
    # )
    # p3.save()

    e0 = EntryPoint.create(
        name="NCI/CADD InChI Resolver",
        description="Demonstration InChI Resolver of the NCI/CADD group",
        category="self",
        href="https://cactus.inchi-resolver.org",
        entrypoint_href="https://cactus.inchi-resolver.org/_self",
        publisher=p1
    )
    e0.save()

    e1 = EntryPoint.create(
        name="Chemical Identifier Resolver",
        description="This service works as a resolver for different chemical structure identifiers and allows "
                    "the conversion of a given structure identifier into another representation or structure "
                    "identifier. It can be used via a web form or a simple URL API.",
        category="api",
        href="http://cactus.nci.nih.gov/chemical/structure",
        publisher=p2,
        parent=e0
    )
    e1.save()

    e2 = EntryPoint.create(
        name="InChI Trust Root Resolver",
        description="Root InChI Resolver at InChI Trust",
        category="resolver",
        href="http://root.inchi-resolver.org"
    )
    e2.save()

    x1 = EndPoint.create(
        entrypoint=e1,
        category="uritemplate",
        uri="{+stdinchi|+stdinchikey}/smiles",
        description="Standard InChI to SMILES conversion",
        #content_media_type="text/plain",
        request_methods=['GET','POST']
    )
    x1.save()
    x1.accept_header_mediatypes.add(m1)
    x1.content_mediatypes.add(m1)

    x2 = EndPoint.create(
        entrypoint=e1,
        category="uritemplate",
        uri="{+stdinchi,+stdinchikey}/iupac_name",
        description="Standard InChI to IUPAC name conversion",
        #content_media_type="text/plain",
        request_methods=['GET']
    )
    x2.save()
    x2.accept_header_mediatypes.add(m1)
    x2.content_mediatypes.add(m1)

    x3 = EndPoint.create(
        entrypoint=e1,
        category="uritemplate",
        uri="{+stdinchi,+stdinchikey}/image",
        description="InChI to SMILES conversion",
        #content_media_type="image/gif",
        request_methods=['POST', 'GET']
    )
    x3.save()
    x3.accept_header_mediatypes.add(m1)
    x3.content_mediatypes.add(m1,m2)

    x4 = EndPoint.create(
        entrypoint=e1,
        category="uritemplate",
        uri="{+smiles}/stdinchi",
        description="SMILES to stdinchi conversion",
        #content_media_type="text/plain",
    )
    x4.save()
    x4.accept_header_mediatypes.add(m1)
    x4.content_mediatypes.add(m1)

    x5 = EndPoint.create(
        entrypoint=e1,
        category="uritemplate",
        uri="{+smiles}/stdinchikey",
        description="SMILES to stdinchikey conversion",
        #content_media_type="text/plain",
    )
    x5.save()
    x5.accept_header_mediatypes.add(m1)
    x5.content_mediatypes.add(m1)




    for j in range(1, 10):

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
