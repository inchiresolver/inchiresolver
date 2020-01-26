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
        name="Root-Organization",
        abbreviation="ROOT",
        href="http://root.com",
    )
    o1.save()

    o2 = Organization.create(
        name="Child-Organization",
        abbreviation="CHILD",
        href="http://child.com",
        parent=o1
    )
    o2.save()


    p1 = Publisher.create(
        name="Markus Sitzmann",
        group="Sitzmann Group",
        contact="Markus Sitzmann",
        href="http://sitzmann.de",
        organization=o2
    )
    p1.save()

    p2 = Publisher.create(
        name="Test",
        group="Test Group",
        contact="John Doe",
        href="http://test.de",
        organization=o2
    )
    p2.save()

    e1 = EntryPoint.create(
        name="Chemical Identifier Resolver",
        description="The Resolver",
        category="service",
        href="http://cactus.nci.nih.gov/chemical/structure",
        publisher=p1
    )
    e1.save()

    e2 = EntryPoint.create(
        name="Next",
        description="Next Resolver",
        category="service",
        href="http://cactus.nci.nih.gov/next",
        publisher=p1
    )
    e2.save()



    i1 = Inchi.create(
        string="InChI=1S/C2H6O/c1-2-3/h3H,2H2,1H3"
    )
    i1.save()
    i1.entrypoints.add(e1)

    i2 = Inchi.create(
        string="InChI=1S/C6H8O6/c7-1-2(8)5-3(9)4(10)6(11)12-5/h2,5,7-10H,1H2/t2-,5+/m0/s1"
    )
    i2.save()
    i2.entrypoints.add(e1)
    i2.entrypoints.add(e2)

    i3 = Inchi.create(
        string="InChI=1S/C17H19NO3/c1-18-7-6-17-10-3-5-13(20)16(17)21-15-12(19)4-2-9(14(15)17)8-11(10)18/h2-5,10-11,13,16,19-20H,6-8H2,1H3/t10-,11+,13-,16-,17-/m0/s1 "
    )
    i3.save()
    i3.entrypoints.add(e1)


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

