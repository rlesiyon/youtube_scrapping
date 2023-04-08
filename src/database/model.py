from sqlalchemy import String
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class Base(DeclarativeBase):
    pass

class Country(Base):
    __tablename__ = "country"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30))

    def __repr__(self) -> str:
        return f"Country(id={self.id!r}, name={self.name!r})"
    
class Video(Base):
    __tablename__ = "video"

    video_id: Mapped[str] = mapped_column(
        String(30), primary_key=True, nullable=False)
    country_id: Mapped[int] = mapped_column(nullable=False)
    category_id: Mapped[str] = mapped_column(String(30))
    channel_id: Mapped[str] = mapped_column(String(30))
    published_at: Mapped[str] = mapped_column(String(30))
    title: Mapped[str] = mapped_column(String(30))
    views: Mapped[int] = mapped_column(String(30))
    likes: Mapped[int] = mapped_column(String(30))

    def __repr__(self) -> str:
        return f"Video(video_id={self.video_id!r}, title={self.title!r}, viewsitle={self.views!r})"

class Description(Base):
    __tablename__ = "video_description"

    video_id: Mapped[str] = mapped_column(
        String(30), primary_key=True, nullable=False)
    description: Mapped[str] = mapped_column(String(30))

    def __repr__(self) -> str:
        return f"Description(id={self.id!r}, description={self.description[:min(10, len(self.description))]!r})"

    
