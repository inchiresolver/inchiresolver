
InChI Resolver Prototype system
===============================

A prototype system of three InChI Resolver APIs has been implemented in order to demonstrate
the interaction of different InChI Resolver instances based on the official protocol:

1) the (InChI Trust) Root InChI Resolver at `<https://root.inchi-resolver.org>`_
2) the PubChem InChI Resolver Instance at `<https://pubchem.inchi-resolver.org>`_
3) the InChI Resolver Instance of the NCI/CADD group, respectively the Chemical Structure Resolver at `<https://cactus.inchi-resolver.org>`_

Although they are currently hosted under the same domain, they are separately running instances of the
InChI Resolver reference implementation (each using their own subdomain).

The following image gives an overview:

.. image:: images/prototype.png


Starting from the root resolver at `<https://root.inchi-resolver.org>`_, the top level of resource objects are listed
as required by the `InChI Resolver Protocol <docs/inchi_resolver_protocol.rst>`_. By following the link to the
*entrypoints* resource (`https://root.inchi-resolver.org/entrypoints <https://root.inchi-resolver.org/entrypoints>`_) all
the three entrypoint resources known by the root resolver are shown:

1. `https://root.inchi-resolver.org/entrypoints/4afa761f-1872-5dcd-9cde-9e38902d9e7d <https://root.inchi-resolver.org/entrypoints/4afa761f-1872-5dcd-9cde-9e38902d9e7d>`_
2. `https://root.inchi-resolver.org/entrypoints/2bbaaa43-34f1-5807-b63d-003b9a4eddad <https://root.inchi-resolver.org/entrypoints/2bbaaa43-34f1-5807-b63d-003b9a4eddad>`_
3. `https://root.inchi-resolver.org/entrypoints/58697b96-0f26-52c3-acbf-99c38b1bd537 <https://root.inchi-resolver.org/entrypoints/58697b96-0f26-52c3-acbf-99c38b1bd537>`_

The first entrypoint object is a self reference allowing the Root InChI Resolver instance to provide information about itself
(e.g. by the available attributes *name*, *description*, *category*, *href*, and *entrypointHref*) as well as some relationship
references, for instance to the publisher resource object (`https://root.inchi-resolver.org/entrypoints/4afa761f-1872-5dcd-9cde-9e38902d9e7d/publisher <https://root.inchi-resolver.org/entrypoints/4afa761f-1872-5dcd-9cde-9e38902d9e7d/publisher>`_).

By following the *children* relationship at the first entrypoint object (see *related* link `https://root.inchi-resolver.org/entrypoints/4afa761f-1872-5dcd-9cde-9e38902d9e7d/children <https://root.inchi-resolver.org/entrypoints/4afa761f-1872-5dcd-9cde-9e38902d9e7d/children>`_
the list of subordinated *entrypoints* is listed which in case of the root resolver are the entrypoint objects of the
other two known resolvers, the PubChem resolver and the Cactus resolver, respectively, and the identical list of entrypoint objects
as above filtered for the first entry, the root resolver itself. If we follow the link to the entrypoint resource object
of the PubChem resolver (link 3 above), this resource object present all information the Root resolver knows about
the PubChem resolver, which is very little. However, if we follow the link provided at the *href* attribute or the
*entrypointHref* attribute, in both cases we change now to PubChem resolver instance (usually running on a domain
somewhere else), and are ending either at the top level resource or the self *entrypoint* resource of the PubChem resolver, respectively.

Needs to be extended but hopefully gives a short glimpse of how things work.





