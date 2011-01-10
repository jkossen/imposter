#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Description {{{
"""
    imposter.dbmanage
    ~~~~~~~~~~~~~~~~~

    Application for maintaining the imposter database

    It's mostly used for updating the database schema and data when upgrading
    to newer imposter versions.

    :copyright: (c) 2010 by Jochem Kossen.
    :license: BSD, see LICENSE.txt for more details.
"""
# }}}

from flask import Flask
from migrate.versioning.api import version_control, upgrade, downgrade, db_version, version
from sqlalchemy.sql import and_
from models import User, Tag, Status, Format, Post, post_tags
from database import DB
from flaskjk import encrypt_password, slugify
from datetime import datetime

import sys
import getpass
import datamigrations

app = Flask(__name__, static_path=None)
app.config.from_pyfile('config_admin.py')
app.config.from_envvar('IMPOSTER_DBMANAGE_CONFIG', silent=True)
db = app.config['DATABASE']
repo = 'migrations/'

def vc_db():
    """install SQLAlchemy-migrate versioning tables into database"""
    version_control(url=db, repository=repo)

def upgrade_db(v=None):
    """upgrade database schema to latest version"""
    from_version = db_version(url=db, repository=repo)
    to_version = v
    if to_version is None:
        to_version = version(repository=repo)

    print("Upgrading db from version %d to %d. " % (from_version, to_version))
    print("Schema upgrade ... ")
    upgrade(url=db, repository=repo, version=v)
    print("Data upgrade ... ")
    datamigrations.run_upgrade_scripts(app, from_version, to_version)
    print("Done!")


def downgrade_db(v):
    """downgrade database schema to specified version"""
    from_version = db_version(url=db, repository=repo)
    to_version = int(v)

    print("Downgrading db from version %d to %d. " % (from_version, to_version))
    print("Schema upgrade ... ")
    downgrade(url=db, repository=repo, version=v)
    print("Data upgrade ... ")
    datamigrations.run_downgrade_scripts(app, from_version, to_version)
    print("Done!")

def add_initial_data():
    """Insert initial data into the database"""
    # open database session
    db_session = DB(db).get_session()

    # ask user for an admin username and password
    username = raw_input('Please enter the admin username: ')
    password = getpass.getpass(prompt='Please enter the admin password: ')

    # add user to database
    u = User(username, encrypt_password(app.config['SECRET_KEY'], password))
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
    initial_post_summary = """
Installed Correctly!
"""
    initial_post_content = """
Imposter was installed correctly!

This is just a sample post to show Imposter works.

**Have a lot of fun blogging!**
"""
    p1 = Post('Welcome to Imposter!', initial_post_summary, initial_post_content)
    p1.slug = slugify(p1.title)
    p1.createdate = datetime.now()
    p1.lastmoddate = datetime.now()
    p1.pubdate = datetime.now()
    p1.format = f
    p1.status = s3
    p1.user = u
    p1.tags = [t1, t2]
    p1.compile()
    db_session.add(p1)
    db_session.commit()

def install_db():
    """Initialize new Imposter database"""
    vc_db()
    upgrade_db()
    add_initial_data()

def usage():
    """show dbmanage.py usage"""
    print 'usage: dbmanage.py install|upgrade|downgrade version'

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
    elif sys.argv[1] == 'downgrade' and len(sys.argv) == 3:
        downgrade_db(sys.argv[2])
    else:
        usage()
        sys.exit(1)
