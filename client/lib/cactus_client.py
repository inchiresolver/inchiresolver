import requests

class CactusClient:

    def __init__(self):
        pass

    def fetch_inchi(self, cids):
        rlist = []
        for cid in cids:
            try:
                print("Requesting %s" % cid)
                url = 'https://cactus.nci.nih.gov/chemical/structure/NCICADD:CID=%s/stdinchi' % cid
                response = requests.get(url)
                print(response.headers)
                string = response.content.decode("utf-8")
                rlist.append((cid, string))
            except Exception as e:
                print(e)
                continue
        return rlist


