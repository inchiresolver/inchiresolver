from os import sys, path, environ
import urllib
import requests
import json
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


def log(response, label=None):
    if label:
        logger.info("------------  %s ------------ ", label)
    logger.info("CONTENT %s", response.content)
    logger.info("HEADERS %s", response.headers)
    logger.info("> STATUS  %s", response.status_code)




host = environ['INCHI_RESOLVER_HOST']
user = environ['INCHI_RESOLVER_USER']
passwd = environ['INCHI_RESOLVER_PASSWD']
auth = (user, passwd)

headers = {'Content-type': 'application/vnd.api+json', 'Accept': 'application/vnd.api+json'}

response = requests.get(host, auth=auth)
log(response, "get root")

organization = json.dumps(
{"data":
    {
        "type": "organizations",
        "attributes": {
            "name": "InChI Trust",
            "abbreviation": "InChI Trust",
            "href": "https://inchi-trust.org",
        }
    }
})

response = requests.post(host + "/organizations", auth=auth, headers=headers, data=organization)
log(response, "Post organization")
organization = json.loads(response.text)

oid = organization['data']['id']
logger.info("ORGANIZATION %s : %s", organization, oid)


publisher = json.dumps(
{"data":
    {
        "type": "publishers",
        "attributes": {
            "name": "Markus Sitzmann",
            "group": "Chembience Group",
            "contact": "markus.sitzmann@gmail.com",
            "href": "https://chembience.com",
        },
        "relationships": {
            "parent": {
                "data": None
            },
            "organization": {
                "data": {
                    "type": "organizations",
                    "id": oid
                }
            }
        }
    }
})

response = requests.post(host + "/publishers", auth=auth, headers=headers, data=publisher)
log(response, "Post publisher")
publisher = json.loads(response.text)


#response = requests.delete(host + "/organizations/" + oid, auth=auth, headers=headers)
#log(response, "Delete organization")

