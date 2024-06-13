from django.utils.translation import gettext_lazy as _
from pathlib import Path
import environ
import os


BASE_DIR = Path(__file__).resolve().parent.parent.parent
env = environ.Env()
# -- MUST BE REMOVED -- #
env.read_env(f'{BASE_DIR.parent}/.env', overwrite=True)
# -- MUST BE REMOVED -- #


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'crispy_forms',
    'crispy_bootstrap5',
    'parler',
    'rosetta',

    'cart.apps.CartConfig',
    'coupon.apps.CouponConfig',
    'order.apps.OrderConfig',
    'shop.apps.ShopConfig',
    'zarinpal.apps.ZarinpalConfig',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.locale.LocaleMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'cart.context_processors.cart',
            ],
            'builtins': ['core.builtins'],
        },
    },
]
DATABASES = {'default': env.db()}
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


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
ROOT_URLCONF = 'core.urls'
WSGI_APPLICATION = 'core.wsgi.application'


LANGUAGE_CODE = 'en'
TIME_ZONE = 'Asia/Tehran'
USE_I18N = True
USE_TZ = True
LANGUAGES = [
    ('en', _('English')),
    ('fa', _('Farsi')),
]
LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]
PARLER_LANGUAGES = {
    None: (
        {'code': 'en', },
        {'code': 'fa', },
    ),
    'default': {
        'fallback': 'en',
        'hide_untranslated': False,
    }
}


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')


email_config = env.email()
EMAIL_USE_TLS = True
EMAIL_BACKEND = email_config['EMAIL_BACKEND']
EMAIL_HOST = email_config['EMAIL_HOST']
EMAIL_PORT = email_config['EMAIL_PORT']
EMAIL_HOST_USER = email_config['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = email_config['EMAIL_HOST_PASSWORD']


CRISPY_TEMPLATE_PACK = 'bootstrap5'
ZARINPAL_MERCHANT_ID = env.str('ZARINPAL_MERCHANT_ID')
CELERY_BROKER_URL = env.str('CELERY_BROKER_URL')
REDIS_URL = env.str('REDIS_URL')
REDIS_EXPIRATION_TIME = env.int('REDIS_EXPIRATION_TIME')
