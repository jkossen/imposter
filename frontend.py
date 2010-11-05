#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Description {{{
"""
    imposter.frontend
    ~~~~~~~~~~~~~~~~~

    Frontend application for the Imposter weblog app

    :copyright: (c) 2010 by Jochem Kossen.
    :license: BSD, see LICENSE.txt for more details.
"""
# }}}

# Imports {{{
from flask import Flask, abort
from datetime import datetime
from models import User, Tag, Status, Post
from sqlalchemy.sql import and_

from database import DB
from flaskjk import Viewer, summarize, markup_to_html

import os
# }}}

# Initialization {{{
app = Flask(__name__, static_path=None)
app.config.from_pyfile('config_frontend.py')
app.config.from_envvar('IMPOSTER_FRONTEND_CONFIG', silent=True)
db_session = DB(app.config['DATABASE']).get_session()
viewer = Viewer(app, 'frontend', app.config['UPLOAD_PATH'])

# filter to make sure we only get posts which have status 'public'
filter_public = and_(Post.status_id==Status.id,
                 Status.value=='public',
                 Post.user_id==User.id,
                 Post.pubdate <= datetime.now()
                 )

# base query used in all frontend retrieve queries
posts_base = db_session.query(Post, Status, User).filter(filter_public)
# }}}

# Shortcut functions {{{
def post_list(posts):
    """Render a list of posts"""
    return viewer.render('post_list.html', posts=posts)

@app.after_request
def shutdown_session(response):
    """End session, close database"""
    db_session.remove()
    return response
# }}}

# Context Processors {{{
@app.context_processor
def inject_recent_posts():
    return dict(recent_posts=posts_base.order_by(Post.pubdate.desc())[0:10])

# }}}

# Template filters {{{
@app.template_filter('strftime')
def tf_strftime(value, format='%a, %d %b %Y %H:%M:%S %Z'):
    """Template filter for human-readable date formats"""
    return value.strftime(format)

@app.template_filter('summarize')
def tf_summarize(content, length=250, suffix='...'):
    """Generate summary from marked-up content"""
    return summarize(content, length, suffix)

@app.template_filter('to_html')
def tf_to_html(content, format):
    """Convert input to html"""
    return markup_to_html(format, content)
# }}}

# Views {{{
@viewer.view('static_files')
def static(filename):
    """Send static files such as style sheets, JavaScript, etc."""
    return viewer.static(filename)

@viewer.view('uploads')
def uploaded(filename):
    """Send static files from the uploads directory."""
    return viewer.uploaded(filename)

@viewer.view('index')
def show_index():
    """Render the frontpage"""
    posts = posts_base.order_by(Post.pubdate.desc())
    return post_list(posts)

@viewer.view('show_post')
def show_post(slug, **kwargs):
    """Render a Post"""
    post = posts_base.filter(Post.slug==slug).first()
    return viewer.render('post.html', post=post[0])

@viewer.view('postlist_by_tag')
def show_postlist_by_tag(tag):
    """Render a post list filtered by tag"""
    tagobj = Tag.query.filter(Tag.value==tag).first()
    if tagobj is None:
        abort(404)
    posts = posts_base.filter(Post.tags.contains(tagobj)).order_by(Post.pubdate.desc())
    return post_list(posts)

@viewer.view('postlist_by_username')
def show_postlist_by_username(username):
    """Render a post list filtered by username"""
    userobj = User.query.filter(User.username==username).first()
    if userobj is None:
        abort(404)
    posts = posts_base.filter(Post.user==userobj).order_by(Post.pubdate.desc())
    return post_list(posts)

@viewer.view('show_atom')
def show_atom():
    """Render atom feed with recent posts"""
    posts = posts_base.order_by(Post.pubdate.desc())[:app.config['FEEDITEMS']]
    return viewer.render('atom.xml', posts=posts)

@viewer.view('show_rss')
def show_rss():
    """Render RSS feed with recent posts"""
    posts = posts_base.order_by(Post.pubdate.desc())[:app.config['FEEDITEMS']]
    return viewer.render('rss.xml', posts=posts)
# }}}

# Main run loop {{{
if __name__ == '__main__':
    app.run(host=app.config['HOST'], port=app.config['PORT'])
# }}}
