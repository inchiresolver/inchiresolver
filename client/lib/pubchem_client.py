import requests

class PubchemClient:

    def __init__(self):
        pass

    def fetch_inchi(self, cids):
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


