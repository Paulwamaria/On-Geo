"""
Django settings for ongeo_main project.

Generated by 'django-admin startproject' using Django 2.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""


import os
import django_heroku
import dj_database_url
from os import environ
from decouple import config,Csv

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
MODE=config("MODE", default="dev")
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True



# Application definition

INSTALLED_APPS = [
    'ongeo.apps.OngeoConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'crispy_forms',
    'django_tables2',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'ongeo_main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ongeo_main.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases


if config('MODE')=="dev":
   DATABASES = {
       'default': {
           'ENGINE': 'django.contrib.gis.db.backends.postgis',
           'NAME': config('DB_NAME'),
           'USER': config('DB_USER'),
           'PASSWORD': config('DB_PASSWORD'),
           'HOST': config('DB_HOST'),
           'PORT': '',
       }
       
   }
# production
else:
   DATABASES = {
       'default': dj_database_url.config(
           default=config('DATABASE_URL')
       )
   }

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())



# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'


TIME_ZONE = 'Africa/Nairobi'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'statics'),
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CRISPY_TEMPLATE_PACK = 'bootstrap4'

LOGIN_REDIRECT_URL = 'home'
LOGIN_URL = 'login'



django_heroku.settings(locals())
# If we aren't building in /app, then fix the environment variables which assumed we were
BUILD_DIR = os.environ.get("BUILD_DIR", "/app")
if BUILD_DIR != "/app":
    lib_re = re.compile(r'(?:^|(?<=:))/app(?=/)', re.ASCII | re.MULTILINE)
    lib_vars = set(["LIBRARY_PATH","LD_LIBRARY_PATH","GEOS_LIBRARY_PATH","GDAL_LIBRARY_PATH","PROJ4_LIBRARY_PATH","GDAL_DATA","GDAL"])
    for lib_var in lib_vars:
        if lib_var in os.environ and os.environ.get(lib_var, None):
            os.environ[lib_var] = lib_re.sub(BUILD_DIR, os.environ.get(lib_var))

# Glob for archive lib name within path provided or else LD_LIBRARY_PATH
def lib_find_archive(lib_paths, lib_name):
    import subprocess, glob

    if lib_paths is not None:
        if not lib_paths or os.path.isfile(lib_paths):
            # Quit if path is empty or points to an actual file
            return lib_paths or None

        elif not os.path.isdir(lib_paths):
            # Separate archive path from name
            lib_name = os.path.basename(lib_paths) or lib_name
            lib_paths = os.path.dirname(lib_paths) or None

    # lib_name must be populated
    if not lib_name: return None

    # Glob search within lib_path or else LD_LIBRARY_PATH
    if lib_paths:
        lib_paths = [lib_paths]
    elif(os.environ.get("LD_LIBRARY_PATH", None)):
        lib_paths = os.environ.get("LD_LIBRARY_PATH", None).split(':')
    else:
        return None

    # Glob-seach each directory for lib_name
    for lib_path in lib_paths:
        if not (lib_path and os.path.isdir(lib_path)):
            continue

        # Find matching archive files
        lib_path_glob = os.path.join(lib_path, lib_name)
        lib_paths_globbed = glob.glob(lib_path_glob)

        # Use shortest-length match
        if lib_paths_globbed: return sorted(lib_paths_globbed, key=len)[0]

    # Archive not found
    return None

# Collect library paths and correct each, if necessary
GDAL_LIBRARY_PATH = lib_find_archive( os.environ.get('GDAL_LIBRARY_PATH', None), 'libgdal.so*' )
GEOS_LIBRARY_PATH = lib_find_archive( os.environ.get('GEOS_LIBRARY_PATH', None), 'libgeos_c.so*' )
PROJ4_LIBRARY_PATH = lib_find_archive( os.environ.get('PROJ4_LIBRARY_PATH', None), 'libproj.so*' )

