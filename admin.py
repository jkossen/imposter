#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Description {{{
"""
    imposter.admin
    ~~~~~~~~~~~~~~

    Admin interface for the Imposter weblog app

    :copyright: (c) 2010-2011 by Jochem Kossen.
    :license: BSD, see LICENSE.txt for more details.
"""
# }}}

# Imports {{{
from __future__ import with_statement
from flask import Flask, request, session, abort, redirect, url_for, flash
from functools import wraps
from database import DB
from models import User, Tag, Format, Status, Post, Page
from datetime import datetime
from sqlalchemy.sql import and_
from flaskjk import Viewer, Paginator, validate_password, slugify
from frontend import filter_public
from forms import PostForm, PageForm, LoginForm
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

# Helper functions {{{
def login_required(fun):
    """Decorator for functions which require an authorized user"""
    @wraps(fun)
    def decorated_function(*args, **kwargs):
        """Decorated function"""
        if not session.get('user_id'):
            return login()
        return fun(*args, **kwargs)

    return decorated_function

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

def recalculate_tagcount(tag):
    """Calculate how many times a given tag is used in public Posts"""
    tag.count = public_posts_base.filter(Post.tags.contains(tag)).count()

# }}}

# Template filters {{{
@app.template_filter('strftime')
def strftime(value, format='%a, %d %b %Y %H:%M:%S %Z'):
    """Template filter for human-readable date formats"""
    return value.strftime(format)
# }}}

# Views {{{
@viewer.view('static_files')
def static_files(filename):
    """Send static files such as style sheets, JavaScript, etc."""
    return viewer.static(filename)

@viewer.view('login', methods=['POST'])
def login():
    """Check user credentials and initialize session"""
    # use a single error message for all failures so the "user" doesn't see what
    # specifically went wrong
    default_error = 'ERROR: Unknown user'

    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.form)
        if form.validate():
            try:
                user = User.query.filter(
                    User.username==request.form['username']).one()
            except:
                flash(default_error, category='error')
                return viewer.render('login.html', form=form)

            if validate_password(app.config['SECRET_KEY'],
                                 request.form['password'],
                                 user.password):
                # We have a valid login, initialize session
                session['username'] = user.username
                session['user_id'] = user.id

                flash('Logged in successfully', category='info')
                return redirect(url_for('index'))
            else:
                flash(default_error, category='error')
        else:
            flash('Incorrect form input', category='error')

    return viewer.render('login.html', form=form)

@viewer.view('logout')
@login_required
def logout():
    """Clear the session"""
    session.clear()
    flash('You were logged out', category='info')
    return redirect(url_for('index'))

@viewer.view('posts_list')
@login_required
def posts_list(page=1):
    """Paginated view of all posts"""
    p_order = Post.pubdate.desc()
    posts = db_session.query(Post).filter(
        Post.user_id==session['user_id']).order_by(Post.pubdate.desc())
    paginator = Paginator(posts, app.config['ENTRIES_PER_PAGE'], page,
                          'posts_list')
    return viewer.render('posts_list.html', posts=posts, paginator=paginator)

@viewer.view('pages_list')
@login_required
def pages_list(page=1):
    """Paginated view of all pages"""
    p_order = Page.pubdate.desc()
    pages = db_session.query(Page).filter(
        Page.user_id==session['user_id']).order_by(Page.pubdate.desc())
    paginator = Paginator(pages, app.config['ENTRIES_PER_PAGE'], page,
                          'pages_list')
    return viewer.render('pages_list.html', pages=pages, paginator=paginator)

@viewer.view('index')
@login_required
def index():
    """The front page of this application"""
    posts = db_session.query(Post).filter(
        Post.user_id==session['user_id']).order_by(Post.pubdate.desc())
    pages = db_session.query(Page).filter(
        Page.user_id==session['user_id'])
    return viewer.render('index.html', posts=posts, pages=pages)

@viewer.view('recalculate_tagcounts')
@login_required
def recalculate_tagcounts():
    """Recount all tag uses"""
    for tag in db_session.query(Tag):
        recalculate_tagcount(tag)
    db_session.commit()
    return redirect(url_for('index'))

@viewer.view('new_post')
@viewer.view('edit_post')
@login_required
def edit_post(post_id=None, post_form=None):
    """Render form to edit a Post"""
    formats = db_session.query(Format).all()
    statuses = db_session.query(Status).all()
    post = None
    form = None

    if post_id:
        post = get_post(post_id)

    if post_form is None:
        form = PostForm(obj=post)
    else:
        form = post_form

    return viewer.render('edit_post.html',
                         form=form,
                         post=post,
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

    post_form = PostForm(request.form)

    if not post_form.validate():
        flash('ERROR: errors detected. Post NOT saved!', category='error')
        return edit_post(post_id=post_id, post_form=post_form)

    # test if we're creating a new post, or updating an existing one
    if post_id is None:
        post = Post()
        post.status_id = 1
        post.user_id = session['user_id']
        post.createdate = datetime.now()
    else:
        post = get_post(post_id)
        orig_tags = [tag for tag in post.tags]

    post_form.populate_obj(post)
    post.lastmoddate = datetime.now()

    # compile input to html
    post.compile(app.config['REPL_TAGS'])

    # update pubdate if post's pubdate is None and its status is set
    # to public
    if request.form['status'] == 'public' and \
           unicode(post.status) != 'public' and \
           post.pubdate is None:
        post.pubdate = datetime.now()

    post.status = get_status(request.form['status'])

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

    flash(message, category='info')

    return redirect(url_for('edit_post', post_id=post.id))

@viewer.view('new_page')
@viewer.view('edit_page')
@login_required
def edit_page(page_id=None, page_form=None):
    """Render form to edit a Page"""
    formats = db_session.query(Format).all()
    statuses = db_session.query(Status).all()
    page = None
    form = None

    if page_id:
        page = get_page(page_id)

    if page_form is None:
        form = PageForm(obj=page)
    else:
        form = page_form

    return viewer.render('edit_page.html',
                           form=form,
                           page=page,
                           formats=formats,
                           statuses=statuses)

@viewer.view('save_new_page', methods=['POST'])
@viewer.view('save_page', methods=['POST'])
@login_required
def save_page(page_id=None):
    """Save Page to database

    If page_id is None a new Page will be inserted in the database. Otherwise
    the existing Page will be updated.
    """
    message = 'Page updated'

    page_form = PageForm(request.form)

    if not page_form.validate():
        flash('ERROR: errors detected. Page NOT saved!', category='error')
        return edit_page(page_id=page_id, page_form=page_form)

    if page_id is None:
        page = Page(request.form['title'], request.form['content'])
        page.status_id = 1
        page.user_id = session['user_id']
        page.createdate = datetime.now()
    else:
        page = get_page(page_id)

    page_form.populate_obj(page)
    page.lastmoddate = datetime.now()

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
