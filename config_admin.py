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

# Theme
THEME = 'default'

# How many posts doe you want to show in a list?
ENTRIES_PER_PAGE = 10

# Show summaries instead of full posts in feed content, post lists and front page?
SUMMARIES = True

# How many items do you want in feeds?
FEEDITEMS = 10

# Summary size in characters
SUMMARY_SIZE = 200

# Table prefix
TABLEPREFIX = 'imposter_'

# Host on which admin runs
HOST = '192.168.1.3'

# Port on which app runs
PORT = 5002

# If you use FastCGI, this specifies the path to the socket for the admin
FCGI_SOCKET = '/var/lib/imposter/admin.sock'

# Secret string used for secure hashing, you could use os.urandom(20)
SECRET_KEY = 'CHANGE_THIS'

# Frontend prefix, ie the 'posts/' in http://yourweblog.net/posts/
PREFIX=''

# Date format to use in URL's. Don't set it to an empty string, adjust FRONTEND_ROUTES instead.
URL_DATE_FORMAT = '%Y/%m/%d'

# Date / time format to use in templates.
POST_DATETIME_FORMAT = '%Y-%m-%d %H:%M'

# Routes to the view functions in the admin
ROUTES = {
    'static_files': 'static/<path:filename>',
    'index': '',
    'login': 'login/',
    'logout': 'logout/',
    'new_post': 'post/new/edit/',
    'new_page': 'page/new/edit/',
    'pages_list': 'pages/<int:page>.html',
    'posts_list': 'posts/<int:page>.html',
    'edit_post': 'post/<int:post_id>/edit/',
    'edit_page': 'page/<int:page_id>/edit/',
    'save_new_post': 'post/new/save/',
    'save_new_page': 'page/new/save/',
    'save_post': 'post/<int:post_id>/save/',
    'save_page': 'page/<int:page_id>/save/',
    'recalculate_tagcounts': 'tags/recalculate/',
    }

# These keys will be replaced by their values before converting to html
REPL_TAGS = {
    '##UPLOADS##': 'https://my-website.org/uploads'
}
