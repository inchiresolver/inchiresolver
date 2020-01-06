from os import sys, path, environ
import requests

#if __name__ == '__main__' and __package__ is None:
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

print(sys.path)
print(environ)


from client.lib.pubchem_client import PubchemClient


client = PubchemClient()

for j in range(2, 3):

    ilist = client.fetch_inchi_for_pubchem_cid(range(j * 10, j * 10 + 10))

    for cid, i in ilist:
        print("Posting: %s" % (i,))
        r = requests.post(environ['INCHI_RESOLVER_HOST'], data={'string': i},
                          auth=(environ['INCHI_RESOLVER_USER'], environ['INCHI_RESOLVER_PASSWD']))
        r.raise_for_status()
        print
        print("Status %s" % (r.status_code))



