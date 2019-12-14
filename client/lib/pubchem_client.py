import requests

class PubchemClient:

    def __init__(self):
        pass

    def fetch_inchi_for_pubchem_cid(self, cids):
        rlist = []
        for cid in cids:
            try:
                print("Requesting %s" % cid)
                url = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/%s/property/InChI/txt' % cid
                response = requests.get(url)
                print(response.headers)
                string = response.content.decode("utf-8")
                rlist.append((cid, string))
            except Exception as e:
                print(e)
                continue
        return rlist


# if __name__== '__main__':
#     c = PubchemClient()
#     ilist = c.fetch_inchi_for_pubchem_cid(range(1, 1000))
#
#     data = [{'string': i} for cid, i in ilist]
#
#     for cid, i in ilist:
#
#         r = requests.post("http://inchiresolver.localhost/inchis/", data={'string': i}, auth=('djangoadmin', 'djangoDJANGO'))
#
#         print(r)
#         f = open('out.html', 'w')
#         f.write(r.content.decode("utf-8"))
#         print('end')
