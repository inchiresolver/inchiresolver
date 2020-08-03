InChI Resolver Protocol
=======================

The InChI Resolver protocol is the specification of a common API protocol format any InChI Resolver instance should adhere to. The goal of using a common InChI Resolver protocol is making web resources which provide information based on/indexed by InChI findable and browsable for an (automated) client system in a systematic manner.

The InChI Resolver protocol is based on the IANA-registered JSON:API v1.0 specification (`<https://jsonapi.org/>`_) as media type format.
JSON:API delineates how clients should request or edit data from a server, and how the server should respond to any requests. A main goal of the specification is to optimize HTTP requests; both in terms of the number of requests and the size of data packages exchanged between clients and servers.

.. code-block:: json


   {
        "key": "test"
    }


InChI Resolver API Resources
----------------------------

InChI Resource
^^^^^^^^^^^^^^

The InChI resource of the InChI Resolver API may provide a browsable index of all InChI structure identifiers
available at this InChI resolver instance. For each InChI instance a related resource link to a web service API
entrypoint resource may be given referring to any service API entrypoints at which the InChI instance is
available.

Organization Resource
^^^^^^^^^^^^^^^^^^^^^

The organization resource of the InChI Resolver API lists all organizations that publish either InChI resolver
API entrypoints known by this InChI resolver instance, or lists any API entrypoints for web services of the
organization that make data accessible by InChI. For each organization related resource either links
to parent or subordinated (children) organization resources or publisher resources at this InChI resolver
instance may be given. A organization resource can be categorized as 'regulatory', 'government', 'academia',
'company', 'vendor', 'research', 'publishing', 'provider', 'public', 'society', 'charity', 'other', or 'none'."

Publisher Resource
^^^^^^^^^^^^^^^^^^

The publisher resource of the InChI Resolver API lists all publishing entities that make InChI related
web service API entrypoints available and are part or member of a organization known by this InChI Resolver
instance. For each publisher resource all parent or subordinated (children) publisher resources, the
organization they belong to, and the entrypoint resources they publish may linked linked. A organization
resource can be categorized as 'entity', 'service', 'network', 'division', 'group', 'person', or 'none'."

Entrypoint Resource
^^^^^^^^^^^^^^^^^^^

The entrypoint resource of the InChI Resolver API lists all entrypoint resources known by this InChI resolver
instance. Each entrypoint resource specifies an URL (attribute 'href') and in combination with related
endpoint resources of the same InChI resolver instance links to  Web service resource that make data
accessible by or about InChI.

There are four entrypoint categories available which classify what type of resource is to be expected
at the specified entrypoint URL. The two first categories 'site' and 'service' are used for entrypoint URLs
which are (usually) pointing to resources or web services that are provided by one of the organizations and
publisher listed by this InChI resolver instance (but are external to the InChI resolver itself). The third
category 'resolver' can be applied for referencing InChI resolver instances  offered elsewhere by other
organizations or publishers. The final category 'self' allows for self-referencing the URL entrypoint of the
current InChI resolver instance which is useful for offering linkage to the publisher and organisation
API resource of this InChI resolver instance.
(1) 'site': a general HTML web page, usually accessed by a HTTP GET request (might be just an entry point with
no content at all)
(2) 'service': a web API, commonly allowing access by the HTTP verbs GET, POST, etc. and returning data using
a specific media type (see 'endpoint' resource).
(3) 'resolver': links to an (external) InChI resolver instance of another organization or publisher
(4) 'self': references the current InChI resolver instance itself (for systematic access of, e.g. the
publisher or organization resource).

Endpoint Resource
^^^^^^^^^^^^^^^^^

The endpoint resource of the InChI Resolver API provides access to all endpoint resources known by this
InChI resolver instance. Each endpoint resource provides an URI (pattern) which, in combination with the
parent entrypoint resource, specifies an URL path pointing to a web resources making data available indexed
by InChI. The type of URI (pattern) can be stated using the "category" attribute which can take the values
'schema', 'uritemplate', and 'documentation'. If 'schema' is specified as value, the endpoint refers to a
schema file (e.g. XSD).  If 'uritemplate' is set as category the uri attribute provides a URL template
according to RFC6570 which allows the description of a range of URIs through variable expansion. If
'documentation' is set for attribute 'category', the URL path points to some kind of human-readable
documentation (e.g. html or pdf file). The exact types of accepted header media types, content media types,
or the schema files how a request has to look like and what kind of schema an endpoint uses for its response
can be specified with the endpoint resource attributes  'acceptHeaderMediaTypes',  'contentMediaTypes',
'requestSchemaEndpoint' or 'responseSchemaEndpoint'. Attribute 'requestMethods' lists all HTTP verbs
(GET, POST, etc.) an endpoint accepts.

Mediatype Resource
^^^^^^^^^^^^^^^^^

The media type resource of the InChI Resolver API provides access of all media types available this InChI
resolver instance.