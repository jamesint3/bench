import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]


def _env(name: str, default: str) -> str:
    return os.getenv(name, default).strip()


DEBUG = _env("GEXABLE_DEBUG", "false").lower() == "true"
SECRET_KEY = os.getenv("GEXABLE_SECRET_KEY")
if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = "gexable-esg-dev-key"
    else:
        raise RuntimeError("GEXABLE_SECRET_KEY must be set when DEBUG is false")
ALLOWED_HOSTS = [h.strip() for h in _env("GEXABLE_ALLOWED_HOSTS", "*").split(",") if h.strip()]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core_api",
    "apps.core",
    "apps.tenants",
    "apps.users",
    "apps.permissions",
    "apps.data_ingestion",
    "apps.emissions_management",
    "apps.energy_management",
    "apps.decarbonization",
    "apps.supplier_intelligence",
    "apps.audits_actions",
    "apps.analytics",
    "apps.reporting",
    "apps.dashboard_api",
    "rest_framework",
    "drf_spectacular",
]

MIDDLEWARE = [
    "core_api.middleware.TenantContextMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "core_api.middleware.RoleContextMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {"context_processors": [
            "django.template.context_processors.request",
            "django.contrib.auth.context_processors.auth",
            "django.contrib.messages.context_processors.messages",
        ]},
    }
]

WSGI_APPLICATION = "config.wsgi.application"

DB_ENGINE = _env("GEXABLE_DB_ENGINE", "sqlite3").lower()
if DB_ENGINE in {"postgres", "postgresql", "timescaledb"}:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": _env("GEXABLE_DB_NAME", "gexable_esg"),
            "USER": _env("GEXABLE_DB_USER", "gexable"),
            "PASSWORD": _env("GEXABLE_DB_PASSWORD", "gexable"),
            "HOST": _env("GEXABLE_DB_HOST", "localhost"),
            "PORT": _env("GEXABLE_DB_PORT", "5432"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": _env("GEXABLE_DB_NAME", str(BASE_DIR / "db.sqlite3")),
        }
    }

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "users.User"

# Many domain apps currently ship without Django migration files in this scaffold.
# Mark them as unmigrated so `migrate --run-syncdb` can create their tables at runtime.
UNMIGRATED_LOCAL_APPS = [
    "core",
    "tenants",
    "permissions",
    "data_ingestion",
    "emissions_management",
    "energy_management",
    "decarbonization",
    "supplier_intelligence",
    "audits_actions",
    "analytics",
    "reporting",
    "dashboard_api",
]
MIGRATION_MODULES = {app_label: None for app_label in UNMIGRATED_LOCAL_APPS}

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Gexable ESG API",
    "VERSION": "0.1.0",
}
