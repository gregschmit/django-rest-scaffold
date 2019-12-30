Django REST Scaffold
====================

.. inclusion-marker-do-not-remove

.. image:: https://travis-ci.org/gregschmit/django-rest-scaffold.svg?branch=master
    :alt: TravisCI
    :target: https://travis-ci.org/gregschmit/django-rest-scaffold

.. image:: https://img.shields.io/pypi/v/django-rest-scaffold
    :alt: PyPI
    :target: https://pypi.org/project/django-rest-scaffold/

.. image:: https://coveralls.io/repos/github/gregschmit/django-rest-scaffold/badge.svg?branch=master
    :alt: Coveralls
    :target: https://coveralls.io/github/gregschmit/django-rest-scaffold?branch=master

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :alt: Code Style
    :target: https://github.com/ambv/black

Source: https://github.com/gregschmit/django-rest-scaffold

REST Scaffold is a Django app that provides a template tag helper for using
the `rest-scaffold.js <https://github.com/gregschmit/rest-scaffold>`_ library.

**The Problem**: AJAX is nice because if you have an API, then you don't need separate
pages/views for listing, creating, and updating model instances. But writing custom AJAX
tables on the frontend can be time-consuming.

**The Solution**: This app provides a template tag that uses ``rest-scaffold.js`` to
quickly render "scaffolds", which are tables that have controls which interact with your
API.


How to Use
==========

.. code-block:: shell

    $ pip install django-rest-scaffold

Include ``rest_scaffold`` in your ``INSTALLED_APPS``.

Build your API or create one using
`AutoREST <https://github.com/gregschmit/autorest>`_.

Then, insert a scaffold using the ``rest_scaffold`` template tag. At the top
you'll need to load the template tag:

.. code-block:: python

    {% load rest_scaffold %}

And then wherever you want in the HTML page, inject the scaffold:

.. code-block:: python

    {% rest_scaffold 'user' api_root='api' %}

In the above example, you would see a scaffold for the ``User`` model.


Contributing
============

Open a pull request fixing a bug or implementing a feature if you want to
contribute. You must only contribute code that you have authored or otherwise
hold the copyright to, and you must make any contributions to this project
available under the MIT license.

To collaborators: don't push using the ``--force`` option.


Dev Quickstart
==============

REST Scaffold comes with a ``settings.py`` file, technically making it a Django project
as well as a Django app. First clone, the repository into a location of your choosing:

.. code-block:: shell

    $ git clone https://github.com/gregschmit/django-rest-scaffold

Then you can go into the ``django-rest-scaffold`` directory, install the test
environment requirements, and then migrate and run the local development server:

.. code-block:: shell

    $ cd django-rest-scaffold
    $ pip install -r requirements-test.txt
    $ python manage.py migrate
    $ python manage.py createsuperuser
    ...
    $ python manage.py runserver

Then you can see the api at http://127.0.0.1:8000/api/, and you can see the example
scaffold page at http://127.0.0.1:8000/example/.
