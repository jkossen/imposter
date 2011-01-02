#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Description {{{
"""
    imposter.admin
    ~~~~~~~~~~~~~~

    Admin interface for the Imposter weblog app

    :copyright: (c) 2010 by Jochem Kossen.
    :license: BSD, see LICENSE.txt for more details.
"""
# }}}

# Imports {{{
from __future__ import with_statement
from flask import Flask, request, session, abort, redirect, url_for, flash
from functools import wraps
from database import DB
from models import User, Tag, Format, Status, Post, Page, post_tags
from datetime import datetime
from sqlalchemy.sql import and_
from flaskjk import Viewer, hashify, slugify
from frontend import filter_public

import os
import re
# }}}

# Initialization {{{
app = Flask(__name__, static_path=None)
app.config.from_pyfile('config_admin.py')
app.config.from_envvar('IMPOSTER_ADMIN_CONFIG', silent=True)
db_session = DB(app.config['DATABASE']).get_session()
viewer = Viewer(app, 'admin')

# base query used in all frontend retrieve queries
public_posts_base = db_session.query(Post, Status, User).filter(filter_public())
# }}}

# Shortcut functions {{{
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
                                  Post.id==post_id)).first()
    if post is None:
        abort(404)

    return post

def get_page(page_id):
    """ Retrieve Page object based on given Page id"""
    page = Page.query.filter(and_(Page.user_id==session['user_id'],
                                  Page.id==page_id)).first()
    if page is None:
        abort(404)

    return page
# }}}

# Template filters {{{
@app.template_filter('strftime')
def strftime(value, format='%a, %d %b %Y %H:%M:%S %Z'):
    """Template filter for human-readable date formats"""
    return value.strftime(format)
# }}}

# Views {{{
@viewer.view('static_files')
def static(filename):
    """Send static files such as style sheets, JavaScript, etc."""
    return viewer.static(filename)

@viewer.view('login', methods=['POST'])
def login():
    """Check user credentials and initialize session"""
    error = None
    if request.method == 'POST':
        hashedpassword = hashify(app.config['SECRET_KEY'],
                                 request.form['password'])
        userquery = User.query.filter(and_(
            User.username==request.form['username'],
            User.password==hashedpassword))

        if userquery.count() == 1:
            user = userquery.first()
            session['username'] = user.username
            session['user_id'] = user.id
            flash('You\'re now logged in')
            return redirect(url_for('index'))

        error = 'Unknown user'
    return viewer.render('login.html', error=error)

@viewer.view('logout')
@login_required
def logout():
    """Clear the session"""
    session.clear()
    flash('You were logged out')
    return redirect(url_for('index'))

@viewer.view('index')
@login_required
def index():
    """The front page of this application"""
    posts = db_session.query(Post).filter(
        Post.user_id==session['user_id']).order_by(Post.pubdate.desc())
    pages = db_session.query(Page).filter(
        Page.user_id==session['user_id'])
    return viewer.render('index.html', posts=posts, pages=pages)

def recalculate_tagcount(tag):
    tag.count = public_posts_base.filter(Post.tags.contains(tag)).count()

@viewer.view('recalculate_tagcounts')
@login_required
def recalculate_tagcounts():
    for tag in db_session.query(Tag):
        recalculate_tagcount(tag)
    db_session.commit()
    return redirect(url_for('index'))

@viewer.view('new_post')
@viewer.view('edit_post')
@login_required
def edit_post(post_id=None):
    """Render form to edit a Post"""
    formats = db_session.query(Format).all()
    statuses = db_session.query(Status).all()
    post = None

    if post_id:
        post = get_post(post_id)

    return viewer.render('edit_post.html',
                           post=post,
                           formats=formats,
                           statuses=statuses)

@viewer.view('new_page')
@viewer.view('edit_page')
@login_required
def edit_page(page_id=None):
    """Render form to edit a Page"""
    formats = db_session.query(Format).all()
    statuses = db_session.query(Status).all()
    page = None

    if page_id:
        page = get_page(page_id)

    return viewer.render('edit_page.html',
                           page=page,
                           formats=formats,
                           statuses=statuses)

@viewer.view('save_new_post', methods=['POST'])
@viewer.view('save_post', methods=['POST'])
@login_required
def save_post(post_id=None):
    """Save Post to database

    If post_id is None a new Post will be inserted in the database. Otherwise
    the existing Post will be updated.
    """
    message = 'Post updated'
    orig_tags = []

    if post_id is None:
        post = Post(request.form['title'], request.form['text'])
        post.status_id = 1
        post.user_id = session['user_id']
        post.createdate = datetime.now()
    else:
        post = get_post(post_id)
        orig_tags = [tag for tag in post.tags]

    post.title = request.form['title']
    post.summary = request.form['summary']
    post.content = request.form['text']
    post.lastmoddate = datetime.now()
    post.format = get_format(request.form['format'])
    post.pubdate = datetime.strptime(request.form['pubdate'].strip(),
                                     '%Y-%m-%d %H:%M')

    # compile input to html
    post.compile(app.config['REPL_TAGS'])

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

    if post.slug is None:
        post.slug = slugify(post.title)

    if post_id is None:
        db_session.add(post)
        message = 'New post was successfully added'

    db_session.commit()

    for tag in orig_tags:
        recalculate_tagcount(tag)

    for tag in post.tags:
        if tag not in orig_tags:
            recalculate_tagcount(tag)

    db_session.commit()

    flash(message)

    return redirect(url_for('edit_post', post_id=post.id))

@viewer.view('save_new_page', methods=['POST'])
@viewer.view('save_page', methods=['POST'])
@login_required
def save_page(page_id=None):
    """Save Page to database

    If page_id is None a new Page will be inserted in the database. Otherwise
    the existing Page will be updated.
    """
    message = 'Page updated'

    if page_id is None:
        page = Page(request.form['title'], request.form['text'])
        page.status_id = 1
        page.user_id = session['user_id']
        page.createdate = datetime.now()
    else:
        page = get_page(page_id)

    page.title = request.form['title']
    page.content = request.form['text']
    page.lastmoddate = datetime.now()
    page.format = get_format(request.form['format'])
    page.pubdate = datetime.strptime(request.form['pubdate'].strip(),
                                     '%Y-%m-%d %H:%M')

    # compile input to html
    page.compile(app.config['REPL_TAGS'])

    # update pubdate if page's pubdate is None and its status is set
    # to public
    if request.form['status'] == 'public' and \
           unicode(page.status) != 'public' and \
           page.pubdate is None:
        page.pubdate = datetime.now()

    page.status = get_status(request.form['status'])

    if page.slug is None:
        page.slug = slugify(page.title)

    if page_id is None:
        db_session.add(page)
        message = 'New page was successfully added'

    db_session.commit()

    flash(message)

    return redirect(url_for('edit_page', page_id=page.id))

# }}}

# Main run loop {{{
if __name__ == '__main__':
    app.run(host=app.config['HOST'], port=app.config['PORT'])
# }}}
