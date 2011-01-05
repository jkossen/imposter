# Debug True/False
DEBUG = True

# Title of this weblog instance
TITLE='Imposter'

# Description of this weblog instance
DESCRIPTION='Another weblog'

# Link to home page
FRONTEND_BASEURL='http://CHANGE_THIS.ORG/imposter'

# Database connection strings, example: postgres://imposter:mysecretpassword@localhost:5432/imposter
DATABASE = 'postgresql://imposter:imposter@localhost/imposter'

# Path to directory where uploaded files reside
UPLOAD_PATH = '/var/www/my-site.org/uploads/'

# Theme
THEME = 'default'

# Show summaries instead of full posts in feed content, post lists and front page?
SUMMARIES = True

# Nr of tags to show in the tag cloud
TAGCLOUD_NR_OF_TAGS = 100

# Range of fontsizes for the tagcloud in percentages
TAGCLOUD_MIN_FONTSIZE = 85
TAGCLOUD_MAX_FONTSIZE = 200

# How many items do you want in feeds?
FEEDITEMS = 10

# How many posts doe you want to show in a list?
ENTRIES_PER_PAGE = 10

# Summary size in characters
SUMMARY_SIZE = 200

# Table prefix
TABLEPREFIX = 'imposter_'

# Host on which frontend runs
HOST = '192.168.1.3'

# Port on which frontend runs
PORT = 5000

# If you use FastCGI, this specifies the path to the socket for the frontend
FCGI_SOCKET = '/var/lib/imposter/frontend.sock'

# Secret string used for secure hashing, you could use os.urandom(20)
SECRET_KEY = 'CHANGE_THIS'

# Frontend prefix, ie the 'posts/' in http://yourweblog.net/posts/
PREFIX='imposter/'

# Date / time format to use in templates.
POST_DATETIME_FORMAT = '%Y-%m-%d %H:%M'

# Routes to the view functions in the frontend
ROUTES = {
    'static_files': 'static/<path:filename>',
    'uploads': 'uploads/<path:filename>',
    'index': '',
    'show_postlist': 'list/<int:page>.html',
    'show_postlist_by_year_index': '<int:year>/',
    'show_postlist_by_year': '<int:year>/<int:page>.html',
    'show_postlist_by_month_index': '<int:year>/<month>/',
    'show_postlist_by_month': '<int:year>/<month>/<int:page>.html',
    'show_postlist_by_tag_index': 'tag/<tag>/',
    'show_postlist_by_tag': 'tag/<tag>/<int:page>.html',
    'show_postlist_by_username': 'user/<username>/<int:page>.html',
    'show_post': '<int:year>/<month>/<day>/<slug>.html',
    'show_page': 'page/<slug>.html',
    'show_rss': 'feed/rss/',
    'show_atom': 'feed/atom/',
    }
