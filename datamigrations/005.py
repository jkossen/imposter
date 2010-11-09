from database import DB
from sqlalchemy.sql import and_
from models import User, Tag, Status, Format, Post, post_tags

def upgrade(app):
    pass

def downgrade(app):
    # column is dropped, no changes needed
    pass
