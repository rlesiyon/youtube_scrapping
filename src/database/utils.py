import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from model import Base, Country, Video
import pandas as pd
from contextlib import contextmanager

def create_table_metadata(engine):
    Base.metadata.create_all(engine)

def create_database_engine(database_uri):
    return db.create_engine(database_uri, echo=True)

def table_exists(engine, name):
    return db.inspect(engine).dialect.has_table(engine.connect(), name)

def query(session, entity_class, entity_attr):
    return session.query(entity_class).filter_by(name=entity_attr).first()

def insert_to_database(database_uri):
    # create the engine for the database
    engine = db.create_engine(database_uri)

    # add countries
    youtubeid = pd.read_csv("../../data/youtube_videoid.csv")
    search_countries = youtubeid["country"].unique()
    with session_scope(engine) as session:
        if not table_exists(engine, "country"):
            create_table_metadata(engine)
        session.add_all([Country(name=country_name) for country_name in search_countries
                         if not query(session, Country, country_name)])
        session.commit()

    # adding videos
    youtubedata = pd.read_csv("../../data/youtube_videoinfo.csv")
    add_videos(youtubedata)


def add_videos(videos, engine):
    '''
    video_id: Mapped[str] = mapped_column(
        String(30), primary_key=True, nullable=False)
    country_id: Mapped[int] = mapped_column(nullable=False)
    category_id: Mapped[str] = mapped_column(String(30))
    channel_id: Mapped[str] = mapped_column(String(30))
    published_at: Mapped[str] = mapped_column(String(30))
    title: Mapped[str] = mapped_column(String(30))
    views: Mapped[int] = mapped_column(String(30))
    likes: Mapped[int] = mapped_column(String(30))
    '''

    with session_scope(engine) as session:
        for row in videos.to_dict(orient='records'):
            session.add(Video(**row))
        session.commit()
   
@contextmanager
def session_scope(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def drop_all_tables(db_uri):
    engine = db.create_engine(db_uri)
    metadata = db.MetaData(bind=engine)
    metadata.reflect()
    metadata.drop_all()

if __name__ == '__main__':
    # db_uri = "sqlite:///youtube_practice.db"
    # insert_to_database(db_uri)
    class Person:
        def __init__(self, name, country):
            self.name = name
            self.country = country
    print(getattr(Person))
