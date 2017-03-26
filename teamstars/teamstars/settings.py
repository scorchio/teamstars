"""
Django settings for teamstars project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


SECRET_KEY = os.environ['DJANGO_SECRET']

DEBUG = os.environ.get('DJANGO_DEBUG', False)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
                'django.contrib.auth.context_processors.auth',
                'django.core.context_processors.request',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

ALLOWED_HOSTS = os.environ.get('HOSTS', '127.0.0.1').split('|')

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',
    'common',
    'votes',
    'calendstar',
    'rest_framework',
    'debug_toolbar',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'teamstars.urls'

WSGI_APPLICATION = 'teamstars.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
if 'RDS_DB_NAME' in os.environ:
    # Use production settings
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }
elif 'USE_SQLITE' in os.environ and os.environ['USE_SQLITE'] == 'True':
    # Use lightweight dev env
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    # Use dev env with postgre
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'teamstars',
            'USER': 'teamstars',
            'PASSWORD': 'teamstars',
            'HOST': 'localhost',
            'PORT': '5432',
        },
        'legacy': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ['LEGACY_DB_NAME'],
            'USER': os.environ['LEGACY_DB_USER'],
            'PASSWORD': os.environ['LEGACY_DB_PASSWORD'],
            'HOST': 'localhost',
            'PORT': '3306',
        }
    }

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Budapest'

USE_I18N = True

USE_L10N = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "..", "www", "static")
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
# TODO Scor: fix static file handling for debug toolbar on windows

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = '/media/'

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler'
        }
    },
    'loggers': {
        'votes': {
            'handlers': ['console'],
            'level': 'DEBUG',
        }
    }
}

AUTHENTICATION_BACKENDS = (
    'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend'
)


if 'SOCIAL_AUTH_FACEBOOK_KEY' in os.environ:
    SOCIAL_AUTH_FACEBOOK_KEY = os.environ['SOCIAL_AUTH_FACEBOOK_KEY']
    SOCIAL_AUTH_FACEBOOK_SECRET = os.environ['SOCIAL_AUTH_FACEBOOK_SECRET']

SOCIAL_AUTH_FACEBOOK_SCOPE = ['public_profile', 'email', 'user_location', 'user_birthday']

SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'id, name, email, age_range, link, picture, birthday, location'
}

SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/votes/'

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'common.social_auth_pipeline.save_fb_profile',
    'common.social_auth_pipeline.save_profile_picture',
)
