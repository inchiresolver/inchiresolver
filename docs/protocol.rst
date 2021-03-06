InChI Resolver Protocol
=======================

:Version: 0.3.3 of 2021-04-21
:Authors:
    Markus Sitzmann

The InChI Resolver Protocol is the specification of a common API protocol format which any InChI Resolver instance
should adhere to. By following the shared conventions of the protocol, any InChI-based web resources and services
should be findable and browsable for an (automated) client system in a systematic, predefined manner.

The InChI Resolver protocol is based on the IANA-registered JSON:API v1.0 specification (`<https://jsonapi.org/>`_)
as media type format. JSON:API has been specified on basis of `JSON schema <https://json-schema.org/>`_ and delineates
how clients should request or edit data from a server, and how the server should respond to any requests. The format
is optimized for HTTP requests to a web API; both in terms of the number of requests and the size of data packages
exchanged between clients and servers.

A first draft of a InChI Resolver Protocol schema specification is available here:
`InChI Resolver Protocol Schema File <https://github.com/inchiresolver/inchiresolver/blob/master/schema/2021-04b1/schema.json>`_.
It is an extension to the JSON:API specification and limits the usage of this specification to resources
permissible to the InChI Resolver Protocol. The available InChI Resolver API resources are described in the following.

InChI Resolver API Resources
----------------------------

The root entry point or top level of a InChI Resolver instance has to be accessible at a valid, absolute URL path.
Starting from there, a InChI Resolver instance should reply to any requests by fully supporting the JSON:API media type
`application/vnd.api+json <https://jsonapi.org/>`_ and any responses may adhere to the
`InChI Resolver Protocol Schema <https://github.com/inchiresolver/inchiresolver/blob/master/schema/2021-04b1/schema.json>`_.

At the current level of implementation of the InChI Resolver Protocol, the following top level resource objects have to
be made accessible (although some of them might be empty for a specific InChI Resolver instance):

- **inchis** (browsable index of all available InChI instances at this InChI resolver instance)
- **organizations** (list of any organizations known by this InChI resolver instance publishing InChI related data)
- **publishers** (list of any publishers known by this InChI resolver instance publishing InChI related entry points [see next point])
- **entrypoints** (list of all web resource entry points known by this InChI resolver instance providing InChI related web resource end points [see next point])
- **endpoints** (list of any web resource/schema/documentation end points known by this InChI resolver instance providing data with or about InChI)
- **mediatypes** (list of any media types listed by end point resources at this InChI resolver instance)

**Example**: `PubChem Demonstration InChI Resolver [Top level at https://pubchem.inchi-resolver.org/] <https://pubchem.inchi-resolver.org/>`_

.. code-block:: json

   {
        "data": {
            "inchis": "https://pubchem.inchi-resolver.org/inchis",
            "organizations": "https://pubchem.inchi-resolver.org/organizations",
            "publishers": "https://pubchem.inchi-resolver.org/publishers",
            "entrypoints": "https://pubchem.inchi-resolver.org/entrypoints",
            "endpoints": "https://pubchem.inchi-resolver.org/endpoints",
            "mediatypes": "https://pubchem.inchi-resolver.org/mediatypes"
        }
    }

**Note**: For future versions of the InChI Resolver Protocol the following top level resource objects are planned to
be included:

- **structures** (list of structure representations linked to a specific InChI at the InChI resource of a InChI resolver instance)
- **rinchi** (browsable index of all RInChI instances available at a InChI resolver instance)
- **reactions** (list of reaction representations linked to a specific InChI at the InChI resource of a InChI resolver instance)

InChI Resource
^^^^^^^^^^^^^^

The InChI resource of the InChI Resolver API may provide a browsable index of all InChI structure identifiers available
at this InChI resolver instance. For each InChI instance a related resource link to a `entrypoint resource`_ may be
given, referring to any service API entrypoints at which the InChI instance is available.

