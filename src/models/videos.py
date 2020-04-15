from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID
from src.extensions import DB
from src.models import Base


class Video(Base):
    __tablename__ = "videos"
    identifier = DB.Column(UUID(as_uuid=True), primary_key=True)
    name = DB.Column(DB.String)
    url = DB.Column(DB.String)

    hwd_id = DB.Column(DB.String, DB.ForeignKey("users.hwd_id"))
    user = DB.relationship("User")

    def __init__(self, name: str, url: str, hwd_id: str, *_, **__):
        self.name = name
        self.identifier = uuid4()
        self.url = url
        self.hwd_id = hwd_id
