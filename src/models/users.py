from src.extensions import DB
from src.models import Base


class User(Base):
    __tablename__ = "users"
    hwd_id = DB.Column(DB.String)

    def __init__(self, hwd_id: str, *_, **__):
        self.hwd_id = hwd_id
