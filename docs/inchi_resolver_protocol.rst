InChI Resolver Protocol
=======================

The InChI Resolver protocol is the specification of a common API protocol format any InChI Resolver instance should adhere to. The goal of using a common InChI Resolver protocol is making web resources which provide information based on/indexed by InChI findable and browsable for an (automated) client system in a systematic manner.

The InChI Resolver protocol is based on the IANA-registered JSON:API v1.0 specification (`<https://jsonapi.org/>`_) as media type format.
JSON:API delineates how clients should request or edit data from a server, and how the server should respond to any requests. A main goal of the specification is to optimize HTTP requests; both in terms of the number of requests and the size of data packages exchanged between clients and servers.
