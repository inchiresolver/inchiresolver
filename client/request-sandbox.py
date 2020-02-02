from os import sys, path, environ
import urllib
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

logger.info(">>> %s", environ['INCHI_RESOLVER_HOST'])

response = requests.get(environ['INCHI_RESOLVER_HOST'],
                          auth=(environ['INCHI_RESOLVER_USER'], environ['INCHI_RESOLVER_PASSWD']))

logger.info("STATUS  %s", response.status_code)
logger.info("CONTENT %s", response.content)
logger.info("HEADERS %s", response.headers)
logger.info("done")




