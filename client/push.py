from os import sys, path, environ
import requests

#if __name__ == '__main__' and __package__ is None:
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

print(sys.path)

print(environ)


from client.lib.pubchem_client import PubchemClient


client = PubchemClient()

for j in range(1, 2):

    ilist = client.fetch_inchi_for_pubchem_cid(range(j * 10, j * 10 + 10))

    #print(ilist)
    #data = [{'string': i} for cid, i in ilist]
    #print(data)

    for cid, i in ilist:
        r = requests.post(environ['INCHI_RESOLVER_HOST'], data={'string': i},
                          auth=(environ['INCHI_RESOLVER_USER'], environ['INCHI_RESOLVER_PASSWD']))



