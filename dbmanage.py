#!/usr/bin/env python
"""
Imposter - Another weblog app
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

This is the database management code for Imposter. It's used for
installing a new Imposter database and upgrading it to newer versions.

"""

from flask import Flask
from migrate.versioning.api import version_control, upgrade
from models import User, Tag, Status, Format, Post
from database import DB
from helpers import hashify, slugify
from datetime import datetime

import sys
import getpass

app = Flask(__name__, static_path=None)
app.config.from_pyfile('config.py')
app.config.from_envvar('IMPOSTER_DBMANAGE_CONFIG', silent=True)

def vc_db():
    """install SQLAlchemy-migrate versioning tables into database"""
    version_control(url=app.config['ADMIN_DATABASE'], repository='migrations/')

def upgrade_db():
    """upgrade database schema to latest version"""
    upgrade(url=app.config['ADMIN_DATABASE'], repository='migrations/')

def add_initial_data():
    """Insert initial data into the database"""
    # open database session
    db_session = DB(app.config['ADMIN_DATABASE']).get_session()

    # ask user for an admin username and password
    username = raw_input('Please enter the admin username: ')
    password = getpass.getpass(prompt='Please enter the admin password: ')

    # add user to database
    u = User(username, hashify(app.config['SECRET_KEY'], password))
    db_session.add(u)

    # create statuses
    s1 = Status('draft')
    s2 = Status('private')
    s3 = Status('public')
    db_session.add(s1)
    db_session.add(s2)
    db_session.add(s3)

    # create formats
    f = Format('rest')
    f2 = Format('markdown')
    db_session.add(f)
    db_session.add(f2)

    # Tags
    t1 = Tag('imposter')
    t2 = Tag('weblog')

    # build initial post and put it in the database
    initial_post_content = """
Imposter was installed correctly!
    
This is just a sample post to show Imposter works.

**Have a lot of fun blogging!**
"""
    p1 = Post('Welcome to Imposter!', initial_post_content)
    p1.slug = slugify(p1.title)
    p1.createdate = datetime.now()
    p1.lastmoddate = datetime.now()
    p1.pubdate = datetime.now()
    p1.format = f
    p1.status = s3
    p1.user = u
    p1.tags = [t1, t2]
    db_session.add(p1)
    db_session.commit()

def install_db():
    """Initialize new Imposter database"""
    vc_db()
    upgrade_db()
    add_initial_data()

def usage():
    """show dbmanage.py usage"""
    print 'usage: dbmanage.py install|upgrade'

#---------------------------------------------------------------------------
# MAIN RUN LOOP
if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)

    if sys.argv[1] == 'install': 
        install_db()
    elif sys.argv[1] == 'upgrade':
        upgrade_db()
    else:
        usage()
        sys.exit(1)
