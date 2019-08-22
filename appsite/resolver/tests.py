from django.core.exceptions import FieldError
from django.test import TestCase
from rdkit import Chem

from inchi.identifier import InChIKey
from resolver.models import Inchi


class IdentifierTest(TestCase):

    def setUp(self):
        pass

    def test_save_and_retrieve(self):
        inchi = Inchi.create(key="LFQSCWFLJHTTHZ-UHFFFAOYSA-N", string="InChI=1S/C2H6O/c1-2-3/h3H,2H2,1H3")
        inchi.save()

        i = Inchi.objects.first()
        print(i)
        print(i.uid)
        print(i.string)
        self.assertTrue(i.version == 1)
        self.assertTrue(i.is_standard is True)
        self.assertTrue(str(i.uid) == 'bd69d81f-f929-510f-8206-4edb124c187f')
        self.assertTrue(str(i.string) == 'InChI=1S/C2H6O/c1-2-3/h3H,2H2,1H3')
        self.assertTrue(str(i.key) == 'LFQSCWFLJHTTHZ-UHFFFAOYSA-N')
        self.assertTrue(str(i.block1) == 'LFQSCWFLJHTTHZ')
        self.assertTrue(str(i.block2) == 'UHFFFAOYSA')
        self.assertTrue(str(i.block3) == 'N')

    def test_url_prefix_save_and_retrieve(self):
        inchi = Inchi.create(key="LFQSCWFLJHTTHZ-UHFFFAOYSA-N", string="InChI=1S/C2H6O/c1-2-3/h3H,2H2,1H3", url_prefix="http://prototype0.inchi-resolver.org/inchis")
        inchi.save()

        i = Inchi.objects.first()
        print(i)
        print(i.uid)
        print(i.string)
        self.assertTrue(i.version == 1)
        self.assertTrue(i.is_standard is True)
        self.assertTrue(str(i.uid) == 'dbb42944-42fc-5131-9b98-ed020daeab7f')
        self.assertTrue(str(i.string) == 'InChI=1S/C2H6O/c1-2-3/h3H,2H2,1H3')
        self.assertTrue(str(i.key) == 'LFQSCWFLJHTTHZ-UHFFFAOYSA-N')
        self.assertTrue(str(i.block1) == 'LFQSCWFLJHTTHZ')
        self.assertTrue(str(i.block2) == 'UHFFFAOYSA')
        self.assertTrue(str(i.block3) == 'N')


    def test_only_inchi(self):
        inchi = Inchi.create(string="InChI=1S/C2H6O/c1-2-3/h3H,2H2,1H3", url_prefix="http://prototype0.inchi-resolver.org/inchis")
        inchi.save()

        i = Inchi.objects.first()
        print(i)
        print(i.uid)
        print(i.string)
        self.assertTrue(i.version == 1)
        self.assertTrue(i.is_standard is True)
        self.assertTrue(str(i.uid) == 'dbb42944-42fc-5131-9b98-ed020daeab7f')
        self.assertTrue(str(i.string) == 'InChI=1S/C2H6O/c1-2-3/h3H,2H2,1H3')
        self.assertTrue(str(i.key) == 'LFQSCWFLJHTTHZ-UHFFFAOYSA-N')
        self.assertTrue(str(i.block1) == 'LFQSCWFLJHTTHZ')
        self.assertTrue(str(i.block2) == 'UHFFFAOYSA')
        self.assertTrue(str(i.block3) == 'N')


    def test_only_inchikey(self):
        inchi = Inchi.create(key="LFQSCWFLJHTTHZ-UHFFFAOYSA-N", url_prefix="http://prototype0.inchi-resolver.org/inchis")
        inchi.save()

        i = Inchi.objects.first()
        print(i)
        print(i.uid)
        print(i.string)
        self.assertTrue(i.version == 1)
        self.assertTrue(i.is_standard is True)
        self.assertTrue(str(i.uid) == 'dbb42944-42fc-5131-9b98-ed020daeab7f')
        self.assertTrue(i.string is None)
        self.assertTrue(str(i.key) == 'LFQSCWFLJHTTHZ-UHFFFAOYSA-N')
        self.assertTrue(str(i.block1) == 'LFQSCWFLJHTTHZ')
        self.assertTrue(str(i.block2) == 'UHFFFAOYSA')
        self.assertTrue(str(i.block3) == 'N')


    def test_save_multiple(self):

        inchi = Inchi.create(key="LFQSCWFLJHTTHZ-UHFFFAOYSA-N")
        inchi.save()

        inchi2 = Inchi.create(key="LFQSCWFLJHTTHZ-UHFFFAOYSA-N")
        inchi2.save()

        inchi3 = Inchi.create(string='InChI=1S/C2H6O/c1-2-3/h3H,2H2,1H3')
        inchi3.save()

        self.assertTrue(Inchi.objects.count(), 1)


    def test5(self):
        with self.assertRaises(FieldError):
            Inchi.create(key="LFQSCWFLJHTTZZ-UHFFFAOYSA-N", string="InChI=1S/C2H6O/c1-2-3/h3H,2H2,1H3")
