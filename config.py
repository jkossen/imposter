# Debug True/False
DEBUG = True

# Title of this weblog instance
TITLE='Imposter'

# Description of this weblog instance
DESCRIPTION='Another weblog'

# Link to home page
FRONTEND_BASEURL='http://CHANGE_THIS.ORG/imposter'

# Database connection strings, example: postgres://imposter:mysecretpassword@localhost:5432/imposter
FRONTEND_DATABASE = 'postgresql://imposter:imposter@localhost/imposter'
BACKEND_DATABASE = 'postgresql://imposter:imposter@localhost/imposter'

# Theme
THEME = 'default'

# Show summaries instead of full posts in feed content, post lists and front page?
SUMMARIES = True

# How many items do you want in feeds?
FEEDITEMS = 10

# Summary size in characters
SUMMARY_SIZE = 200

# Table prefix
TABLEPREFIX = 'imposter_'

# Host on which frontend runs
FRONTEND_HOST = '192.168.1.3'

# Host on which admin runs
ADMIN_HOST = '192.168.1.3'

# Port on which frontend runs
FRONTEND_PORT = 5000

# Port on which backend runs
ADMIN_PORT = 5001

# Secret string used for secure hashing, you could use os.urandom(20)
SECRET_KEY = 'CHANGE_THIS'

# Frontend prefix, ie the 'posts/' in http://yourweblog.net/posts/
FRONTEND_PREFIX=''

# Date format to use in URL's. Don't set it to an empty string, adjust FRONTEND_ROUTES instead.
URL_DATE_FORMAT = '%Y/%m/%d'

# Date / time format to use in templates.
POST_DATETIME_FORMAT = '%Y-%m-%d %H:%M'

# Routes to the view functions in the frontend
FRONTEND_ROUTES = {
    'index': '',
    'show_post': '<path:post_date>/<slug>.html',
    'show_rss': 'feed/rss/',
    'show_atom': 'feed/atom/',
    'postlist_by_tag': 'tag/<tag>/',
    'static_files': 'static/<path:filename>',
    }