The current prototype implementation of the resolver accepts InChI strings as input and creates the corresponding
InChIKey, version number and whether the InChI is a Standard InChI or not. The safeOptions used for the creation
of the original InChI can be added.

Example: `PubChem Demonstration InChI Resolver [InChI instance object https://pubchem.inchi-resolver.org/inchis/36d8eb2e-aa7e-5c6e-8961-d9e8ead14f92] <https://pubchem.inchi-resolver.org/inchis/36d8eb2e-aa7e-5c6e-8961-d9e8ead14f92>`_

.. code-block:: json

     {
        "type": "inchis",
        "id": "36d8eb2e-aa7e-5c6e-8961-d9e8ead14f92",
        "attributes": {
            "string": "InChI=1S/C20H21N7O6/c21-20-24-16-15(18(31)25-20)27-9-26(8-12(27)7-22-16)11-3-1-10(2-4-11)17(30)23-13(19(32)33)5-6-14(28)29/h1-4,9,12-13H,5-8H2,(H6-,21,22,23,24,25,28,29,30,31,32,33)/p+1",
            "key": "MEANFMOQMXYMCT-UHFFFAOYSA-O",
            "version": 1,
            "isStandard": true,
            "safeOptions": null
        },
        "relationships": {
            "entrypoints": {
                "meta": {
                    "count": 1
                },
                "data": [
                    {
                        "type": "entrypoints",
                        "id": "aa5da239-0fe8-5f0e-a1f5-ee83b42e7386"
                    }
                ],
                "links": {
                    "self": "https://pubchem.inchi-resolver.org/inchis/36d8eb2e-aa7e-5c6e-8961-d9e8ead14f92/relationships/entrypoints",
                    "related": "https://pubchem.inchi-resolver.org/inchis/36d8eb2e-aa7e-5c6e-8961-d9e8ead14f92/entrypoints"
                }
            }
        },
        "links": {
            "self": "https://pubchem.inchi-resolver.org/inchis/36d8eb2e-aa7e-5c6e-8961-d9e8ead14f92"
        },
        "meta": {
            "added": "2020-08-02T23:35:38.738353Z",
            "modified": "2020-08-02T23:35:38.738367Z"
        }
    }

.. _organization resources:
.. _organization:

Organization Resource
^^^^^^^^^^^^^^^^^^^^^

The organization resource of the InChI Resolver API may list all organizations which either publish other InChI resolver
API entrypoints known by this InChI resolver instance or make any web services API entrypoints available providing data
based on InChI also known by this InChI resolver instance. For each organization resource either links to related parent
or subordinated (children) organization resources, and `publisher resources`_  at this InChI
resolver instance may be provided. A organization resource can be categorized as *regulatory*, *government*, *academia*,
*company*, *vendor*, *research*, *publishing*, *provider*, *public*, *society*, *charity*, *other*, or *none*.

**Example**: `PubChem Demonstration InChI Resolver [Organization instance object https://pubchem.inchi-resolver.org/organizations/904a3dfd-7417-5e2a-ac98-377501d0ff9b] <https://pubchem.inchi-resolver.org/organizations/904a3dfd-7417-5e2a-ac98-377501d0ff9b>`_

