from database import DB
from sqlalchemy.sql import and_
from models import User, Tag, Status, Format, Post, post_tags

def upgrade(app):
    """ data migration to update the Tag.count fields """
    db_session = DB(app.config['DATABASE']).get_session()
    existing_tags = db_session.query(Tag).all()

    for tag in existing_tags:
        tag.count = db_session.query(Post, Status).filter(and_(Post.status_id==Status.id,
            Status.value=='public',
            )).filter(Post.tags.contains(tag)).count()
    db_session.commit()

def downgrade(app):
    # column is dropped, no changes needed
    pass
