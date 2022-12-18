from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Index
from sqlalchemy.types import TypeDecorator
from sqlalchemy.dialects.postgresql import TSVECTOR
from datetime import datetime

db = SQLAlchemy()


class TSVector(TypeDecorator):
    impl = TSVECTOR


class Video(db.Model):
    __tablename__ = "videos"

    id = db.Column(db.String(), primary_key=True)
    title = db.Column(db.String())
    description = db.Column(db.String())
    published_at = db.Column(db.DateTime, default=datetime.utcnow())
    thumbnail = db.Column(db.String())

    __ts_vector__ = db.Column(TSVector(), db.Computed(
        "(setweight(to_tsvector('english', coalesce(title, '')), 'A') || "
        "setweight(to_tsvector('english', coalesce(description, '')), 'B'))",
        persisted=True))

    __table_args__ = (Index('idx_video___ts_vector__',
                            __ts_vector__, postgresql_using='gin'),)
