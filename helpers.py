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

utility function library

"""

from flask import g
from hashlib import sha256
from docutils import core
from docutils.writers.html4css1 import Writer,HTMLTranslator
import markdown
import re
from unicodedata import normalize

def hashify(seed, text):
    return sha256('%s%s' % (seed, text)).hexdigest()

class HTMLFragmentTranslator(HTMLTranslator):
    def __init__(self, document):
        HTMLTranslator.__init__(self, document)
        self.head_prefix = ['','','','','']
        self.body_prefix = []
        self.body_suffix = []
        self.stylesheet = []
        def astext(self):
            return ''.join(self.body)

html_fragment_writer = Writer()
html_fragment_writer.translator_class = HTMLFragmentTranslator

def rest_to_html(s):
    """Convert ReST input to HTML output"""
    return core.publish_string(s, writer = html_fragment_writer)

def markup_to_html(format, text):
    """Convert supported marked-up input to HTML output"""
    if format.value == 'rest':
        return rest_to_html(text)
    elif format.value == 'markdown':
        return markdown.markdown(text)

    return text


def slugify(text, delim=u'-', maxlen=128):
    """Generates an ASCII-only slug usable in paths and URLs.

    Based on http://flask.pocoo.org/snippets/5/

    """
    punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
    result = []
    for word in punct_re.split(text.lower()):
        word = normalize('NFKD', unicode(word)).encode('ascii', 'ignore')
        if word:
            result.append(word)
    return unicode(delim.join(result)[0:maxlen])

def summarize(content, length=250, suffix='...'):
    """Generate summary from given content

    Based on http://stackoverflow.com/questions/250357/smart-truncate-in-python

    """
    if len(content) <= length:
        return content
    return content[:length+1].rsplit(' ', 1)[0]+suffix
