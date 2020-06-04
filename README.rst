zuul-stats-client
=================

This is a Python client to report various statistics from a `Zuul`_ server.

Requirements.
-------------

Python 3.6+. The ``requirements.txt`` file lists the extra Python librarires
required by the client.

Installation & Usage
--------------------

Install via `Setuptools`_.

.. code:: sh

   python setup.py install --user

(or ``sudo python setup.py install`` to install the package for all
users)

You can run the client directly:

.. code:: bash

   $ zuul-stats-client -h

.. _Zuul: https://zuul-ci.org/
.. _Setuptools: http://pypi.python.org/pypi/setuptools