.. code-block:: json

    {
        "type": "organizations",
        "id": "904a3dfd-7417-5e2a-ac98-377501d0ff9b",
        "attributes": {
            "name": "U.S. National Library of Medicine",
            "abbreviation": "NLM",
            "category": "government",
            "href": "https://www.nlm.nih.gov"
        },
        "relationships": {
            "parent": {
                "links": {
                    "self": "https://pubchem.inchi-resolver.org/organizations/904a3dfd-7417-5e2a-ac98-377501d0ff9b/relationships/parent",
                    "related": "https://pubchem.inchi-resolver.org/organizations/904a3dfd-7417-5e2a-ac98-377501d0ff9b/parent"
                },
                "data": {
                    "type": "organizations",
                    "id": "6ca138a9-6b7e-5752-b6df-99df6971c445"
                }
            },
            "children": {
                "meta": {
                    "count": 1
                },
                "data": [
                    {
                        "type": "organizations",
                        "id": "247ed733-8fe0-5a9f-bb26-c43acc0dd8c6"
                    }
                ],
                "links": {
                    "self": "https://pubchem.inchi-resolver.org/organizations/904a3dfd-7417-5e2a-ac98-377501d0ff9b/relationships/children",
                    "related": "https://pubchem.inchi-resolver.org/organizations/904a3dfd-7417-5e2a-ac98-377501d0ff9b/children"
                }
            },
            "publishers": {
                "meta": {
                    "count": 2
                },
                "data": [
                    {
                        "type": "publishers",
                        "id": "baa3343a-111d-5893-9870-d78af85776c6"
                    },
                    {
                        "type": "publishers",
                        "id": "fabfce20-45e2-5092-890b-b24ac7581cdd"
                    }
                ],
                "links": {
                    "self": "https://pubchem.inchi-resolver.org/organizations/904a3dfd-7417-5e2a-ac98-377501d0ff9b/relationships/publishers",
                    "related": "https://pubchem.inchi-resolver.org/organizations/904a3dfd-7417-5e2a-ac98-377501d0ff9b/publishers"
                }
            }
        },
        "links": {
            "self": "https://pubchem.inchi-resolver.org/organizations/904a3dfd-7417-5e2a-ac98-377501d0ff9b"
        },
        "meta": {
            "added": "2020-08-02T23:33:13.057681Z",
            "modified": "2020-08-02T23:33:13.057694Z"
        }
    }

.. _publisher resources:

Publisher Resource
^^^^^^^^^^^^^^^^^^

The publisher resource of the InChI Resolver API lists all publishing entities that make InChI related
web service API entrypoints available propagated by this InChI resolver instance, and are part or member of a
organization also known by this InChI Resolver instance. For each publisher resource all parent or subordinated
(children) publisher resources, the `organization`_ they belong to, and the `entrypoint resources`_ they publish may be
linked. A organization resource can be categorized as *entity*, *service*, *network*, *division*, *group*, *person*,
or *none*.

**Example**: `PubChem Demonstration InChI Resolver [Publisher instance object https://pubchem.inchi-resolver.org/publishers/fabfce20-45e2-5092-890b-b24ac7581cdd] <https://pubchem.inchi-resolver.org/publishers/fabfce20-45e2-5092-890b-b24ac7581cdd>`_

