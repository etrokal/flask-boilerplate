from .db import db
from datetime import datetime, timezone


class BaseModel(db.Model):
    __abstract__ = True   # This is crucial – prevents a separate table

    created_at = db.Column(db.DateTime, default=datetime.now(
        timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc),
                           onupdate=datetime.now(timezone.utc), nullable=False)

    # Common methods
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)  # Assumes Flask's abort for 404
