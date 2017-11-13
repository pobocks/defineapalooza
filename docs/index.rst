.. defineapalooza documentation master file, created by
   sphinx-quickstart on Tue Oct 24 20:05:38 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.
   
   
Welcome to defineapalooza's documentation!
==========================================

Defineapalooza is a single page application for fetching dictionary definition information from the Oxford Dictionary API and a list of potentially related LCSH subject headings from id.loc.gov.  It is a single page application (really, a single-FORM application), making requests over AJAX if possible, falling back to form-submission.

.. toctree::
   :maxdepth: 4
   :caption: Contents:

Summary
=======
.. qrefflask:: defineapalooza:app
   :undoc-static:

API Docs
========
.. autoflask:: defineapalooza:app
   :undoc-static:



Indices and tables
==================

* :ref:`genindex`
* :ref:`search`

.. comment * :ref:`modindex`
