#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Description {{{
"""
    imposter.public_api
    ~~~~~~~~~~~~~~~~~~~

    Public API application for the Imposter weblog app

    :copyright: (c) 2010 by Jochem Kossen.
    :license: BSD, see LICENSE.txt for more details.
"""
# }}}

# {{{ Imports
from flask import Flask, g, abort, jsonify
from datetime import datetime
from models import User, Tag, Status, Format, Post
from sqlalchemy.sql import and_

from database import DB

import os
# }}}

# Initialization {{{
app = Flask(__name__, static_path=None)
app.config.from_pyfile('config.py')
app.config.from_envvar('IMPOSTER_PUBLIC_API_CONFIG', silent=True)
db_session = DB(app.config['PUBLIC_API_DATABASE']).get_session()

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

def get_route(function):
    """Return complete route based on configuration and routes"""
    return '/%s%s' % (app.config['PUBLIC_API_PREFIX'], app.config['PUBLIC_API_ROUTES'][function])

def get_public_post_dict(post, user):
    """Return a dict containing public post data"""
    post_dict = post.get_public_dict()
    post_dict['pubdate'] = post.pubdate.strftime(app.config['POST_DATETIME_FORMAT'])
    post_dict['lastmoddate'] = post.lastmoddate.strftime(app.config['POST_DATETIME_FORMAT'])
    post_dict['username'] = user.username

    return post_dict

@app.after_request
def shutdown_session(response):
    """End session, close database"""
    db_session.remove()
    return response
# }}}

# Views {{{

@app.route(get_route('json_post_by_slug'))
def json_post_by_slug(slug):
    """Retrieve Post selected by slug in JSON format"""
    post_result = posts_base.filter(Post.slug==slug).first()
    if post_result is None:
        abort(404)
    post_dict = get_public_post_dict(post_result[0], post_result[2])
    return jsonify(post_dict)

@app.route(get_route('json_status_by_id'))
def json_status_by_id(id):
    """List of statuses in the database"""
    status = Status.query.filter(Status.id==id).first()
    if status is None:
        abort(404)
    return jsonify(status.get_public_dict())

@app.route(get_route('json_format_by_id'))
def json_format_by_id(id):
    """List of formats in the database"""
    fmt = Format.query.filter(Format.id==id).first()
    if fmt is None:
        abort(404)
    return jsonify(fmt.get_public_dict())

@app.route(get_route('json_user_by_id'))
def json_user_by_id(id):
    """List of usernames in the database"""
    user = User.query.filter(User.id==id).first()
    if user is None:
        abort(404)
    return jsonify(user.get_public_dict())

@app.route(get_route('json_sluglist_latest'))
def json_sluglist_latest():
    """List of post slugs (by post publication date) in the database"""
    posts = posts_base.order_by(Post.pubdate.desc())[:app.config['FEEDITEMS']]
    out = {'posts': []}
    for post in posts:
        out['posts'].append([post[0].pubdate.strftime(app.config['POST_DATETIME_FORMAT']), post[0].slug])

    return jsonify(out)

@app.route(get_route('json_posts_latest'))
def json_posts_latest():
    """Latest posts (by publication date) in the database"""
    posts = posts_base.order_by(Post.pubdate.desc())[:app.config['FEEDITEMS']]
    out = {'posts': []}
    for post_result in posts:
        post_dict = get_public_post_dict(post_result[0], post_result[2])
        out['posts'].append(post_dict)

    return jsonify(out)

@app.route(get_route('json_statuslist'))
def json_statuslist():
    """List of statuses in the database"""
    statuses = Status.query.all()
    out = {'statuses': []}
    for status in statuses:
        out['statuses'].append(status.value)

    return jsonify(out)

@app.route(get_route('json_taglist'))
def json_taglist():
    """List of tags in the database"""
    tags = Tag.query.all()
    out = {'tags': []}
    for tag in tags:
        out['tags'].append(tag.value)

    return jsonify(out)

@app.route(get_route('json_sluglist_by_tag'))
def json_sluglist_by_tag(tag):
    """Render a post list filtered by tag"""
    tagobj = Tag.query.filter(Tag.value==tag).first()
    if tagobj is None:
        abort(404)
    posts = posts_base.filter(Post.tags.contains(tagobj))
    out = {'posts': []}
    for post in posts:
        out['posts'].append(post[0].slug)

    return jsonify(out)
# }}}

# Main run loop {{{
if __name__ == '__main__':
    app.run(host=app.config['PUBLIC_API_HOST'], port=app.config['PUBLIC_API_PORT'])
# }}}

