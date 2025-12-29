import os


class Settings:
    def __init__(self) -> None:
        self.database_url = os.getenv("DATABASE_URL", "sqlite:///./publisher.db")
        self.token_encryption_key = os.getenv("TOKEN_ENCRYPTION_KEY")
        self.oauth_consumer_key = os.getenv("OAUTH_CONSUMER_KEY")
        self.oauth_consumer_secret = os.getenv("OAUTH_CONSUMER_SECRET")
        self.base_url = os.getenv("BASE_URL", "http://localhost:8000")
        self.session_cookie_name = "publisher_session"
        self.session_ttl_seconds = int(os.getenv("SESSION_TTL_SECONDS", "1209600"))
        self.version = os.getenv("APP_VERSION", "0.1.0")


settings = Settings()