.. code-block:: json

    {
        "type": "publishers",
        "id": "fabfce20-45e2-5092-890b-b24ac7581cdd",
        "attributes": {
            "name": "PubChem group",
            "category": "group",
            "email": "pubchem-help@ncbi.nlm.nih.gov",
            "address": "8600 Rockville Pike; Bethesda, MD  20894; USA",
            "href": "https://pubchemdocs.ncbi.nlm.nih.gov/contact",
            "orcid": null
        },
        "relationships": {
            "parent": {
                "links": {
                    "self": "https://pubchem.inchi-resolver.org/publishers/fabfce20-45e2-5092-890b-b24ac7581cdd/relationships/parent",
                    "related": "https://pubchem.inchi-resolver.org/publishers/fabfce20-45e2-5092-890b-b24ac7581cdd/parent"
                },
                "data": null
            },
            "children": {
                "meta": {
                    "count": 1
                },
                "data": [
                    {
                        "type": "publishers",
                        "id": "baa3343a-111d-5893-9870-d78af85776c6"
                    }
                ],
                "links": {
                    "self": "https://pubchem.inchi-resolver.org/publishers/fabfce20-45e2-5092-890b-b24ac7581cdd/relationships/children",
                    "related": "https://pubchem.inchi-resolver.org/publishers/fabfce20-45e2-5092-890b-b24ac7581cdd/children"
                }
            },
            "organization": {
                "links": {
                    "self": "https://pubchem.inchi-resolver.org/publishers/fabfce20-45e2-5092-890b-b24ac7581cdd/relationships/organization",
                    "related": "https://pubchem.inchi-resolver.org/publishers/fabfce20-45e2-5092-890b-b24ac7581cdd/organization"
                },
                "data": {
                    "type": "organizations",
                    "id": "904a3dfd-7417-5e2a-ac98-377501d0ff9b"
                }
            },
            "entrypoints": {
                "meta": {
                    "count": 4
                },
                "data": [
                    {
                        "type": "entrypoints",
                        "id": "2d7c119f-561d-5da1-99b6-18494a780da5"
                    },
                    {
                        "type": "entrypoints",
                        "id": "3328eb7b-4fe3-5d1e-a182-2fc246aaed68"
                    },
                    {
                        "type": "entrypoints",
                        "id": "aa5da239-0fe8-5f0e-a1f5-ee83b42e7386"
                    },
                    {
                        "type": "entrypoints",
                        "id": "a1e74f8e-6ba5-571d-b5a6-2f22bfaa89c8"
                    }
                ],
                "links": {
                    "self": "https://pubchem.inchi-resolver.org/publishers/fabfce20-45e2-5092-890b-b24ac7581cdd/relationships/entrypoints",
                    "related": "https://pubchem.inchi-resolver.org/publishers/fabfce20-45e2-5092-890b-b24ac7581cdd/entrypoints"
                }
            }
        },
        "links": {
            "self": "https://pubchem.inchi-resolver.org/publishers/fabfce20-45e2-5092-890b-b24ac7581cdd"
        },
        "meta": {
            "added": "2020-08-02T23:33:13.062385Z",
            "modified": "2020-08-02T23:33:13.062398Z"
        }
    }

.. _publisher resource:
.. _entrypoint resources:

Entrypoint Resource
^^^^^^^^^^^^^^^^^^^

The entrypoint resource of the InChI Resolver API lists all entrypoint resources known by this InChI resolver
instance. Each entrypoint resource specifies an URL (attribute *href*) which, in combination with related
`endpoint resources`_ of the this InChI resolver instance, links to any Web service resources that should be
propagated by this InChI resolver instance.

There are four entrypoint categories available which classify what type of resource is to be expected
at the specified entrypoint URL. The first two categories, *site* and *service*, are used for entrypoint URLs
which are (usually) pointing to resources or services at the Web that are provided by one of the organizations and
publishers listed by this InChI resolver instance (but are external to the InChI resolver itself). The third
category *resolver* can be applied for referencing InChI resolver instances published elsewhere on the Web by another
organization or publisher. The final category, *self*, allows for self-referencing the URL entrypoint of the
current InChI resolver instance which is useful for referencing the publisher and organisation
API resource of this InChI resolver instance.

**Entrypoint Category Overview:**

1) *Site*: a general HTML web page, usually accessed by a HTTP GET request used for InChI related information or documentation of services (might be just an entry point with no content at all). Example: `link to the PubChem Documentation site <https://pubchem.inchi-resolver.org/entrypoints/a1e74f8e-6ba5-571d-b5a6-2f22bfaa89c8>`_
2) *Service*: a web API, commonly allowing access by the HTTP verbs GET, POST, etc. and returning data using a specific media type (see 'endpoint' resource). Example: `the entry point to the PubChem PUG (Power User Gateway) service <https://pubchem.inchi-resolver.org/entrypoints/aa5da239-0fe8-5f0e-a1f5-ee83b42e7386>`_
3) *Resolver*: links to an (external) InChI resolver instance of another organization or publisher. If this category is used, also the attribute *entrypointHref* should be set providing a direct link to the the *self* entrypoint of the referenced InChI resolver instance. A recommendation for the format of this link is [external InChI resolver URL]/_self is suggested which should be supported by any InChI resolver instance as a reference to the own (self) entrypoint. Example: `the PubChem Demonstration InChI Resolver references the InChI Trust Root Resolver <https://pubchem.inchi-resolver.org/entrypoints/42626518-a53d-56d5-8556-8efc586ed14f>`_
4) *Self*: references the current InChI resolver instance itself (for systematic access of, e.g. the publisher or organization resource). If this category is used, also the attribute *entrypointHref* should be set providing a direct link to the the *self* entrypoint of the referenced InChI resolver instance. Example: `self reference to the entrypoint of the PubChem resolver <https://pubchem.inchi-resolver.org/entrypoints/2d7c119f-561d-5da1-99b6-18494a780da5>`_

