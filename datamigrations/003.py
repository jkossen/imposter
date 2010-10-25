from database import DB
from sqlalchemy.sql import and_
from models import User, Tag, Status, Format, Post, post_tags
from flaskjk import markup_to_html

def upgrade(app):
    """ data migration to update the Tag.count fields """
    db_session = DB(app.config['DATABASE']).get_session()
    existing_posts = db_session.query(Post).all()

    for post in existing_posts:
        post.summary_html = markup_to_html(post.format, post.summary)
        post.content_html = markup_to_html(post.format, post.content)

    db_session.commit()

def downgrade(app):
    # column is dropped, no changes needed
    pass
