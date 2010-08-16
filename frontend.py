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

This is the frontend application code for Imposter. It's only used for
viewing content, not manipulation.

"""

from flask import Flask, g, render_template, send_from_directory, abort
from datetime import datetime
from models import User, Tag, Status, Post
from sqlalchemy.sql import and_

from database import DB

import os

import config as cfg
import helpers

#---------------------------------------------------------------------------
# INITIALIZATION

app = Flask(__name__, static_path=None)
app.config.from_object(cfg)

db_session = DB(cfg.FRONTEND_DATABASE).get_session()

# filter to make sure we only get posts which have status 'public'
filter_public = and_(Post.status_id==Status.id,
                 Status.value=='public',
                 Post.user_id==User.id,
                 Post.pubdate <= datetime.now()
                 )

# base query used in all frontend retrieve queries
posts_base = db_session.query(Post, Status, User).filter(filter_public)

#---------------------------------------------------------------------------
# SHORTCUT FUNCTIONS

def get_route(function):
    """Return complete route based on configuration and routes"""
    return '/%s%s' % (cfg.FRONTEND_PREFIX, cfg.FRONTEND_ROUTES[function])

def themed(template):
    """Return path to template in configured theme"""
    return os.path.join('frontend', cfg.THEME, template)

def post_list(posts):
    """Render a list of posts"""
    g.cfg = cfg
    return render_template(themed('post_list.html'), posts=posts)

@app.after_request
def shutdown_session(response):
    """End session, close database"""
    db_session.remove()
    return response

#---------------------------------------------------------------------------
# TEMPLATE FILTERS

@app.template_filter('datetimeformat')
def datetimeformat(value, format='%a, %d %b %Y %H:%M:%S %Z'):
    """Template filter for human-readable date formats"""
    return value.strftime(format)

@app.template_filter('summarize')
def summarize(content, length=250, suffix='...'):
    """Generate summary from marked-up content"""
    return helpers.summarize(content, length, suffix)

@app.template_filter('to_html')
def to_html(content, format):
    """Convert input to html"""
    return helpers.markup_to_html(format, content)

#---------------------------------------------------------------------------
# FRONTEND VIEWS

@app.route(get_route('static_files'))
def static(filename):
    """Send static files such as style sheets, JavaScript, etc."""
    static_path = os.path.join(app.root_path, 'templates', 'frontend',
                               cfg.THEME, 'static')
    return send_from_directory(static_path, filename)

@app.route(get_route('index'))
def show_index():
    """Render the frontpage"""
    g.cfg = cfg
    posts = posts_base.order_by(Post.pubdate.desc())
    return post_list(posts)

@app.route(get_route('show_post'))
def show_post(slug, **kwargs):
    """Render a Post"""
    g.cfg = cfg
    post = posts_base.filter(Post.slug==slug).first()
    return render_template(themed('post.html'), post=post[0])

@app.route(get_route('postlist_by_tag'))
def show_postlist_by_tag(tag):
    """Render a post list filtered by tag"""
    tagobj = Tag.query.filter(Tag.value==tag).first()
    if tagobj is None:
        abort(404)
    posts = posts_base.filter(Post.tags.contains(tagobj))
    return post_list(posts)

#---------------------------------------------------------------------------
# FEED VIEWS

# TODO: Perhaps these should instead be part of the API app?

@app.route(get_route('show_atom'))
def show_atom():
    """Render atom feed of posts"""
    g.cfg = cfg
    posts = posts_base.order_by(Post.pubdate.desc())[:cfg.FEEDITEMS]
    return render_template(os.path.join('frontend', 'atom.xml'), posts=posts)

@app.route(get_route('show_rss'))
def show_rss():
    """Render RSS feed of posts"""
    g.cfg = cfg
    posts = posts_base.order_by(Post.pubdate.desc())[:cfg.FEEDITEMS]
    return render_template(os.path.join('frontend', 'rss.xml'), posts=posts)

#---------------------------------------------------------------------------
# MAIN RUN LOOP
if __name__ == '__main__':
    app.run(host=cfg.FRONTEND_HOST, port=cfg.FRONTEND_PORT)
