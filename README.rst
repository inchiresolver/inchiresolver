InChI Resolver 
==============

.. image:: https://circleci.com/gh/chembience/chembience-inchiresolver/tree/master.svg?style=shield
    :target: https://circleci.com/gh/chembience/chembience-inchiresolver/tree/master

.. image:: https://img.shields.io/github/release/inchiresolver/inchiresolver.svg
   :target: https://img.shields.io/github/release/inchiresolver/inchiresolver.svg

.. image:: https://img.shields.io/github/license/inchiresolver/inchiresolver.svg
   :target: https://img.shields.io/github/license/inchiresolver/inchiresolver.svg


Repository of the InChI Resolver project. The goal of this project is to provide the implementation of an InChI resolver prototype as well as the the specifiation of a common InChI Resolver API protocol which allows a client communicating with any InChI Resolver instance in a well-defined manner.

The Docker images required for running the InChI Resolver prototype are available from `DockerHub <https://cloud.docker.com/u/inchiresolver/repository/list>`_.

InChI Resolver Protocol
-----------------------

The InChI Resolver protocol is the specification of a common API protocol format any InChI Resolver instance should adhere to. The goal of using a common InChI Resolver protocol is making web resources which provide information based on/indexed by InChI findable and browsable for an (automated) client system in a systematic manner.

The InChI Resolver protocol is based on the IANA-registered JSON:API v1.0 specification (`<https://jsonapi.org/>`_) as media type format.
JSON:API delineates how clients should request or edit data from a server, and how the server should respond to any requests. A main goal of the specification is to optimize HTTP requests; both in terms of the number of requests and the size of data packages exchanged between clients and servers.

For more details read `here <docs/inchi_resolver_protocol.rst>`_.

Links & Resources
-----------------

InChI Resolver web page: `<https://inchi-resolver.org>`_

Currently there are three Prototype InChI Resolver APIs in development which should act as a demonstration system for the interaction of several InChI Resolver instances based on the InChI Resolver Protocol:

1) the (InChI Trust) Root InChI Resolver at `<https://root.inchi-resolver.org>`_
2) the InChI Resolver Instance of the NCI/CADD group, respectively the Chemical Structure Resolver at `<https://cactus.inchi-resolver.org>`_
3) the PubChem InChI Resolver Instance at `<https://pubchem.inchi-resolver.org>`_

The development of the InChI Resolver project created `Chembience <https://chembience.com/>`_
(`GitHub repository <https://github.com/chembience/chembience>`_) as spin-off open-source project. As a Python-based
platform integrating RDKit (`<http://rdkit.org/>`_), Chembience provides all infrastructure-related components (modern software delivery mechanism, web server, and database server) for the development of web-based cheminformatics services. Chembience has been first
released publicly in March 2018 and has since seen more than ten releases. The InChI Resolver prototypes have been implemented on basis of Chembience: `<https://chembience.com>`_; some slides about the concepts in Chembience: `SlideShare Link <https://www.slideshare.net/sitzmann/chembience>`_


Requirements
------------

Please have at least `Docker CE 17.09 <https://docs.docker.com/engine/installation/>`_ and `Docker Compose 1.17 <https://docs.docker.com/compose/install/>`_ installed on your system.


Installation of the InChI Resolver Prototype
--------------------------------------------

Clone the repository::

    git clone https://github.com/inchiresolver/inchiresolver.git inchiresolver

Then, change into the newly created directory ::

    cd inchiresolver/

and run the following command (it is important that you do this from inside the newly created ``inchiresolver`` directory) ::

    ./init
    ./up

As a first step, this will download all necessary Docker images to your system and may take a while for the
initial setup (approx 1.5GB of downloads from DockerHub). After a successful download, it will start a InChI resolver
instance locally.

The already applied ``./up`` commando has started up the container-based InChI Resolver App and a Postgres Database
instance (the initial configuration of the containers is provided in the ``.env`` file and the ``docker-compose.yml``
file, **NOTE**: the InChI Resolver App connects to port 8011 of the host system, if this port is already in
use, it can by reconfigured in ``.env``, see variable ``DJANGO_APP_CONNECTION_PORT``). If everything went fine, you
should now be able to go to ::

    http://localhost:8011/admin      (you should see Django Admin Login page)

For the initial setup of Django installation underlying the InChI Resolver still a few steps need to be done. Since
Django runs inside a Docker container you can not directly access Django's regular ``manage.py`` script to set up things.
Instead you have to use the ``django-manage-py`` script provided in the current directory which passes any arguments
to the ``manage.py`` script of the Django instance running inside the InChI Resolver container.

To finalize the initial setup of Django in your container instance, run these commands (except for using ``django-manage-py``
instead of ``manage.py`` these are the same steps as for any regular Django installation for setting up Django's admin pages) ::

    ./django-manage-py migrate           (creates the initial Django database tables)
    ./django-manage-py createsuperuser   (will prompt you to create a Django superuser account)
    ./django-manage-py collectstatic     (adds all media (css, js, templates) for the Django admin application; creates a static/ directory in the django directory)

After running these commands you should be able to go to::

    http://localhost:8011/admin

and login into the Django admin application with the just set up account and password.

In order to stop the InChI Resolver, use the ``down`` script::

    ./down

Anything you have created and stored so far in the database has been persisted. If you are familiar with ``docker-compose``,
all life-circle commands should work as expected, in fact, ``up`` and  ``down`` are just short cuts for their respective
``docker-compose`` commands.

Since the InChI Resolver App is based on Chembience's Django Template App, please take also a look at the `Chembience GitHub repository <https://github.com/chembience/chembience>`_ pages.


Markus Sitzmann 2020-03-12

    
