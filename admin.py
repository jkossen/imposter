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

This is the admin application code for Imposter. It's used for editing
content, and every action requires a logged-in user.

"""

from __future__ import with_statement
from flask import Flask, g, request, session, abort, redirect, url_for, \
     render_template, send_from_directory, flash
from functools import wraps
from database import DB
from models import User, Tag, Format, Status, Post
from datetime import datetime
from sqlalchemy.sql import and_
from helpers import hashify, slugify

import os
import re
import config as cfg

#---------------------------------------------------------------------------
# INITIALIZATION

db_session = DB(cfg.ADMIN_DATABASE).get_session()
app = Flask(__name__, static_path=None)
app.config.from_object(cfg)

#---------------------------------------------------------------------------
# SHORTCUT FUNCTIONS

def login_required(fun):
    """Decorator for functions which require an authorized user"""
    @wraps(fun)
    def decorated_function(*args, **kwargs):
        """Decorated function"""
        if not session.get('user_id'):
            return login()
        return fun(*args, **kwargs)

    return decorated_function

def get_tag(value):
    """Retrieve Tag object based on given String

    If no such Tag object exists, return a new Tag object.
    """
    tag = Tag.query.filter(Tag.value==value).first()
    if tag is None:
        return Tag(value)
    return tag

def get_format(value):
    """Retrieve Format object based on given String"""
    query = Format.query.filter(Format.value==value)
    return query.one()

def get_status(value):
    """Retrieve Status object based on given String"""
    query = Status.query.filter(Status.value==value)
    return query.one()

def get_post(post_id):
    """ Retrieve Post object based on given Post id"""
    post = Post.query.filter(and_(Post.user_id==session['user_id'],
                                  Post.id=='%d' % post_id)).first()
    if post is None:
        abort(404)

    return post

def get_route(function):
    """Return complete route based on configuration and routes"""
    return '/%s%s' % (cfg.ADMIN_PREFIX, cfg.ADMIN_ROUTES[function])

#---------------------------------------------------------------------------
# TEMPLATE FILTERS

@app.template_filter('strftime')
def strftime(value, format='%a, %d %b %Y %H:%M:%S %Z'):
    """Template filter for human-readable date formats"""
    return value.strftime(format)

#---------------------------------------------------------------------------
# VIEWS

@app.route(get_route('static_files'))
def static(filename):
    """Send static files such as style sheets, JavaScript, etc."""
    static_path = os.path.join(app.root_path, 'templates', 'admin', 'static')
    return send_from_directory(static_path, filename)

@app.route(get_route('login'), methods=['POST'])
def login():
    """Check user credentials and initialize session"""
    g.cfg = cfg
    error = None
    if request.method == 'POST':
        hashedpassword = hashify(request.form['password'])
        userquery = User.query.filter(and_(
            User.username=='%s' % request.form['username'],
            User.password=='%s' % hashedpassword))

        if userquery.count() == 1:
            user = userquery.first()
            session['username'] = user.username
            session['user_id'] = user.id
            flash('You were logged in')
            return redirect(url_for('index'))

        error = 'Unknown user'
    return render_template(os.path.join('admin', 'login.html'), error=error)

@app.route(get_route('logout'))
@login_required
def logout():
    """Clear the session"""
    session.clear()
    flash('You were logged out')
    return redirect(url_for('index'))

@app.route(get_route('index'))
@login_required
def index():
    """The front page of this application"""
    g.cfg = cfg
    posts = db_session.query(Post).filter(
        Post.user_id==session['user_id'])
    return render_template(os.path.join('admin', 'index.html'), posts=posts)

@app.route(get_route('new_post'))
@app.route(get_route('edit_post'))
@login_required
def edit_post(post_id=None):
    """Render form to edit a Post"""
    g.cfg = cfg
    formats = db_session.query(Format).all()
    statuses = db_session.query(Status).all()
    post = None

    if post_id:
        post = get_post(post_id)

    return render_template(os.path.join('admin', 'edit_post.html'),
                           post=post,
                           formats=formats,
                           statuses=statuses)

@app.route(get_route('save_new_post'), methods=['POST'])
@app.route(get_route('save_post'), methods=['POST'])
@login_required
def save_post(post_id=None):
    """Save changed Post content to database or save new Post"""
    g.cfg = cfg
    message = 'Post updated'

    if post_id is None:
        post = Post(request.form['title'], request.form['text'])
        post.status_id = 1
        post.user_id = session['user_id']
        post.createdate = datetime.now()
    else:
        post = get_post(post_id)

    post.title = request.form['title']
    post.content = request.form['text']
    post.lastmoddate = datetime.now()
    post.format = get_format(request.form['format'])
    post.pubdate = datetime.strptime(request.form['pubdate'].strip(), '%Y-%m-%d %H:%M')

    # update pubdate if post's pubdate is None and its status is set
    # to public
    if request.form['status'] == 'public' and \
           unicode(post.status) != 'public' and \
           post.pubdate is None:
        post.pubdate = datetime.now()

    post.status = get_status(request.form['status'])

    sep = re.compile('\s*,\s*')
    post.tags = [get_tag(tag) for tag \
                 in sep.split(request.form['tags'].lower())]

    post.slug = slugify(post.title)

    if post_id is None:
        db_session.add(post)
        message = 'New post was successfully added'

    db_session.commit()

    flash(message)

    return redirect(url_for('edit_post', post_id=post_id))

#---------------------------------------------------------------------------
# MAIN RUN LOOP
if __name__ == '__main__':
    app.run(host=cfg.ADMIN_HOST, port=cfg.ADMIN_PORT)
