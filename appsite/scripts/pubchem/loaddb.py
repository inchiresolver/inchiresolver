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
    EndPoint.objects.all().delete()
    MediaType.objects.all().delete()

    client = PubchemClient()

    xml = MediaType.create(
        name="text/xml",
        description="XML"
    )
    xml.save()

    html = MediaType.create(
        name="text/html",
        description="HTML"
    )
    html.save()

    o1 = Organization.create(
        name="U.S. National Institutes of Health",
        abbreviation="NIH",
        href="https://www.nih.gov",
        category="government",
        parent=None
    )
    o1.save()

    o2 = Organization.create(
        name="U.S. National Library of Medicine",
        abbreviation="NLM",
        href="https://www.nlm.nih.gov",
        category="government",
        parent=o1
    )
    o2.save()

    o3 = Organization.create(
        name="U.S. National Center for Biotechnology Information",
        abbreviation="NCBI",
        href="https://www.ncbi.nlm.nih.gov",
        category="government",
        parent=o2
    )
    o3.save()

    p1 = Publisher.create(
        name="PubChem group",
        category="group",
        address="8600 Rockville Pike; Bethesda, MD  20894; USA",
        email="pubchem-help@ncbi.nlm.nih.gov",
        href="https://pubchemdocs.ncbi.nlm.nih.gov/contact",
        organization=o2
    )
    p1.save()

    p2 = Publisher.create(
        name="Evan Bolton",
        parent = p1,
        category="person",
        orcid="https://orcid.org/0000-0002-5959-6190",
        organization=o2
    )
    p2.save()

    re = EntryPoint.create(
        name="InChI Trust Root Resolver",
        description="Root InChI Resolver at InChI Trust",
        category="resolver",
        href="https://root.inchi-resolver.org",
        entrypoint_href="https://root.inchi-resolver.org/_self",
    )
    re.save()

    e0 = EntryPoint.create(
        name="PubChem InChI Resolver",
        description="Demonstration InChI Resolver of the PubChem group",
        category="self",
        href="https://pubchem.inchi-resolver.org",
        entrypoint_href="https://pubchem.inchi-resolver.org/_self",
        publisher=p1,
        parent=re
    )
    e0.save()

    e1 = EntryPoint.create(
        name="PubChem PUG REST site",
        description="PUG (Power User Gateway) site",
        category="site",
        href="https:/pubchem.ncbi.nlm.nih.gov/pug_rest",
        publisher=p1
    )
    e1.save()

    e2 = EntryPoint.create(
        name="PubChem PUG REST",
        description="PUG (Power User Gateway), a web interface for accessing PubChem data and services",
        category="service",
        href="https://pubchem.ncbi.nlm.nih.gov/rest/pug",
        publisher=p1,
        parent=e1,
    )
    e2.save()

    e3 = EntryPoint.create(
        name="PubChem Documentation",
        description="PubChem tutorials and documentation",
        category="site",
        href="https://pubchemdocs.ncbi.nlm.nih.gov",
        publisher=p1,
        parent=e1,
    )
    e3.save()

    x1 = EndPoint.create(
        entrypoint=e3,
        category="documentation",
        uri="pug-rest-tutorial",
        description="Documentation of the PUG REST interface",
        request_methods=['GET']
    )
    x1.save()
    x1.content_media_types.add(html)

    x2 = EndPoint.create(
        entrypoint=e1,
        category="schema",
        uri="pug_rest.xsd",
        description="Schema for PubChem PUG REST response",
        request_methods=['GET']
    )
    x2.save()
    x2.content_media_types.add(xml)

    # x3 = EndPoint.create(
    #     entrypoint=e2,
    #     category="uritemplate",
    #     uri="compound/inchikey/{inchi|inchikey}/cids",
    #     description="resolve InChI or InChIKey to PubChem CID",
    #     response_schema_endpoint=x2,
    #     request_methods=['GET']
    # )
    # x3.save()
    # x3.content_media_types.add(xml)

    x4 = EndPoint.create(
        entrypoint=e2,
        category="uritemplate",
        uri="compound/inchikey/{inchi|inchikey}",
        description="full PubChem compound dataset document for the specified InChI or InChIKey",
        response_schema_endpoint=x2,
        request_methods=['GET']
    )
    x4.save()
    x4.content_media_types.add(xml)

    x5 = EndPoint.create(
        entrypoint=e2,
        category="uritemplate",
        uri="compound/inchikey/{inchi|inchikey}/cids",
        description="resolve InChI or InChIKey to PubChem CID",
        response_schema_endpoint=x2,
        request_methods=['GET']
    )
    x5.save()
    x5.content_media_types.add(xml)

    x6 = EndPoint.create(
        entrypoint=e2,
        category="uritemplate",
        uri="compound/inchikey/{inchi|inchikey}/sids",
        description="resolve InChI or InChIKey to PubChem SID",
        response_schema_endpoint=x2,
        request_methods=['GET']
    )
    x6.save()
    x6.content_media_types.add(xml)


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
                inchi.entrypoints.add(e2)
            except Exception as e:
                print(e)
