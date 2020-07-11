import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'n)@5g+15-_%m=i#n(v16tz0f=ne)t4l34acp+9t!xgc$1vcbs1'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'server',
    'graphene_django',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'django_webserver',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
]

AUTH_USER_MODEL = 'server.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'FastQL.urls'

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

WSGI_APPLICATION = 'FastQL.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

DATE_FORMAT = "%d-%m-%Y"
TIME_FORMAT = "%H:%M"
DATE_TIME_FORMAT = "%d-%m-%Y %H:%M"

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [

        'rest_framework.permissions.IsAuthenticated',
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',

    'DATE_INPUT_FORMATS': [DATE_FORMAT],

    'TIME_INPUT_FORMATS': [TIME_FORMAT],

    'DATETIME_INPUT_FORMATS': [DATE_TIME_FORMAT],

    'DATE_FORMAT': DATE_FORMAT,

    'TIME_FORMAT': TIME_FORMAT,

    'DATETIME_FORMAT': DATE_TIME_FORMAT,

}

GRAPHENE = {
    'SCHEMA': 'ql.schema',
    'MIDDLEWARE': [
        'graphql_jwt.middleware.JSONWebTokenMiddleware',
    ],
}

AUTHENTICATION_BACKENDS = [
    'graphql_jwt.backends.JSONWebTokenBackend',
    'django.contrib.auth.backends.ModelBackend',
]

GRAPHQL_JWT = {
    'JWT_ALLOW_ARGUMENT': False,
}

QL_EXCLUDE_AUTO_QUERYS = ['User']
QL_EXCLUDE_AUTO_MUTATIONS = ['User']