**Example**: `PubChem Demonstration InChI Resolver [Entrypoint instance object https://pubchem.inchi-resolver.org/entrypoints/aa5da239-0fe8-5f0e-a1f5-ee83b42e7386] <https://pubchem.inchi-resolver.org/entrypoints/aa5da239-0fe8-5f0e-a1f5-ee83b42e7386>`_

.. code-block:: json

    {
        "type": "entrypoints",
        "id": "aa5da239-0fe8-5f0e-a1f5-ee83b42e7386",
        "attributes": {
            "name": "PubChem PUG REST",
            "description": "PUG (Power User Gateway), a web interface for accessing PubChem data and services",
            "category": "service",
            "href": "https://pubchem.ncbi.nlm.nih.gov/rest/pug",
            "entrypointHref": null
        },
        "relationships": {
            "parent": {
                "links": {
                    "self": "https://pubchem.inchi-resolver.org/entrypoints/aa5da239-0fe8-5f0e-a1f5-ee83b42e7386/relationships/parent",
                    "related": "https://pubchem.inchi-resolver.org/entrypoints/aa5da239-0fe8-5f0e-a1f5-ee83b42e7386/parent"
                },
                "data": {
                    "type": "entrypoints",
                    "id": "3328eb7b-4fe3-5d1e-a182-2fc246aaed68"
                }
            },
            "children": {
                "meta": {
                    "count": 0
                },
                "data": [],
                "links": {
                    "self": "https://pubchem.inchi-resolver.org/entrypoints/aa5da239-0fe8-5f0e-a1f5-ee83b42e7386/relationships/children",
                    "related": "https://pubchem.inchi-resolver.org/entrypoints/aa5da239-0fe8-5f0e-a1f5-ee83b42e7386/children"
                }
            },
            "publisher": {
                "links": {
                    "self": "https://pubchem.inchi-resolver.org/entrypoints/aa5da239-0fe8-5f0e-a1f5-ee83b42e7386/relationships/publisher",
                    "related": "https://pubchem.inchi-resolver.org/entrypoints/aa5da239-0fe8-5f0e-a1f5-ee83b42e7386/publisher"
                },
                "data": {
                    "type": "publishers",
                    "id": "fabfce20-45e2-5092-890b-b24ac7581cdd"
                }
            },
            "endpoints": {
                "meta": {
                    "count": 3
                },
                "data": [
                    {
                        "type": "endpoints",
                        "id": "54d8f3a6-e0d1-5968-aef0-0e97a73597ac"
                    },
                    {
                        "type": "endpoints",
                        "id": "51369fbe-1933-5450-8a5e-0ca5b9924204"
                    },
                    {
                        "type": "endpoints",
                        "id": "f6fd1b92-271e-5974-a4f9-c729a63090a1"
                    }
                ],
                "links": {
                    "self": "https://pubchem.inchi-resolver.org/entrypoints/aa5da239-0fe8-5f0e-a1f5-ee83b42e7386/relationships/endpoints",
                    "related": "https://pubchem.inchi-resolver.org/entrypoints/aa5da239-0fe8-5f0e-a1f5-ee83b42e7386/endpoints"
                }
            }
        },
        "links": {
            "self": "https://pubchem.inchi-resolver.org/entrypoints/aa5da239-0fe8-5f0e-a1f5-ee83b42e7386"
        },
        "meta": {
            "added": "2020-08-02T23:33:13.072821Z",
            "modified": "2020-08-02T23:33:13.072834Z"
        }
    }

