=============================
Imposter - Another weblog app
=============================
:Author: Jochem Kossen

Imposter is a weblog application, written in Python_, utilizing Flask_,
Werkzeug_, Jinja2_ and SQLAlchemy_.

Copyright and license
---------------------

:copyright: (c) 2010-2011 by Jochem Kossen <jochem.kossen@gmail.com>
:license: two-clause BSD

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

   1. Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.

   2. Redistributions in binary form must reproduce the above
      copyright notice, this list of conditions and the following
      disclaimer in the documentation and/or other materials provided
      with the distribution.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS "AS IS" AND
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

* Posts can be edited in ReST_, Markdown_ or HTML code. This is a
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

* The frontend and public_api app don't need write permissions since
  they don't manipulate data

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

* `Python`_ (developed with 2.5 provided with Debian Lenny)
* `Flask`_
* `Werkzeug`_
* `Jinja2`_
* `SQLAlchemy`_
* `SQLAlchemy-migrate`_ (database schema versioning)
* `docutils`_ (provides ReST support)
* `Markdown`_
* `Flask-WTF`_ (`WTForms`_ extension for Flask)
* Flaskjk_ (my own library with generic Flask functions)

As Imposter uses SQLAlchemy for its database abstraction layer, make sure you
have a database supported by SQLAlchemy available.

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

.. _Python: http://www.python.org
.. _Flask: http://flask.pocoo.org
.. _Werkzeug: http://werkzeug.pocoo.org
.. _Jinja2: http://jinja.pocoo.org
.. _SQLAlchemy: http://www.sqlalchemy.org
.. _SQLAlchemy-migrate: http://code.google.com/p/sqlalchemy-migrate/
.. _docutils: http://docutils.sourceforge.net
.. _ReST: http://docutils.sourceforge.net/rst.html
.. _Markdown: http://daringfireball.net/projects/markdown
.. _Flask-WTF: http://packages.python.org/Flask-WTF/
.. _WTForms: http://wtforms.simplecodes.com
.. _Flaskjk: http://github.com/jkossen/flaskjk
