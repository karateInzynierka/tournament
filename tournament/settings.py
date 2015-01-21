import os
from os.path import dirname, join

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

PROJECT_PATH = os.path.dirname(os.path.dirname(__file__))

MEDIA_ROOT = join(BASE_DIR, 'media')

MEDIA_URL = '/media/'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATIC_TEMPLATES = os.path.join(BASE_DIR, 'static')

# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'static'),
# )

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)

# STATICFILES_DIRS = (
#     STATIC_PATH,
# )

MAX_UPLOAD_SIZE = 20971520  # 20MB

CONTENT_TYPES = ['application/pdf', 'image/jpeg', 'image/png']  # .pdf, .jpeg and .png

SECRET_KEY = '$2570k@5cvn*q3tju((%i!@aunnw8_lcknx&n=vr3kc4#ndnmt'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']

TIME_ZONE = 'Europe/Warsaw'

LANGUAGE_CODE = 'pl-pl'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'datetimewidget',
    'main',
    'karatekyokushin',
    'karateshotokan',
    'easy_pdf',
)

ROOT_URLCONF = 'tournament.urls'

WSGI_APPLICATION = 'tournament.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

GRAPH_MODELS = {
  'all_applications': True,
  'group_models': True,
}

USE_I18N = True

USE_L10N = True

USE_TZ = True


