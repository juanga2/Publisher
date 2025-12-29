from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings


def _build_engine_url() -> str:
    if settings.database_url.startswith("postgresql"):
        return settings.database_url
    if settings.database_url.startswith("sqlite"):
        return settings.database_url
    return f"postgresql+psycopg://{settings.database_url}"


engine = create_engine(_build_engine_url(), future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()
