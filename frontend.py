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
from datetime import date, datetime
from models import User, Tag, Status, Post, Page
from sqlalchemy.sql import select, and_, func

from database import DB
from flaskjk import Viewer, Paginator, summarize, markup_to_html

import os
# }}}

# Initialization {{{
app = Flask(__name__, static_path=None)
app.config.from_pyfile('config_frontend.py')
app.config.from_envvar('IMPOSTER_FRONTEND_CONFIG', silent=True)
db_session = DB(app.config['DATABASE']).get_session()
viewer = Viewer(app, 'frontend', app.config['UPLOAD_PATH'])
# }}}

# Shortcut functions {{{
def filter_public():
    return and_(Post.status_id==Status.id,
            Status.value=='public',
            Post.user_id==User.id,
            Post.pubdate <= datetime.now()
            )

def posts_base():
    """ base query to make sure we get only published posts """
    return db_session.query(Post, Status, User).filter(filter_public())

def pages_base():
    """ base query to make sure we get only published pages """
    return db_session.query(Page, Status, User).filter(and_(Page.status_id==Status.id,
        Status.value=='public',
        Page.pubdate <= datetime.now()))

@app.after_request
def shutdown_session(response):
    """End session, close database"""
    db_session.remove()
    return response
# }}}

# Context Processors {{{
@app.context_processor
def inject_pages():
    return dict(pages=pages_base())

@app.context_processor
def inject_recent_posts():
    return dict(recent_posts=posts_base().order_by(Post.pubdate.desc())[0:10])

@app.context_processor
def inject_tag_cloud():
    tags = db_session.query(Tag).filter(Tag.count>=1).order_by(Tag.count.desc())[0:app.config['TAGCLOUD_NR_OF_TAGS']]

    min_percent = app.config['TAGCLOUD_MIN_FONTSIZE']
    max_percent = app.config['TAGCLOUD_MAX_FONTSIZE']
    min = tags[-1].count
    max = tags[0].count

    tags_sizes = []
    for tag in tags:
        size = min_percent + ((max-(max-(tag.count-min)))*(max_percent-min_percent)/(max-min))
        tags_sizes.append([tag, size])

    return dict(tags=sorted(tags_sizes, key=lambda tag:tag[0].value))

@app.context_processor
def inject_archives():
    min_max_pubdates = db_session.query(func.min(Post.pubdate), func.max(Post.pubdate)).filter(filter_public())
    #min_year = min_max_pubdates[0].year()
    #max_year = min_max_pubdates[1].year()
    #archives = []
    return dict(min_max_pubdates=min_max_pubdates)
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
    return show_postlist()

@viewer.view('show_post')
def show_post(slug, **kwargs):
    """Render a Post"""
    query = posts_base().filter(Post.slug==slug)
    if query.count() < 1:
        abort(404)
    post = query.first()
    return viewer.render('post.html', post=post[0])

@viewer.view('show_page')
def show_page(slug, **kwargs):
    """Render a Page"""
    query = pages_base().filter(Page.slug==slug)
    if query.count() < 1:
        abort(404)
    page = query.first()
    return viewer.render('page.html', page=page[0])

@viewer.view('show_postlist')
def show_postlist(page=1):
    """Render the frontpage"""
    posts = posts_base().order_by(Post.pubdate.desc())
    paginator = Paginator(posts, app.config['ENTRIES_PER_PAGE'], page, 'show_postlist')
    return viewer.render('post_list.html', posts=posts, paginator=paginator)

@viewer.view('show_postlist_by_month_index')
@viewer.view('show_postlist_by_month')
def show_postlist_by_month(year, month, page=1):
    """Render a post list filtered by month"""
    start_of_month = date(int(year), int(month), 1)
    next_month = date(int(year)+((int(month)+1)/12), (int(month)+1) % 12, 1)
    posts = posts_base().filter(Post.pubdate > start_of_month).filter(Post.pubdate <= next_month).order_by(Post.pubdate.desc())
    paginator = Paginator(posts, app.config['ENTRIES_PER_PAGE'], page, 'show_postlist_by_month', year=year, month=month)
    return viewer.render('post_list.html', posts=posts, paginator=paginator)

@viewer.view('show_postlist_by_year_index')
@viewer.view('show_postlist_by_year')
def show_postlist_by_year(year, page=1):
    """Render a post list filtered by year"""
    year = int(year)
    posts = posts_base().filter(Post.pubdate > date(year, 1, 1)).filter(Post.pubdate <= date(year+1, 1, 1)).order_by(Post.pubdate.desc())
    paginator = Paginator(posts, app.config['ENTRIES_PER_PAGE'], page, 'show_postlist_by_year', year=year)
    return viewer.render('post_list.html', posts=posts, paginator=paginator)

@viewer.view('show_postlist_by_tag_index')
@viewer.view('show_postlist_by_tag')
def show_postlist_by_tag(tag, page=1):
    """Render a post list filtered by tag"""
    tagobj = Tag.query.filter(Tag.value==tag).first()
    if tagobj is None:
        abort(404)
    posts = posts_base().filter(Post.tags.contains(tagobj)).order_by(Post.pubdate.desc())
    paginator = Paginator(posts, app.config['ENTRIES_PER_PAGE'], page, 'show_postlist_by_tag', tag=tag)
    return viewer.render('post_list.html', posts=posts, paginator=paginator)

@viewer.view('show_postlist_by_username')
def show_postlist_by_username(username, page=1):
    """Render a post list filtered by username"""
    userobj = User.query.filter(User.username==username).first()
    if userobj is None:
        abort(404)
    posts = posts_base().filter(Post.user==userobj).order_by(Post.pubdate.desc())
    paginator = Paginator(posts, app.config['ENTRIES_PER_PAGE'], page, 'show_postlist_by_username', username=username)
    return viewer.render('post_list.html', posts=posts, paginator=paginator)

@viewer.view('show_atom')
def show_atom():
    """Render atom feed with recent posts"""
    posts = posts_base().order_by(Post.pubdate.desc())[:app.config['FEEDITEMS']]
    return viewer.render('atom.xml', posts=posts)

@viewer.view('show_rss')
def show_rss():
    """Render RSS feed with recent posts"""
    posts = posts_base().order_by(Post.pubdate.desc())[:app.config['FEEDITEMS']]
    return viewer.render('rss.xml', posts=posts)
# }}}

# Main run loop {{{
if __name__ == '__main__':
    app.run(host=app.config['HOST'], port=app.config['PORT'])
# }}}
