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

schema = {
    'inchis': {
        'properties': {
            'string': {'type': 'string'},
            'key': {'type': 'string'},
            'version': {'type': 'number'},
            'isStandard': {'type': 'boolean'}
        },
        'required': ['string']
    }
}

session = Session(
    environ['INCHI_RESOLVER_HOST'],
    request_kwargs=dict(auth=HTTPBasicAuth(environ['INCHI_RESOLVER_USER'], environ['INCHI_RESOLVER_PASSWD'])),
    schema=schema
)

i = session.create('inchis')
i.string = "InChI=1S/C19H16O4/c1-12(20)11-15(13-7-3-2-4-8-13)17-18(21)14-9-5-6-10-16(14)23-19(17)22/h2-10,15,22H,11H2,1H3"
i.key = ""
i.version = 1
i.isStandard = False

print(session.is_dirty)

r = i.commit()
print(r)


print(session.is_dirty)



