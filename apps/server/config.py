import os


class Config:
    """Config class for the application."""

    NODE_ENV = os.environ.get("NODE_ENV")

    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

    DB_NAME = os.environ.get("DB_NAME")
    DB_HOST = os.environ.get("DB_HOST")
    DB_PORT = os.environ.get("DB_PORT")
    DB_USER = os.environ.get("DB_USER")
    DB_PASS = os.environ.get("DB_PASS")
    DB_URI = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    SENTRY_DSN = os.environ.get("SENTRY_DSN")

    AZURE_PUBSUB_CONNECTION_STRING = os.environ.get("AZURE_PUBSUB_CONNECTION_STRING")
    AZURE_PUBSUB_HUB_NAME = os.environ.get("AZURE_PUBSUB_HUB_NAME")

    ZEP_API_URL = os.environ.get("ZEP_API_URL")
    ZEP_API_KEY = os.environ.get("ZEP_API_KEY")

    SERPAPI_API_KEY = os.environ.get("SERPAPI_API_KEY")

    TEST_USER_EMAIL = os.environ.get("TEST_USER_EMAIL")
    TEST_USER_PASSWORD = os.environ.get("TEST_USER_PASSWORD")
    JWT_EXPIRY = os.environ.get("JWT_EXPIRY")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    
    GITHUB_CLIENT_ID = os.environ.get("GITHUB_CLIENT_ID")
    GITHUB_CLIENT_SECRET = os.environ.get("GITHUB_CLIENT_SECRET")
    FRONTEND_URL = os.environ.get("FRONTEND_URL")
    
    GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
    AWS_REGION = os.environ.get("AWS_REGION")
    AWS_S3_BUCKET = os.environ.get("AWS_S3_BUCKET")


def get_config(key: str, default: str = None) -> str:
    return  # _config_instance.get_config(key, default)
