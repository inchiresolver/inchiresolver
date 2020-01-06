from os import sys, path, environ
import requests
import logging
from requests.auth import HTTPBasicAuth

from jsonapi_client import Session, Filter, ResourceTuple

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
sys.path.append('/home/app')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

print(sys.path)
print(environ)


s = Session(
    environ['INCHI_RESOLVER_HOST'],
    request_kwargs=dict(auth=HTTPBasicAuth(environ['INCHI_RESOLVER_USER'], environ['INCHI_RESOLVER_PASSWD']))
)

documents = s.get('inchis')

r = documents.resources[0]

print(documents)

print(r)
print(r.string)
print(r.key)

s.close()

logger.info("done")




