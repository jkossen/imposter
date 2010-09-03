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
PUBLIC_API_DATABASE = 'postgresql://imposter:imposter@localhost/imposter'
ADMIN_DATABASE = 'postgresql://imposter:imposter@localhost/imposter'

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

# Host on which public_api runs
PUBLIC_API_HOST = '192.168.1.3'

# Host on which admin runs
ADMIN_HOST = '192.168.1.3'

# Port on which frontend runs
FRONTEND_PORT = 5000

# Port on which public_api runs
PUBLIC_API_PORT = 5001

# Port on which backend runs
ADMIN_PORT = 5002

# If you use FastCGI, this specifies the path to the socket for the frontend
FRONTEND_FCGI_SOCKET = '/var/lib/imposter/frontend.sock'

# If you use FastCGI, this specifies the path to the socket for the admin
ADMIN_FCGI_SOCKET = '/var/lib/imposter/admin.sock'

# Secret string used for secure hashing, you could use os.urandom(20)
SECRET_KEY = 'CHANGE_THIS'

# Frontend prefix, ie the 'posts/' in http://yourweblog.net/posts/
FRONTEND_PREFIX='imposter/'

# Admin prefix, ie the 'admin/' in http://yourweblog.net/admin/
ADMIN_PREFIX=''

# public_api prefix, ie the 'api/' in http://yourweblog.net/api/
PUBLIC_API_PREFIX='api/'

# Date format to use in URL's. Don't set it to an empty string, adjust FRONTEND_ROUTES instead.
URL_DATE_FORMAT = '%Y/%m/%d'

# Date / time format to use in templates.
POST_DATETIME_FORMAT = '%Y-%m-%d %H:%M'

# Routes to the view functions in the frontend
FRONTEND_ROUTES = {
    'static_files': 'static/<path:filename>',
    'index': '',
    'show_post': '<path:post_date>/<slug>.html',
    'show_rss': 'feed/rss/',
    'show_atom': 'feed/atom/',
    'postlist_by_tag': 'tag/<tag>/',
    }

# Routes to the view functions in the frontend
PUBLIC_API_ROUTES = {
    'json_status_by_id': 'json/status/<id>/',
    'json_format_by_id': 'json/format/<id>/',
    'json_user_by_id': 'json/user/<id>/',
    'json_post_by_slug': 'json/post/<slug>/',
    'json_sluglist_latest': 'json/latest/',
    'json_posts_latest': 'json/posts/latest/',
    'json_statuslist': 'json/statuses/',
    'json_taglist': 'json/tags/',
    'json_sluglist_by_tag': 'json/tag/<tag>/',
    }

# Routes to the view functions in the admin
ADMIN_ROUTES = {
    'static_files': 'static/<path:filename>',
    'index': '',
    'login': 'login/',
    'logout': 'logout/',
    'new_post': 'edit/',
    'edit_post': 'edit/<int:post_id>/',
    'save_new_post': 'save/',
    'save_post': 'save/<int:post_id>/',
    }
