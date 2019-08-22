
from django.test import TestCase


# Create your tests here.
from inchi.identifier import InChI

class InChITest(TestCase):

    def test1(self):
        s = "InChI=1S/C2H6O/c1-2-3/h3H,2H2,1H3"
        inchi = InChI(s)
        print(inchi)
        print(inchi.element['well_formatted'])
        print(inchi.element['is_standard'])
        print(inchi.element['version'])
