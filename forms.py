# -*- coding: utf-8 -*-
# Description {{{
"""
    imposter.forms
    ~~~~~~~~~~~~~~

    WTForms classes for creating forms and input validation.

    :copyright: (c) 2010-2011 by Jochem Kossen.
    :license: BSD, see LICENSE.txt for more details.
"""
# }}}

# Imports {{{
from flaskext.wtf import Form, TextField, PasswordField, DateTimeField, SelectField, TextAreaField, FieldList, Required
from wtforms.fields import Field
from wtforms.widgets import TextInput
from models import Format, Status, Tag
# }}}

# Helper functions {{{
def get_format(value):
    """Retrieve Format object based on given String"""
    query = Format.query.filter(Format.value==value)
    return query.one()

def get_status(value):
    """Retrieve Status object based on given String"""
    query = Status.query.filter(Status.value==value)
    return query.one()

def get_tag(value):
    """Retrieve Tag object based on given String

    If no such Tag object exists, return a new Tag object.
    """
    tag = Tag.query.filter(Tag.value==value).first()
    if tag is None:
        return Tag(value)
    return tag
# }}}

# Classes {{{
class TagListField(Field):
    """Custom TagListField for editing tags"""
    widget = TextInput()

    def _value(self):
        if self.data:
            tags = []
            for item in self.data:
                tags.append(item.value)
            return u', '.join(tags)
        else:
            return u''

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = [get_tag(x.strip()) for x in valuelist[0].split(',')]
        else:
            self.data = []

class FormatField(SelectField):
    """A SelectField for picking a Format"""
    def populate_obj(self, obj, name):
        """Data comes in as a String, but the targetet object expects a Format object"""
        setattr(obj, name, get_format(self.data))

class StatusField(SelectField):
    """A SelectField for picking a Status"""
    def populate_obj(self, obj, name):
        """Data comes in as a String, but the targetet object expects a Status object"""
        setattr(obj, name, get_status(self.data))

class PostForm(Form):
    """Form for the Post objects from Imposter.models"""
    title = TextField('Title', validators=\
                      [Required(message='Title is required.')])
    tags = TagListField('Tags', validators=\
                        [Required(message='Tags are required')])
    pubdate = DateTimeField('Publication date', format='%Y-%m-%d %H:%M',
                            validators=\
                            [Required(message='Wrong date or date format.')])
    format = FormatField('Format', choices=[('markdown','Markdown'),
                                            ('rest', 'ReStructuredText')],
                         validators=\
                         [Required(message='Please pick a format')])
    status = StatusField('Status', choices=[('draft','Draft'),
                                            ('private','Private'),
                                            ('public','Public')],
                         validators=\
                         [Required(message='Please pick a status')])
    summary = TextAreaField('Summary', validators=\
                            [Required('Summary is required.')])
    content = TextAreaField('Content', validators=\
                            [Required('Content is required.')])

class PageForm(Form):
    """Form for the Page objects from Imposter.models"""
    title = TextField('Title', validators=\
                      [Required(message='Title is required.')])
    pubdate = DateTimeField('Publication date', format='%Y-%m-%d %H:%M',
                            validators=\
                            [Required(message='Wrong date or date format.')])
    format = FormatField('Format', choices=[('markdown','Markdown'),
                                            ('rest', 'ReStructuredText')],
                         validators=\
                         [Required(message='Please pick a format')])
    status = StatusField('Status', choices=[('draft','Draft'),
                                            ('private','Private'),
                                            ('public','Public')],
                         validators=\
                         [Required(message='Please pick a status')])
    content = TextAreaField('Content', validators=\
                            [Required('Content is required.')])

class LoginForm(Form):
    username = TextField('Username', validators=[Required(message='Username is required.')])
    password = PasswordField('Password', validators=[Required(message='Password is required.')])
# }}}
