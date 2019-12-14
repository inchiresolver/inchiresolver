from os import sys, path, environ
import requests
from requests.auth import HTTPBasicAuth

from jsonapi_client import Session, Filter, ResourceTuple

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
sys.path.append('/home/app')

print(environ)
print(sys.path)

#from client.lib.pubchem_client import PubchemClient



s = Session(environ['INCHI_RESOLVER_HOST'], request_kwargs=dict(auth=HTTPBasicAuth(environ['INCHI_RESOLVER_USER'], environ['INCHI_RESOLVER_PASSWD'])))
print(s)

documents = s.get('inchis')

r = documents.resources[0]

print(documents)

print(r)
print(r.string)
print(r.key)


s.close()




