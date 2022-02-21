from sqlalchemy import TIMESTAMP, Column, Integer, String, Boolean, DateTime, text
from .database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column("id", Integer, primary_key=True, nullable=False)
    title = Column("title", String, nullable=False)
    content = Column("content", String, nullable=False)
    published = Column("published", Boolean, server_default="TRUE", nullable=False)
    created_at = Column(
        "created_at",
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
    )
