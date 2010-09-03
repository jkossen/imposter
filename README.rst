Imposter - Another weblog app
=============================

Copyright and license
---------------------

Copyright (c) 2010 by Jochem Kossen <jochem.kossen@gmail.com>

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

   1. Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.

   2. Redistributions in binary form must reproduce the above
      copyright notice, this list of conditions and the following
      disclaimer in the documentation and/or other materials provided
      with the distribution.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS
BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Imposter features and lack thereof
----------------------------------

* Imposter consists of small but functional separated admin and
  frontend applications. In the future a separate api and frontend
  user interaction app is planned. See also `Ideas behind the
  separation of apps`_

* Posts can be edited in ReST, Markdown or HTML code. This is a
  per-post option.

* Tag support

* Theme support (Jinja2 is used for templates)

* Supports various databases (everything SQLAlchemy supports)

* Simple to read, understand and hack code (and there's not a whole
  lot of it)

* Since the frontend app does not write to the data sources, there is
  NO support for comments. The current plan is to develop a separate
  app for frontend user interaction that will deal with this.

  I currently recommend using a service such as those provided by
  http://disqus.com or http://intensedebate.com


Ideas behind the separation of apps
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* You can easily run the admin on HTTPS while the front-end runs on
  HTTP

* You can easily run the admin on a private LAN while the front-end
  runs on public servers

* The frontend doesn't need write rights

* Performance: front-end can be optimized for viewing content, admin
  for changing content

* Run multiple front-ends to distribute load

* Stability: problems with the admin should not cause problems in the
  front-end and vice-versa


Installation
------------

Requirements
~~~~~~~~~~~~
Imposter requires the following software:

* Python (developed with 2.5 provided with Debian Lenny)
* Flask
* Werkzeug 
* Jinja2
* SQLAlchemy
* SQLAlchemy-migrate (database schema versioning)
* docutils (provides ReST support)
* Markdown

As Imposter uses SQLAlchemy for its database abstraction layer, make
sure you have a database supported by SQLAlchemy available.

Installation Instructions
~~~~~~~~~~~~~~~~~~~~~~~~~
* Install the software listed under `Requirements`_
* Adjust the configuration in config.py
* Create a database and database accounts for Imposter
* Install the Imposter database: python dbmanage.py install

There are several options for running Imposter. To run with the
standard Werkzeug webserver, you can just run python frontend.py for
the frontend, and python admin.py for the admin. Because this is often
not an option for production environments, you can also run Imposter
under Apache using mod_wsgi, or using FastCGI under any other
webserver.

For mod_wsgi, Imposter comes with frontend.wsgi and admin.wsgi files.

For FastCGI, Imposter comes with frontend.fcgi and admin.fcgi files.

Check http://flask.pocoo.org/docs/deploying/ for more information
concerning deployment.
