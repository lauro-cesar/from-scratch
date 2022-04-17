"""
"""
from celery.schedules import crontab
import os
import firebase_admin
from firebase_admin import credentials
from typing import Any, Dict

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUTH_USER_MODEL = "accounts.User"
FIREBASE_APP = firebase_admin.initialize_app()



redis_host = os.environ.get("REDIS_HOST", default="localhost")
redis_port = os.environ.get("REDIS_PORT", default=6379)
redis_db = os.environ.get("REDIS_DB", default=0)
cache_host = os.environ.get("CACHE_HOST", default="localhost")
FQDNS = os.environ.get("FQDNS",default="localhost,192.168.1.12")
DATABASE_HOST=os.environ.get("DATABASE_HOST", default="127.0.0.1"),

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    default="_fake_key_",
)

DEBUG = int(os.environ.get("DEBUG", default=1))

REST_API_ADDRESS=os.environ.get("REST_API_ADDRESS", default="http://192.168.1.12:9099")
SOCKET_API_ADDRESS=os.environ.get("SOCKET_API_ADDRESS", default="ws://192.168.1.12:9099")


TEST=False
CELERY_BROKER_URL = f"redis://{redis_host}:{redis_port}/{redis_db}"
CELERY_RESULT_BACKEND = f"redis://{redis_host}:{redis_port}/{redis_db}"
CELERY_TASK_DEFAULT_QUEUE = os.environ.get(
    "REDIS_QUEUE_NAME", default="default_django_queue"
)
CELERY_ENABLE_UTC = False
CELERY_TIMEZONE = "America/Sao_Paulo"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_SERIALIZER = "json"
TASK_OFFSET_LIMIT=50
TIME_ZONE = "America/Sao_Paulo"


SENDGRID_API_KEY = os.environ.get(
    "SENDGRID_API_KEY",
    default="_fake_key_",
)
EMAIL_HOST = "smtp.sendgrid.net"
EMAIL_HOST_USER = "apikey"
EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL="naoresponda@sharedway.app"


DEFAULT_AUTO_FIELD="django.db.models.BigAutoField"
API_BASE_URI="http://192.168.1.12:9099"


REST_FRAMEWORK = {
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework_xml.parsers.XMLParser",
    ],
    # "EXCEPTION_HANDLER": "server.exception_handler.custom_exception_handler",
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {"anon": "1000/day", "user": "10000/day"},
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_PAGINATION_CLASS": "project.pagination.FlutterPagination",
    "PAGE_SIZE": 150,
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication"
    ],
}

SITE_ID = 1
ALLOWED_HOSTS = [
    "127.0.0.1", "localhost", "192.168.1.15", "192.168.1.12","192.168.1.21"    
]+list(FQDNS.split(","))


API_VERSION = 1
APPEND_SLASH = True
X_FRAME_OPTIONS = 'SAMEORIGIN'
SILENCED_SYSTEM_CHECKS = ['security.W019']

INSTALLED_APPS = [ 
    "jazzmin",
    "project_tools.apps.ProjectToolsConfig",
    "accounts.apps.AccountsConfig",    
    "project.apps.ProjectConfig",
    "datavault.apps.DatavaultConfig",
    "rest_framework",
    "corsheaders",
    "rest_framework.authtoken",
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.flatpages",
    "django.contrib.humanize",
    "django.contrib.gis",
    "channels",
]

#  
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

    # "project.debugger.DebugMe",
MIDDLEWARE = [
    'django.middleware.cache.UpdateCacheMiddleware',  
    "django.contrib.sites.middleware.CurrentSiteMiddleware",    
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",    
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "project.middleware.SSOAuthMiddleWare",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.flatpages.middleware.FlatpageFallbackMiddleware",
    "django.middleware.cache.FetchFromCacheMiddleware",
]
CSRF_USE_SESSIONS=True

CORS_ALLOWED_ORIGINS = [
    'http://localhost:8899',
    'http://127.0.0.1:8899',
    'http://localhost:9055',
    'http://192.168.1.12:9055',
    'http://localhost:8001',
]
CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS


ROOT_URLCONF = "project.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",        
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
        ],
        "APP_DIRS": False,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",           
            ],
        },
    }
]
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(redis_host, redis_port)],
        },
    },
}

CACHES = {
    "default": {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': f'redis://{redis_host}:{redis_port}',       
        'OPTIONS': {
            'db': '12',
            'parser_class': 'redis.connection.PythonParser',
            'pool_class': 'redis.BlockingConnectionPool',
        }

    }
}

WSGI_APPLICATION = "project.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": os.environ.get("DATABASE_NAME", default="django_db"),
        "USER": os.environ.get("DATABASE_USER", default="django_user"),
        "PASSWORD": os.environ.get("DATABASE_PASSWORD", default="django_password"),
        "HOST": os.environ.get("DATABASE_HOST", default="127.0.0.1"),
        "PORT": os.environ.get("DATABASE_PORT", default="5432"),
    }
}

LEAFLET_CONFIG = {
    "DEFAULT_CENTER": (-49, -29),
    "DEFAULT_ZOOM": 4,
    "MAX_ZOOM": 20,
    "MIN_ZOOM": 3,
    "SCALE": "both",
    "ATTRIBUTION_PREFIX": "Inspired by Life in GIS (Lauro Cesar)",
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "pt-br"
LANGUAGES = [("pt-br", "Português")]

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True
USE_THOUSAND_SEPARATOR = True
USE_L10N = True


STATIC_URL = "/static/"
MEDIA_URL = "/media/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


ASSETS_DIR = os.path.join(BASE_DIR, "assets")
PRIVATE_DIR = os.path.join(BASE_DIR, "media/private")

APP_NAME="API dashboard"


JAZZMIN_SETTINGS: Dict[str, Any] = {
   
    "user_avatar": "avatar",

    "topmenu_links": [
   
    ],
    "usermenu_links": [       
        {"model": "auth.User"},
    ],

    "show_sidebar": True,
    "navigation_expanded": False,
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-list",
    "related_modal_active": True,
    "custom_css": None,
    "custom_js": None,
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {"auth.user": "horizontal_tabs", "auth.group": "horizontal_tabs"},
    "language_chooser": False,



    "hide_apps": ["authtoken"],
    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [],
    # List of apps to base side menu (app or model) ordering off of
    "order_with_respect_to": [                                   
        "accounts"
        "auth"
        ],
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.User": "fas fa-user",    
        "auth.Group": "fas fa-users",
        "admin.LogEntry": "fas fa-file",
    },

}


JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": True,
    "brand_small_text": False,
    "brand_colour": False,
    "accent": "accent-primary",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": True,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": True,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": True,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "spacelab",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    },
    "actions_sticky_top": True
}