.. _endpoint resources:

Endpoint Resource
^^^^^^^^^^^^^^^^^

The endpoint resource of the InChI Resolver API provides access to all endpoint resources known by this
InChI resolver instance. Each endpoint resource provides an URI (pattern) which, in combination with the
parent `entrypoint resource`_, specifies an URL path pointing to a web resources making data available indexed
by InChI. The type of URI (pattern) can be stated using the "category" attribute which can take the values
*schema*, *uritemplate*, and *documentation*. If *schema* is specified as value, the endpoint refers to a
schema file (e.g. XSD).  If *uritemplate* is set as category the uri attribute provides a URL template
according to RFC6570 which allows the description of a range of URIs through variable expansion. If
*documentation* is set for attribute *category*, the URL path points to some kind of human-readable
documentation (e.g. html or pdf file). The exact types of accepted header media types, content media types,
or the schema files how a request has to look like and what kind of schema an endpoint uses for its response
can be specified with the endpoint resource attributes  *acceptHeaderMediaTypes*,  *contentMediaTypes*,
*requestSchemaEndpoint* or *responseSchemaEndpoint*. Attribute *requestMethods* lists all HTTP verbs
(GET, POST, etc.) the corresponding endpoint will accept.

**Example**: `PubChem Demonstration InChI Resolver [Endpoint instance object https://pubchem.inchi-resolver.org/endpoints/51369fbe-1933-5450-8a5e-0ca5b9924204] <https://pubchem.inchi-resolver.org/endpoints/51369fbe-1933-5450-8a5e-0ca5b9924204>`_

.. code-block:: json

    {
        "type": "endpoints",
        "id": "51369fbe-1933-5450-8a5e-0ca5b9924204",
        "attributes": {
            "uri": "compound/inchikey/{inchi|inchikey}/cids",
            "fullPathUri": "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/inchikey/{inchi|inchikey}/cids",
            "description": "resolve InChI or InChIKey to PubChem CID",
            "category": "uritemplate",
            "requestMethods": [
                "GET"
            ]
        },
        "relationships": {
            "entrypoint": {
                "data": {
                    "type": "entrypoints",
                    "id": "aa5da239-0fe8-5f0e-a1f5-ee83b42e7386"
                },
                "links": {
                    "related": "https://pubchem.inchi-resolver.org/entrypoints/aa5da239-0fe8-5f0e-a1f5-ee83b42e7386"
                }
            },
            "acceptHeaderMediaTypes": {
                "meta": {
                    "count": 0
                },
                "data": [],
                "links": {
                    "self": "https://pubchem.inchi-resolver.org/endpoints/51369fbe-1933-5450-8a5e-0ca5b9924204/relationships/accept_header_media_types",
                    "related": "https://pubchem.inchi-resolver.org/endpoints/51369fbe-1933-5450-8a5e-0ca5b9924204/accept_header_media_types"
                }
            },
            "contentMediaTypes": {
                "meta": {
                    "count": 1
                },
                "data": [
                    {
                        "type": "mediatypes",
                        "id": "b28c3aeb-48ba-5b77-b26a-48aead52892d"
                    }
                ],
                "links": {
                    "self": "https://pubchem.inchi-resolver.org/endpoints/51369fbe-1933-5450-8a5e-0ca5b9924204/relationships/content_media_types",
                    "related": "https://pubchem.inchi-resolver.org/endpoints/51369fbe-1933-5450-8a5e-0ca5b9924204/content_media_types"
                }
            },
            "requestSchemaEndpoint": {
                "links": {
                    "self": "https://pubchem.inchi-resolver.org/endpoints/51369fbe-1933-5450-8a5e-0ca5b9924204/relationships/request_schema_endpoint",
                    "related": "https://pubchem.inchi-resolver.org/endpoints/51369fbe-1933-5450-8a5e-0ca5b9924204/request_schema_endpoint"
                },
                "data": null
            },
            "responseSchemaEndpoint": {
                "links": {
                    "self": "https://pubchem.inchi-resolver.org/endpoints/51369fbe-1933-5450-8a5e-0ca5b9924204/relationships/response_schema_endpoint",
                    "related": "https://pubchem.inchi-resolver.org/endpoints/51369fbe-1933-5450-8a5e-0ca5b9924204/response_schema_endpoint"
                },
                "data": {
                    "type": "endpoints",
                    "id": "4cca274b-fb36-5fbb-b905-3728f0686d6c"
                }
            }
        },
        "links": {
            "self": "https://pubchem.inchi-resolver.org/endpoints/51369fbe-1933-5450-8a5e-0ca5b9924204"
        },
        "meta": {
            "added": "2020-08-02T23:33:13.090024Z",
            "modified": "2020-08-02T23:33:13.090038Z"
        }
   }

