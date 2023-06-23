from datetime import datetime

from . import db
from .constants import MAX_SHORT_LINK_LEN


class URLMap(db.Model):
    """Model with original and short URLs mapping."""
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text)
    short = db.Column(db.String(MAX_SHORT_LINK_LEN), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def from_dict(self, data):
        """Fills an empty class with the provided data from the dictionary."""
        api_db_map = {
            "url": "original",
            "custom_id": "short"
        }
        for api_field, db_field in api_db_map.items():
            if api_field in data:
                setattr(self, db_field, data[api_field])
