import datetime as dt
import uuid

from sqlalchemy import JSON, Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from app.db import Base


def _now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def _uuid() -> str:
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=_uuid)
    email = Column(String, nullable=True)
    display_name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=_now, nullable=False)


class Wiki(Base):
    __tablename__ = "wikis"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    api_base = Column(String, nullable=False)
    rest_base = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=_now, nullable=False)


class LinkedAccount(Base):
    __tablename__ = "linked_accounts"

    id = Column(String, primary_key=True, default=_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    wiki_id = Column(String, ForeignKey("wikis.id"), nullable=False)
    mw_username = Column(String, nullable=False)
    oauth_token_encrypted = Column(String, nullable=False)
    oauth_token_secret_encrypted = Column(String, nullable=False)
    scopes = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), default=_now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=_now, nullable=False)

    user = relationship("User")
    wiki = relationship("Wiki")


class Session(Base):
    __tablename__ = "sessions"

    id = Column(String, primary_key=True, default=_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    csrf_token = Column(String, nullable=False)
    oauth_request_token = Column(String, nullable=True)
    oauth_request_token_secret = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), default=_now, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)

    user = relationship("User")