Mediatype Resource
^^^^^^^^^^^^^^^^^^

The media type resource of the InChI Resolver API provides access of all media types available this InChI
resolver instance.

**Example**: `PubChem Demonstration InChI Resolver [Mediatype instance object https://pubchem.inchi-resolver.org/mediatypes/b28c3aeb-48ba-5b77-b26a-48aead52892d] <https://pubchem.inchi-resolver.org/mediatypes/b28c3aeb-48ba-5b77-b26a-48aead52892d>`_

.. code-block:: json


    {
        "type": "mediatypes",
        "id": "b28c3aeb-48ba-5b77-b26a-48aead52892d",
        "attributes": {
            "name": "text/xml",
            "description": "XML"
        },
        "relationships": {
            "acceptingEndpoints": {
                "meta": {
                    "count": 0
                },
                "data": [],
                "links": {
                    "self": "https://pubchem.inchi-resolver.org/mediatypes/b28c3aeb-48ba-5b77-b26a-48aead52892d/relationships/accepting_endpoints",
                    "related": "https://pubchem.inchi-resolver.org/mediatypes/b28c3aeb-48ba-5b77-b26a-48aead52892d/accepting_endpoints"
                }
            },
            "deliveringEndpoints": {
                "meta": {
                    "count": 4
                },
                "data": [
                    {
                        "type": "endpoints",
                        "id": "4cca274b-fb36-5fbb-b905-3728f0686d6c"
                    },
                    {
                        "type": "endpoints",
                        "id": "54d8f3a6-e0d1-5968-aef0-0e97a73597ac"
                    },
                    {
                        "type": "endpoints",
                        "id": "51369fbe-1933-5450-8a5e-0ca5b9924204"
                    },
                    {
                        "type": "endpoints",
                        "id": "f6fd1b92-271e-5974-a4f9-c729a63090a1"
                    }
                ],
                "links": {
                    "self": "https://pubchem.inchi-resolver.org/mediatypes/b28c3aeb-48ba-5b77-b26a-48aead52892d/relationships/delivering_endpoints",
                    "related": "https://pubchem.inchi-resolver.org/mediatypes/b28c3aeb-48ba-5b77-b26a-48aead52892d/delivering_endpoints"
                }
            }
        },
        "links": {
            "self": "https://pubchem.inchi-resolver.org/mediatypes/b28c3aeb-48ba-5b77-b26a-48aead52892d"
        },
        "meta": {
            "added": "2020-08-02T23:33:13.047167Z",
            "modified": "2020-08-02T23:33:13.047183Z"
        }
    }
